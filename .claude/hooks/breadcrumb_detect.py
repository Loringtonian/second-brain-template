#!/usr/bin/env python3
"""Detect 'breadcrumb' keyword in user prompt and emit skill directive."""
import sys, json, re

input_data = json.load(sys.stdin)
prompt = input_data.get("prompt", "")

# Meta-escape: suppress when user is talking ABOUT the breadcrumb system
# "the breadcrumb" is always meta — actual requests say "breadcrumb this" or "leave breadcrumbs"
META_ESCAPE = re.compile(
    r'\bthe\s+breadcrumbs?\b|'
    r'breadcrumbs?.{0,15}(hook|skill|detect|system|script|setting|fire|trigger)\b|'
    r'(fix|update|modify|implement|change|test|debug|check).{0,30}\bbreadcrumbs?\b|'
    r'\bbreadcrumb_detect\b',
    re.IGNORECASE
)

if META_ESCAPE.search(prompt):
    sys.exit(0)  # Silent — meta discussion, not a breadcrumb request

# Match "breadcrumb" as a word boundary (case-insensitive)
# Also match trigger phrases from the skill
TRIGGERS = re.compile(
    r'\bbreadcrumbs?\b|'
    r'\bregister this\b|'
    r'\badd.{0,10}toolkit\b|'
    r'\bremember this tool\b|'
    r'\bmake.{0,20}future instances.{0,10}(know|aware)\b',
    re.IGNORECASE
)

if TRIGGERS.search(prompt):
    print("""<user-prompt-submit-hook>
BREADCRUMB DETECTED

Invoke /breadcrumb skill. The user wants to register a capability, tool, pattern,
or gotcha so future Claude instances can find it. Extract what they discovered
from their message and place it in the right discovery layer.
</user-prompt-submit-hook>""")
