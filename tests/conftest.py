import nltk


def pytest_sessionstart():
    print("downloading NLTK ressources")
    nltk.download("punkt")
