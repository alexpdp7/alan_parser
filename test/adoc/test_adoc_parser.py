import dataclasses
import re
import textwrap
import typing

import alanp


class HeaderToken(alanp.Token):
    pass


class TextToken(alanp.Token):
    pass


class NewLineToken(alanp.Token):
    pass


class ZeroParser(alanp.TokenParser):
    def parse(self, text: str):
        if text.startswith("="):
            match = re.match("=+ ", text)
            return (HeaderToken(match.group()), TextLineParser())
        if text.startswith("\n"):
            return (NewLineToken("\n"), ZeroParser())
        return TextLineParser().parse(text)


class TextLineParser(alanp.TokenParser):
    def parse(self, text: str):
        line = text.split("\n")[0]
        return (TextToken(line), ZeroParser())


@dataclasses.dataclass
class HeaderBlock:
    header_token: alanp.ParsedToken
    text_token: alanp.ParsedToken


@dataclasses.dataclass
class ParagraphBlock:
    tokens: typing.List[alanp.ParsedToken]


def make_blocks(text):
    parse_token_state = alanp.ParseTokenState(ZeroParser(), text, 0)
    while True:
        (parsed_token, parse_token_state) = parse_token_state.parse()

        if isinstance(parsed_token.token, NewLineToken):
            continue

        if isinstance(parsed_token.token, HeaderToken):
            header_token = parsed_token
            (parsed_token, parse_token_state) = parse_token_state.parse()
            assert isinstance(parsed_token.token, TextToken)
            text_token = parsed_token
            (parsed_token, parse_token_state) = parse_token_state.parse()
            assert isinstance(parsed_token.token, NewLineToken) or isinstance(
                parsed_token.token, alanp.EofToken
            )
            yield HeaderBlock(header_token, text_token)
            continue

        if isinstance(parsed_token.token, TextToken):
            paragraph = [parsed_token]
            while True:
                (parsed_token, parse_token_state) = parse_token_state.parse()
                if isinstance(parsed_token.token, NewLineToken) or isinstance(
                    parsed_token.token, TextToken
                ):
                    paragraph.append(parsed_token)
                if isinstance(parsed_token.token, alanp.EofToken) or (
                    len(paragraph) >= 2
                    and isinstance(paragraph[-2].token, NewLineToken)
                    and isinstance(paragraph[-1].token, NewLineToken)
                ):
                    yield ParagraphBlock(paragraph)
                    if isinstance(parsed_token.token, alanp.EofToken):
                        return
                    break


def _adoc(adoc):
    return textwrap.dedent(adoc)


simple = _adoc(
    """\
= Foo

Bar
"""
)


def test_tokenize_simple():
    tokens = list(
        alanp.tokenize(
            simple,
            ZeroParser(),
        )
    )
    assert tokens == [
        alanp.ParsedToken(pos=0, token=HeaderToken(text="= ")),
        alanp.ParsedToken(pos=2, token=TextToken(text="Foo")),
        alanp.ParsedToken(pos=5, token=NewLineToken(text="\n")),
        alanp.ParsedToken(pos=6, token=NewLineToken(text="\n")),
        alanp.ParsedToken(pos=7, token=TextToken(text="Bar")),
        alanp.ParsedToken(pos=10, token=NewLineToken(text="\n")),
        alanp.ParsedToken(pos=11, token=alanp.EofToken(text="")),
    ]


def test_make_blocks_simple():
    blocks = list(make_blocks(simple))
    assert blocks == [
        HeaderBlock(
            header_token=alanp.ParsedToken(pos=0, token=HeaderToken(text="= ")),
            text_token=alanp.ParsedToken(pos=2, token=TextToken(text="Foo")),
        ),
        ParagraphBlock(
            tokens=[
                alanp.ParsedToken(pos=7, token=TextToken(text="Bar")),
                alanp.ParsedToken(pos=10, token=NewLineToken(text="\n")),
            ]
        ),
    ]
