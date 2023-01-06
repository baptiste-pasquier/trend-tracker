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
    tweet: str,
    negation_set: set[str],
    fg_stop_words: bool = False,
    fg_lemmatization: bool = False,
) -> tuple[str, list[str], list[str]]:
    """Text cleaning of a tweet and extraction of mentions and hashtags

    Parameters
    ----------
    tweet : str
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
        tweet : Cleaned string
        mentions : List of mentionned users in the tweet (@'s)
        hashtags : List of hashtags in the tweets (#'s)
    """

    # lowercase
    tweet = tweet.lower()

    # remove extra newlines
    tweet = re.sub(r"[\r|\n|\r\n]+", " ", tweet)

    # remove URL
    tweet = re.sub(r"https?://[\S]+", "", tweet)

    # Extract @tag and #tag
    mentions = re.findall(r"@(\w+)", tweet)
    hashtags = re.findall(r"#(\w+)", tweet)

    # remove contractions
    tweet = " ".join([contractions.fix(x) for x in tweet.split()])

    # Remove @ # and any special chars
    tweet = re.sub(r"[\W_]+", " ", tweet)

    # tokenization
    tweet_words = word_tokenize(tweet)

    if fg_stop_words:
        # remove stop words
        stop_words = set(stopwords.words("english")).difference(negation_set)
        tweet_words = [word for word in tweet_words if word not in stop_words]

    if fg_lemmatization:
        # lemmatization
        tweet_pos_tag = nltk.tag.pos_tag(tweet_words)
        tweet_pos_tag = [
            (word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in tweet_pos_tag
        ]
        wordnet_lemmatizer = WordNetLemmatizer()
        tweet_words = [
            wordnet_lemmatizer.lemmatize(word, tag) for (word, tag) in tweet_pos_tag
        ]

    return " ".join(tweet_words), mentions, hashtags
