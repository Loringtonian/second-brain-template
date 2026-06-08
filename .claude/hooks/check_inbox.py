#!/usr/bin/env python3
"""
Inbox check hook for Second Brain.
Runs on first message of session to check a capture inbox (e.g. a phone-sync VM).
"""

import sys
import json
import os
import subprocess
import time

# Session marker file - cleared on reboot
SESSION_MARKER = "/tmp/claude_secondbrain_session_started"
# Endpoint of your capture inbox (e.g. a phone-sync VM on your private network).
INBOX_URL = "http://CAPTURE_VM_HOST:5000/list"  # __FILL_FROM_USER__:capture_inbox_url
# Don't re-check within 5 minutes even if marker cleared
COOLDOWN_SECONDS = 300

def is_first_message():
    """Check if this is the first message of the session."""
    if os.path.exists(SESSION_MARKER):
        # Check if marker is recent (within cooldown period)
        try:
            mtime = os.path.getmtime(SESSION_MARKER)
            if time.time() - mtime < COOLDOWN_SECONDS:
                return False
        except:
            pass
        return False
    return True

def mark_session_started():
    """Create marker file to indicate session has started."""
    try:
        with open(SESSION_MARKER, 'w') as f:
            f.write(str(time.time()))
    except:
        pass

def check_inbox():
    """Check VM inbox for unprocessed items."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--connect-timeout", "3", INBOX_URL],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None, "VM unreachable"

        data = json.loads(result.stdout)
        count = data.get("count", 0)
        files = data.get("files", [])

        return count, files

    except subprocess.TimeoutExpired:
        return None, "VM timeout"
    except json.JSONDecodeError:
        return None, "Invalid response"
    except Exception as e:
        return None, str(e)

def main():
    # Only check on first message of session
    if not is_first_message():
        sys.exit(0)

    # Mark session as started
    mark_session_started()

    # Check inbox
    count, files = check_inbox()

    if count is None:
        # VM issue - don't block, just note it
        sys.exit(0)

    if count == 0:
        # No items - nothing to report
        sys.exit(0)

    # Items found - generate directive
    # Categorize files
    voice_captures = [f for f in files if not f.startswith("images/") and f.endswith(".md")]
    screenshots = [f for f in files if f.startswith("images/") or f.endswith((".jpg", ".png"))]

    directive = f"""<user-prompt-submit-hook>
CAPTURE INBOX CHECK (Session Start)

📥 **{count} items in VM inbox:**
- Voice captures: {len(voice_captures)}
- Screenshots: {len(screenshots) if screenshots else 0}

**Action:** Run your ingestion skill (e.g. `/ingest-example`) to review and process these items.
Do NOT process manually - use the skill which has the proper approval workflow.

Files: {', '.join(voice_captures[:5])}{'...' if len(voice_captures) > 5 else ''}
</user-prompt-submit-hook>"""

    print(directive)
    sys.exit(0)

if __name__ == "__main__":
    main()
