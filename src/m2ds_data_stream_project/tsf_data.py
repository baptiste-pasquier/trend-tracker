import re

import contractions
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def get_wordnet_pos(tag):
    """
    TO DOCUMENT
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


def text_cleaning(tweet, negation_set, fg_stop_words=False, fg_lemmatization=False):
    """
    Clean/Transform the text of a tweet

    Arguments
    ---------------------------
        tweet(<str>): String to clean
        fg_stop_words (<bool>): Remove or not stop words
        fg_lemmatization (<bool>): Apply or not lemmatization


    Returns
    ---------------------------
        tweet(<str>): Tokenized text
        mentions (<list>): List of mentionned users in the tweet (@'s)
        hashtags (<list>): List of hashtags in the tweets (#'s)
    """

    # lowercase
    tweet = tweet.lower()

    # remove extra newlines
    tweet = re.sub(r"[\r|\n|\r\n]+", "", tweet)

    # remove URL
    tweet = re.sub(r"https?://[\S]+", "", tweet)

    # Extract @tag and #tag
    mentions = re.findall(r"@(\w+)", tweet)
    hashtags = re.findall(r"#(\w+)", tweet)
    # Remove them and special chars
    tweet = re.sub("[^A-Za-z0-9]+", " ", tweet)

    # remove contractions
    tweet = " ".join([contractions.fix(x) for x in tweet.split()])

    # tokenization
    tweet = word_tokenize(tweet)

    if fg_stop_words:
        # remove stop words
        stop_words = set(stopwords.words("english")).difference(negation_set)
        tweet = [word for word in tweet if word not in stop_words]

    if fg_lemmatization:
        # lemmatization
        tweet = nltk.tag.pos_tag(tweet)
        tweet = [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in tweet]
        wordnet_lemmatizer = WordNetLemmatizer()
        tweet = [wordnet_lemmatizer.lemmatize(word, tag) for (word, tag) in tweet]

    return " ".join(tweet), mentions, hashtags
