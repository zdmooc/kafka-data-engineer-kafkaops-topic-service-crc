from __future__ import annotations

import re
from typing import Dict, List, Tuple


class GovernanceError(ValueError):
    pass


class Governance:
    def __init__(self, topic_name_regex: str, required_labels: List[str]) -> None:
        self._re = re.compile(topic_name_regex)
        self._required_labels = required_labels

    def validate_topic(self, name: str, labels: Dict[str, str]) -> None:
        if not self._re.match(name):
            raise GovernanceError(
                f"Topic name '{name}' does not match policy regex: {self._re.pattern}"
            )
        missing = [k for k in self._required_labels if k not in labels or not str(labels[k]).strip()]
        if missing:
            raise GovernanceError(f"Missing required labels: {', '.join(missing)}")
