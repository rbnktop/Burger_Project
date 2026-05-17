import re
from semantic_release.commit_parser import ParsedCommit
from semantic_release.enums import LevelBump
from semantic_release.git_helpers import Commit

def fallback_parser(commit: Commit):
    message = commit.message.strip().split("\n")[0]

    # 1. First, check if it already matches a strict conventional commit format
    match = re.match(r"^(\w+)(?:\(([^)]+)\))?!?: (.+)$", message)
    if match:
        commit_type, scope, text = match.groups()
        bump = LevelBump.NO_RELEASE
        if commit_type == "feat":
            bump = LevelBump.MINOR
        elif commit_type == "fix":
            bump = LevelBump.PATCH

        return ParsedCommit(
            bump=bump,
            type=commit_type,
            scope=scope or "",
            descriptions=[text],
            breaking="!" in message or "BREAKING CHANGE" in commit.message,
            commit=commit
        )

    # 2. Fallback rules for legacy/informal commits
    lower_msg = message.lower()

    if any(x in lower_msg for x in ["fix", "glitch", "bug", "hiccup"]):
        commit_type = "fix"
        bump = LevelBump.PATCH
    elif any(x in lower_msg for x in ["feat", "add", "implement", "organize"]):
        commit_type = "feat"
        bump = LevelBump.MINOR
    else:
        commit_type = "chore"
        bump = LevelBump.NO_RELEASE

    return ParsedCommit(
        bump=bump,
        type=commit_type,
        scope="legacy",
        descriptions=[message],
        breaking=False,
        commit=commit
    )