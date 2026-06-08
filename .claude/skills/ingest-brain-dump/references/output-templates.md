# Output Templates

## Approval Proposal Format

Present to user for approval:

```markdown
## Brain Dump Ingestion Proposal

**Source:** [description/date]
**Ideas Identified:** [count]

### New Files (Approve Creation):

1. [NEW_IDEA] Create: Second_Brain/[Category]/[Title].md
   Keywords: [list]
   Projects: [list]
   → [Y/N]

### Augmentations:

2. [AUGMENT] Add to: [existing file path]
   Content: [brief summary]
   → [Y/N]

### Direct Additions (Already Done):

3. [TODO] Added to [TODO file]
4. [READING_LIST] Added to AA_Lists/READING_LIST.md

### Logged Only:

5. [QUESTION] "[question]" - Not stored
```

## User Response Options

- `Y` or `Yes` - Approve
- `N` or `No` - Reject
- `Modify: [instructions]` - Adjust and re-present

## Completion Summary Format

After execution:

```markdown
## Brain Dump Ingestion Complete

**Source:** [description]
**Ideas Processed:** [count]

### Actions Taken:
- Created: [list files]
- Augmented: [list files]
- TODOs added: [count]
- Skipped: [count] (rejected/duplicate)

### Verification:
- All files passed template validation
```

## Verification Output

After creating files, run validation:

```bash
python3 .claude/scripts/validate_template.py "[filepath]"
```

Expected output for valid file:
```
✓ VALID - Template A
File: [path]
Sections found: 8
```
