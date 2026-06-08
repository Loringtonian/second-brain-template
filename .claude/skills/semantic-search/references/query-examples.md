# Query Examples

Common search patterns for semantic search.

## Conceptual Searches

```bash
# Broad topics
python3 scripts/sb_embed.py search "artificial intelligence governance"
python3 scripts/sb_embed.py search "coordination problems and solutions"
python3 scripts/sb_embed.py search "longevity and health optimization"

# Themes
python3 scripts/sb_embed.py search "long-term thinking frameworks"
python3 scripts/sb_embed.py search "personal development strategies"
python3 scripts/sb_embed.py search "shipping imperfect products"
```

## Project-Filtered Searches

```bash
# A sci-fi writing project
python3 scripts/sb_embed.py search "AI story concept" --project "__FILL_FROM_USER__:scifi_project_name"

# A governance/coordination project
python3 scripts/sb_embed.py search "governance algorithm" --project "__FILL_FROM_USER__:governance_project_name"

# A capture/inbox project
python3 scripts/sb_embed.py search "mobile capture workflow" --project "__FILL_FROM_USER__:capture_project_name"
```

## Category-Filtered Searches

```bash
# Intellectual journal
python3 scripts/sb_embed.py search "philosophy of AI" --category "Journal - Intellectual"

# Inventions
python3 scripts/sb_embed.py search "app idea" --category "Inventions"

# Predictions
python3 scripts/sb_embed.py search "technology forecast" --category "Predictions"
```

## Duplicate Detection

```bash
# Before creating a new file
python3 scripts/sb_embed.py verify "The key insight is that AI governance needs to be decentralized"

# Check longer text
python3 scripts/sb_embed.py verify "$(cat draft_idea.md)"
```

## Finding Similar Files

```bash
# Find ideas related to an existing file
python3 scripts/sb_embed.py similar "Journal_Intellectual/coordination_theory.md"

# With more results
python3 scripts/sb_embed.py similar "path/to/file.md" --top-k 10
```

## JSON Output for Scripting

```bash
# Get structured output
result=$(python3 scripts/sb_embed.py search "query" --json)

# Parse with jq
python3 scripts/sb_embed.py search "query" --json | jq '.results[].filepath'

# Get top match
python3 scripts/sb_embed.py search "query" --json | jq -r '.results[0].filepath'
```
