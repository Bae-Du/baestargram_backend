import re
import unicodedata

from fastapi import HTTPException, status

PROFANITY_MESSAGE = "비속어는 사용할 수 없어요."

_ENGLISH_WORDS = frozenset(
    {
        "asshole",
        "bastard",
        "bitch",
        "bollocks",
        "cock",
        "cunt",
        "dick",
        "dumbass",
        "faggot",
        "fuck",
        "fucked",
        "fucker",
        "fucking",
        "motherfucker",
        "nigga",
        "nigger",
        "piss",
        "pussy",
        "shit",
        "slut",
        "whore",
    }
)

_KOREAN_WORDS = frozenset(
    {
        "개같",
        "개놈",
        "개년",
        "개새끼",
        "개색기",
        "개색히",
        "개소리",
        "꺼져",
        "닥쳐",
        "느금마",
        "니미",
        "니애미",
        "미친놈",
        "미친년",
        "병신",
        "븅신",
        "보지련",
        "빠구리",
        "빨아",
        "ㅅㅂ",
        "시발",
        "시바",
        "시벌",
        "시팔",
        "ㅆㅂ",
        "씨발",
        "씨바",
        "씨벌",
        "씨팔",
        "쌍놈",
        "쌍년",
        "씹",
        "염병",
        "앰창",
        "애미",
        "애비",
        "ㅈㄹ",
        "자지련",
        "좆",
        "존나",
        "졸라",
        "지랄",
        "창녀",
        "창년",
        "후장",
    }
)

_LEET = str.maketrans(
    {
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "@": "a",
        "$": "s",
        "*": "",
    }
)

_ENGLISH_WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(word) for word in sorted(_ENGLISH_WORDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)


def _normalize(text: str) -> str:
    compact = unicodedata.normalize("NFKC", text).lower().translate(_LEET)
    return re.sub(r"[^a-z0-9가-힣ㄱ-ㅎㅏ-ㅣ]", "", compact)


def contains_profanity(text: str | None) -> bool:
    if not text:
        return False

    if _ENGLISH_WORD_RE.search(text):
        return True

    compact = _normalize(text)
    if not compact:
        return False

    for word in _KOREAN_WORDS:
        if word in compact:
            return True

    for word in _ENGLISH_WORDS:
        if len(word) >= 4 and word in compact:
            return True

    return False


def reject_if_profane(*texts: str | None) -> None:
    if any(contains_profanity(text) for text in texts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROFANITY_MESSAGE,
        )
