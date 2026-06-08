"""
Canonical timezone helper for your Second Brain.

Use ONE timezone for every timestamp so they sort and compare cleanly. Set yours via the
`SECOND_BRAIN_TZ` environment variable (an IANA name like "America/New_York" or "Europe/Berlin");
it defaults to UTC. Import `now()` from here instead of calling `datetime.now()` directly.

Usage:
    from tz import now, TIMEZONE
    timestamp = now().isoformat(timespec='seconds')
    formatted = now().strftime('%Y-%m-%d %H:%M:%S %Z')
"""

import os
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9
    ZoneInfo = None

# SECOND_BRAIN_TZ — your timezone (see .env.example). __FILL_FROM_USER__:timezone
_TZ_NAME = os.environ.get("SECOND_BRAIN_TZ", "UTC")

try:
    TIMEZONE = ZoneInfo(_TZ_NAME) if ZoneInfo else timezone.utc
except Exception:
    TIMEZONE = timezone.utc


def now() -> datetime:
    """Return the current time in your configured timezone (SECOND_BRAIN_TZ, default UTC)."""
    return datetime.now(TIMEZONE)
