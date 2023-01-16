from trend_tracker.tsf_data import text_cleaning


def test_text_cleaning_lowercase():
    tweet, _, _ = text_cleaning("great Day remember YOU", set())
    assert tweet == "great day remember you"


def test_text_cleaning_newlines():
    tweet, _, _ = text_cleaning(
        """great day
    remember you do not have permission
    to do anything""",
        set(),
    )
    assert tweet == "great day remember you do not have permission to do anything"

    tweet, _, _ = text_cleaning("great day\n\nremember you", set())
    assert tweet == "great day remember you"

    tweet, _, _ = text_cleaning("great day\rremember you", set())
    assert tweet == "great day remember you"

    tweet, _, _ = text_cleaning("great day\r\nremember you", set())
    assert tweet == "great day remember you"


def test_text_cleaning_URL():
    tweet, _, _ = text_cleaning("great day https://www.google.com/", set())
    assert tweet == "great day"

    tweet, _, _ = text_cleaning("https://www.google.com/ great day", set())
    assert tweet == "great day"

    tweet, _, _ = text_cleaning("great https://www.google.com/ day", set())
    assert tweet == "great day"


def test_text_cleaning_extract_tag():
    tweet, mentions, hashtags = text_cleaning(
        "@tag1 great @tag2\nday @tag3-remember", set()
    )
    assert tweet == "tag1 great tag2 day tag3 remember"
    assert mentions == ["tag1", "tag2", "tag3"]
    assert hashtags == []

    tweet, mentions, hashtags = text_cleaning(
        "#tag1 great #tag2\nday #tag3-remember", set()
    )
    assert tweet == "tag1 great tag2 day tag3 remember"
    assert mentions == []
    assert hashtags == ["tag1", "tag2", "tag3"]

    tweet, mentions, hashtags = text_cleaning(
        "@tag1 great #tag2 day @tag3 remember #tag4", set()
    )
    assert tweet == "tag1 great tag2 day tag3 remember tag4"
    assert mentions == ["tag1", "tag3"]
    assert hashtags == ["tag2", "tag4"]


def test_text_cleaning_contractions():
    tweet, _, _ = text_cleaning(
        "great day remember you don't have permission because I'm", set()
    )
    assert tweet == "great day remember you do not have permission because i am"


def test_text_cleaning_special_chars():
    tweet, _, _ = text_cleaning(
        "@tag1 great #tag2 day - remember.!  you à é_do.", set()
    )
    assert tweet == "tag1 great tag2 day remember you à é do"
