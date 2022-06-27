from lmparser.samples import lm


def test_single_word_paragraph():
    assert [
        {
            "children": [{"end": 6, "start": 0, "text": "Single", "type": "Word"}],
            "type": "Paragraph",
        }
    ] == lm.parse_text("Single")


def test_multi_word_paragraph():
    assert [
        {
            "type": "Paragraph",
            "children": [
                {"type": "Word", "text": "This", "start": 0, "end": 4},
                {"type": "Whitespace", "text": " ", "start": 4, "end": 5},
                {"type": "Word", "text": "is", "start": 5, "end": 7},
                {"type": "Whitespace", "text": " ", "start": 7, "end": 8},
                {"type": "Word", "text": "a", "start": 8, "end": 9},
                {"type": "Whitespace", "text": " ", "start": 9, "end": 10},
                {"type": "Word", "text": "sentence.", "start": 10, "end": 19},
            ],
        }
    ] == lm.parse_text("This is a sentence.")


def test_multi_line_paragraph():
    assert [
        {
            "type": "Paragraph",
            "children": [
                {"type": "Word", "text": "This", "start": 0, "end": 4},
                {"type": "Whitespace", "text": " ", "start": 4, "end": 5},
                {"type": "Word", "text": "is", "start": 5, "end": 7},
                {"type": "Whitespace", "text": " ", "start": 7, "end": 8},
                {"type": "Word", "text": "a", "start": 8, "end": 9},
                {"type": "Whitespace", "text": " ", "start": 9, "end": 10},
                {"type": "Word", "text": "sentence.", "start": 10, "end": 19},
                {"type": "Whitespace", "text": "\n", "start": 19, "end": 20},
                {"type": "Word", "text": "Sentence", "start": 20, "end": 28},
                {"type": "Whitespace", "text": " ", "start": 28, "end": 29},
                {"type": "Word", "text": "in", "start": 29, "end": 31},
                {"type": "Whitespace", "text": " ", "start": 31, "end": 32},
                {"type": "Word", "text": "same", "start": 32, "end": 36},
                {"type": "Whitespace", "text": " ", "start": 36, "end": 37},
                {"type": "Word", "text": "paragraph", "start": 37, "end": 46},
            ],
        }
    ] == lm.parse_text("This is a sentence.\nSentence in same paragraph")


def test_two_paragraphs():
    assert [
        {
            "type": "Paragraph",
            "children": [
                {"type": "Word", "text": "This", "start": 0, "end": 4},
                {"type": "Whitespace", "text": " ", "start": 4, "end": 5},
                {"type": "Word", "text": "is", "start": 5, "end": 7},
                {"type": "Whitespace", "text": " ", "start": 7, "end": 8},
                {"type": "Word", "text": "a", "start": 8, "end": 9},
                {"type": "Whitespace", "text": " ", "start": 9, "end": 10},
                {"type": "Word", "text": "sentence.", "start": 10, "end": 19},
                {"type": "ParagraphBreak", "text": "\n\n", "start": 19, "end": 21},
            ],
        },
        {
            "type": "Paragraph",
            "children": [
                {"type": "Word", "text": "New", "start": 21, "end": 24},
                {"type": "Whitespace", "text": " ", "start": 24, "end": 25},
                {"type": "Word", "text": "paragraph", "start": 25, "end": 34},
            ],
        },
    ] == lm.parse_text("This is a sentence.\n\nNew paragraph")
