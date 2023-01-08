from __future__ import annotations

import re

import contractions
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def get_wordnet_pos(tag: str) -> str:
    """_summary_
    TODO docstring

    Parameters
    ----------
    tag : str
        _description_

    Returns
    -------
    str
        _description_
    """
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def text_cleaning(
    corpus: str,
    negation_set: set[str],
    fg_stop_words: bool = False,
    fg_lemmatization: bool = False,
) -> tuple[str, list[str], list[str]]:
    """Text cleaning of a corpus and extraction of mentions and hashtags

    Parameters
    ----------
    corpus : str
        String to clean
    negation_set : set[str]
        Negation words
    fg_stop_words : bool, optional
        Remove or not stop words, by default False
    fg_lemmatization : bool, optional
        Apply or not lemmatization, by default False

    Returns
    -------
    tuple[str, list[str], list[str]]
        corpus : Cleaned string
        mentions : List of mentionned users in the corpus (@'s)
        hashtags : List of hashtags in the corpuss (#'s)
    """

    # lowercase
    corpus = corpus.lower()

    # remove extra newlines
    corpus = re.sub(r"[\r|\n|\r\n]+", " ", corpus)

    # remove URL
    corpus = re.sub(r"https?://[\S]+", "", corpus)

    # Extract @tag and #tag
    mentions = re.findall(r"@(\w+)", corpus)
    hashtags = re.findall(r"#(\w+)", corpus)

    # remove contractions
    corpus = " ".join([contractions.fix(x) for x in corpus.split()])

    # Remove @ # and any special chars
    corpus = re.sub(r"[\W_]+", " ", corpus)

    # tokenization
    corpus_words = word_tokenize(corpus)

    if fg_stop_words:
        # remove stop words
        stop_words = set(stopwords.words("english")).difference(negation_set)
        corpus_words = [word for word in corpus_words if word not in stop_words]

    if fg_lemmatization:
        # lemmatization
        corpus_pos_tag = nltk.tag.pos_tag(corpus_words)
        corpus_pos_tag = [
            (word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in corpus_pos_tag
        ]
        wordnet_lemmatizer = WordNetLemmatizer()
        corpus_words = [
            wordnet_lemmatizer.lemmatize(word, tag) for (word, tag) in corpus_pos_tag
        ]

    return " ".join(corpus_words), mentions, hashtags
