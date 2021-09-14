import dataclasses
import re
import typing

import alanp


class HeaderToken(alanp.Token):
    pass


class TextToken(alanp.Token):
    pass


class NewLineToken(alanp.Token):
    pass


class ZeroParser(alanp.TokenParser):
    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        if text.startswith("="):
            match = re.match("=+ ", text)
            assert match
            return (HeaderToken(match.group()), TextLineParser())
        if text.startswith("\n"):
            return (NewLineToken("\n"), ZeroParser())
        return TextLineParser().parse(text)


class TextLineParser(alanp.TokenParser):
    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        line = text.split("\n")[0]
        return (TextToken(line), ZeroParser())


class Block:
    pass


@dataclasses.dataclass
class HeaderBlock(Block):
    header_token: alanp.ParsedToken
    text_token: alanp.ParsedToken


@dataclasses.dataclass
class ParagraphBlock(Block):
    tokens: typing.List[alanp.ParsedToken]


def make_blocks(text: str) -> typing.Generator[Block, None, None]:
    parse_token_state: typing.Optional[alanp.ParseTokenState] = alanp.ParseTokenState(
        ZeroParser(), text, 0
    )
    while True:
        assert parse_token_state
        (parsed_token, parse_token_state) = parse_token_state.parse()

        if isinstance(parsed_token.token, NewLineToken):
            continue

        assert parse_token_state

        if isinstance(parsed_token.token, HeaderToken):
            header_token = parsed_token
            (parsed_token, parse_token_state) = parse_token_state.parse()
            assert isinstance(parsed_token.token, TextToken)
            assert parse_token_state
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
                assert parse_token_state
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
