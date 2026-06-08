#!/usr/bin/env python3
"""
Local watermark remover (the deterministic engine behind the /remove-watermark skill).

No LLM, no network, no API keys. Given a watermark region it inpaints it out with OpenCV
(default) or LaMa (--lama), writes a `_clean` copy next to the source (original untouched),
and emits a tight before/after crop pair for the skill's vision QA. The region is normally
supplied by the skill's vision-locate step as fractions (--region-frac), which is what lets
the same call work across any aspect ratio. A coarse --corner fallback exists for --fast use.

Deps: numpy, opencv-python (cv2), Pillow. Optional: simple-lama-inpainting (for --lama).

Usage:
  python3 remove_watermark.py <image | dir | glob> [options]

Region (first one given wins):
  --region X,Y,W,H        explicit px box; X,Y = top-left
  --region-frac CX,CY,W,H  center+size as fractions of W/H (vision-locate output)
  --corner br|bl|tr|tl     coarse fallback box near a corner (default br)

Mask / inpaint:
  --box-frac F     fallback box edge as fraction of min(W,H)   [0.18]
  --shape S        diamond | box                               [diamond]
  --feather N      dilate mask by N px                         [6]
  --method M       telea | ns  (cv2 algorithm)                 [telea]
  --radius N       cv2 inpaint radius                          [4]
  --lama           use simple-lama-inpainting instead of cv2 (optional dep)

Output:
  --suffix S       output filename suffix                      [_clean]
  --workdir PATH   dir for before/after crops   [/tmp/dewatermark/<stem>/]
  --json           print a machine-readable JSON summary
"""

import argparse
import glob as globmod
import json
import os
import sys

import numpy as np
import cv2
from PIL import Image

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.webp')


def expand_inputs(arg, suffix):
    """Expand a file / dir / glob to image paths, skipping our own `<suffix>` outputs."""
    def keep(p):
        stem, ext = os.path.splitext(os.path.basename(p))
        return ext.lower() in IMG_EXTS and not stem.endswith(suffix)
    if os.path.isdir(arg):
        return [os.path.join(arg, n) for n in sorted(os.listdir(arg))
                if keep(n)]
    if any(ch in arg for ch in '*?['):
        return [p for p in sorted(globmod.glob(arg)) if keep(p)]
    return [arg]


def resolve_box(W, H, args):
    """Return (x0, y0, x1, y1) px box, clamped to the image."""
    if args.region:
        x, y, w, h = (int(v) for v in args.region.split(','))
        x0, y0, x1, y1 = x, y, x + w, y + h
    elif args.region_frac:
        cx, cy, w, h = (float(v) for v in args.region_frac.split(','))
        floor = args.min_frac * min(W, H)   # generous min box absorbs locate error
        bw = max(w * W * args.inflate, floor)
        bh = max(h * H * args.inflate, floor)
        x0 = cx * W - bw / 2
        y0 = cy * H - bh / 2
        x1, y1 = x0 + bw, y0 + bh
    else:
        edge = args.box_frac * min(W, H)
        c = args.box_frac / 2 + 0.03          # center inset from the corner (fraction)
        cx = (1 - c) if 'r' in args.corner else c
        cy = (1 - c) if 'b' in args.corner else c
        x0 = cx * W - edge / 2
        y0 = cy * H - edge / 2
        x1, y1 = x0 + edge, y0 + edge
    x0 = max(0, int(round(x0))); y0 = max(0, int(round(y0)))
    x1 = min(W, int(round(x1))); y1 = min(H, int(round(y1)))
    return x0, y0, x1, y1


def build_mask(W, H, box, shape, feather):
    x0, y0, x1, y1 = box
    mask = np.zeros((H, W), np.uint8)
    if shape == 'diamond':
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        pts = np.array([[cx, y0], [x1, cy], [cx, y1], [x0, cy]], np.int32)
        cv2.fillConvexPoly(mask, pts, 255)
    else:
        mask[y0:y1, x0:x1] = 255
    if feather > 0:
        k = 2 * int(feather) + 1
        mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    return mask


def inpaint_cv2(rgb, mask, method, radius):
    flag = cv2.INPAINT_NS if method == 'ns' else cv2.INPAINT_TELEA
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    out = cv2.inpaint(bgr, mask, radius, flag)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


def inpaint_lama(rgb, mask):
    from simple_lama_inpainting import SimpleLama  # lazy: optional dep
    sl = SimpleLama()
    res = sl(Image.fromarray(rgb), Image.fromarray(mask).convert('L'))
    return np.asarray(res.convert('RGB'))


