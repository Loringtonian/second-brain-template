# Connection Finder Settings

Configuration for the connection-finder skill. Edit this file to adjust behavior.

---

## Sensitivity Level

**Current: AGGRESSIVE**

### Options

| Level           | Behavior                                                                                      |
|-----------------|-----------------------------------------------------------------------------------------------|
| **AGGRESSIVE**  | Activate on any concept/idea discussion. More proactive, may surface connections unprompted.  |
| **MODERATE**    | Activate only when multiple keywords match or during explicit exploration/brainstorming.       |
| **CONSERVATIVE**| Activate only on explicit request or very strong keyword matches. Minimal unprompted suggestions.|

### Changing Sensitivity

To change, update the "Current" value above. The skill reads this file and adjusts immediately.

---

## Output Format

**Current: BRIEF**

### Options

| Format   | Behavior                                                          |
|----------|-------------------------------------------------------------------|
| **BRIEF**| 2–3 sentences per suggestion. Quick hits. Expand on request.     |
| **FULL** | Comprehensive context for each connection. More detail upfront.   |

---

## Feedback Tracking

The skill monitors for rejection signals to self-calibrate.

### Rejection Signals
- "That's not relevant"
- "Not a good connection"
- "That's a stretch"
- Owner ignores/dismisses the suggestion

### Self-Adjustment Trigger

After **3+ rejections** in a single session, the skill will proactively ask:

> "I've noticed a few of my connection suggestions weren't hitting the mark. Would you like me to dial back the sensitivity?"

### Session Reset

Rejection count resets at the start of each new conversation.

---

## Search Scope

**Current: STANDARD**

### Options

| Scope        | Searches                                                                     |
|--------------|------------------------------------------------------------------------------|
| **MINIMAL**  | Core idea folders only (Journal_Intellectual/, Inventions/, Projects/)       |
| **STANDARD** | All primary folders + KEYWORD_GUIDE.md vocabulary matching                   |
| **DEEP**     | All folders including External_Sources/ (slower, more comprehensive)         |

---

## Maximum Connections

**Current: 3**

Maximum connections surfaced per activation. Increase for more suggestions; decrease for fewer.

---

## Change Log

| Date       | Change                          | Reason                    |
|------------|---------------------------------|---------------------------|
| 2025-12-16 | Initial settings                | Skill created             |
| 2025-12-30 | Updated search scope            | Migrated to grep-based    |
