from utils.summarizer import limit_words, word_count


def test_limit_words_max_500():
    text = "word " * 600
    result = limit_words(text, 500)

    assert len(result.split()) == 500


def test_limit_words_less_than_500():
    text = "word " * 100
    result = limit_words(text, 500)

    assert len(result.split()) == 100


def test_word_count():
    text = "Hello world test case"
    assert word_count(text) == 4


def test_limit_words_returns_string():
    text = "hello world"
    result = limit_words(text, 500)

    assert isinstance(result, str)