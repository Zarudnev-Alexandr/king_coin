from typing import Any, Optional


def id_check(text: Any) -> str:
    if 0 <= len(text) <= 99999:
        return text
    raise ValueError


def descr_check(text: Any) -> Optional[Any]:
    if 1 <= len(text) <= 500:
        if text == 'пропустить':
            return None
        else:
            return text
    raise ValueError