def process(path, args):
    im = Image.open(path)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    if has_alpha:
        im = im.convert('RGBA')
        arr = np.asarray(im)
        rgb, alpha = arr[:, :, :3].copy(), arr[:, :, 3].copy()
    else:
        im = im.convert('RGB')
        rgb, alpha = np.asarray(im).copy(), None

    H, W = rgb.shape[:2]
    box = resolve_box(W, H, args)
    mask = build_mask(W, H, box, args.shape, args.feather)

    if args.lama:
        cleaned_rgb = inpaint_lama(rgb, mask)
        method = 'lama'
    else:
        cleaned_rgb = inpaint_cv2(rgb, mask, args.method, args.radius)
        method = f'cv2:{args.method}'

    if alpha is not None:
        cleaned = np.dstack([cleaned_rgb, alpha])
        out_im = Image.fromarray(cleaned, 'RGBA')
    else:
        out_im = Image.fromarray(cleaned_rgb, 'RGB')

    stem, _ = os.path.splitext(os.path.basename(path))
    clean_path = os.path.join(os.path.dirname(os.path.abspath(path)),
                              f'{stem}{args.suffix}.png')
    out_im.save(clean_path)

    # before/after crops (region + margin) for the patch-quality QA view
    workdir = args.workdir or os.path.join('/tmp/dewatermark', stem)
    os.makedirs(workdir, exist_ok=True)
    x0, y0, x1, y1 = box
    m = max(20, int(0.4 * max(x1 - x0, y1 - y0)))
    cx0, cy0 = max(0, x0 - m), max(0, y0 - m)
    cx1, cy1 = min(W, x1 + m), min(H, y1 + m)
    before_path = os.path.join(workdir, f'{stem}_wm_before.png')
    after_path = os.path.join(workdir, f'{stem}_wm_after.png')
    Image.fromarray(rgb[cy0:cy1, cx0:cx1]).save(before_path)
    Image.fromarray(cleaned_rgb[cy0:cy1, cx0:cx1]).save(after_path)

    return {
        'source': os.path.abspath(path),
        'clean': clean_path,
        'dims': [W, H],
        'mode': 'RGBA' if alpha is not None else 'RGB',
        'region_px': [x0, y0, x1 - x0, y1 - y0],
        'region_frac': [round((x0 + x1) / 2 / W, 4), round((y0 + y1) / 2 / H, 4),
                        round((x1 - x0) / W, 4), round((y1 - y0) / H, 4)],
        'shape': args.shape,
        'feather': args.feather,
        'inflate': args.inflate,
        'min_frac': args.min_frac,
        'method': method,
        'before_crop': before_path,
        'after_crop': after_path,
    }


def main():
    p = argparse.ArgumentParser(description='Local watermark remover (cv2 / LaMa inpaint)')
    p.add_argument('input', help='image file, directory, or glob')
    p.add_argument('--region')
    p.add_argument('--region-frac', dest='region_frac')
    p.add_argument('--corner', default='br', choices=['br', 'bl', 'tr', 'tl'])
    p.add_argument('--box-frac', type=float, default=0.18)
    p.add_argument('--inflate', type=float, default=1.5,
                   help='scale a --region-frac box around its center to absorb locate error')
    p.add_argument('--min-frac', type=float, default=0.11,
                   help='floor on a --region-frac box edge, as fraction of min(W,H)')
    p.add_argument('--shape', default='box', choices=['diamond', 'box'])
    p.add_argument('--feather', type=int, default=6)
    p.add_argument('--method', default='telea', choices=['telea', 'ns'])
    p.add_argument('--radius', type=int, default=4)
    p.add_argument('--lama', action='store_true')
    p.add_argument('--suffix', default='_clean')
    p.add_argument('--workdir')
    p.add_argument('--json', action='store_true')
    args = p.parse_args()

    paths = expand_inputs(args.input, args.suffix)
    if not paths:
        print(f'ERROR: no images found for: {args.input}')
        sys.exit(1)

    results = []
    for path in paths:
        if not os.path.exists(path):
            print(f'ERROR: not found: {path}', file=sys.stderr)
            continue
        try:
            r = process(path, args)
            results.append(r)
            if not args.json:
                print(f"OK  {os.path.basename(path)}  {r['dims'][0]}x{r['dims'][1]}  "
                      f"region_frac={r['region_frac']}  method={r['method']}")
                print(f"    clean:  {r['clean']}")
                print(f"    crops:  {r['before_crop']} | {r['after_crop']}")
        except Exception as e:
            print(f'ERROR processing {path}: {e}', file=sys.stderr)

    if args.json:
        print(json.dumps({'results': results}, indent=2))
    if not results:
        sys.exit(1)


if __name__ == '__main__':
    main()
