import unicodedata
import re

# Char to remove
REMOVABLE_CHARS = '!"#$%&*+,;<=>?@[\\]^`{|}~_.:/()-ø\' '


def _remove_html(raw_html):
    cleaner_regexp = re.compile("<.*?>")
    clean_text = re.sub(cleaner_regexp, "", raw_html)

    clean_text = clean_text.replace("&amp;", "&")
    clean_text = clean_text.replace("&nbsp;", " ")
    return clean_text


def _remove_accents(raw_text):
    # Replace accented characters by unaccented ones
    clean_text = "".join(
        (
            c
            for c in unicodedata.normalize("NFD", raw_text)
            if unicodedata.category(c) != "Mn"
        )
    )
    return clean_text


def normalise(raw_text):
    transform = _remove_accents(raw_text)
    transform = transform.strip()

    # Replace special characters with _
    transform = transform.translate(
        transform.maketrans(REMOVABLE_CHARS, "_" * len(REMOVABLE_CHARS))
    )

    return transform
