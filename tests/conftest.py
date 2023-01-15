import nltk


def pytest_sessionstart():
    """Download NLTK ressources before testing."""
    print("downloading NLTK ressources")
    nltk.download("punkt")
