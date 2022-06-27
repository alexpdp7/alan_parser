import typing

import lmparser


class ParagraphBreak(lmparser.LeafSegment):
    pass


class Whitespace(lmparser.LeafSegment):
    pass


class Word(lmparser.LeafSegment):
    pass


class Paragraph(lmparser.ParentSegment):
    pass


class LmTokenizer(lmparser.Parser):
    def parse(self, segment):
        parsed, remaining = segment.parse_re(r"\n( *\n)+", ParagraphBreak)
        if parsed:
            assert remaining  # !!
            return parsed, remaining, self
        parsed, remaining = segment.parse_re(r"\s+", Whitespace)
        if parsed:
            assert remaining  # !!
            return parsed, remaining, self
        parsed, remaining = segment.parse_re(r"\S+", Word)
        if parsed:
            assert remaining  # !!
            return parsed, remaining, self
        assert False, f"unparseable {segment}"


def assemble_tokens(tokens):
    paragraphs = []
    paragraph_tokens = []
    for token in tokens:
        paragraph_tokens.append(token)
        if type(token) == ParagraphBreak:
            paragraphs.append(Paragraph(paragraph_tokens))
            paragraph_tokens = []
    if paragraph_tokens:
        paragraphs.append(Paragraph(paragraph_tokens))
    return paragraphs


def parse_text(text):
    return list(
        map(Paragraph.as_dict, assemble_tokens(lmparser.parse_str(text, LmTokenizer())))
    )
