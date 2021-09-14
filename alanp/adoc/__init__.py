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


class ConditionalDirectiveToken(alanp.Token):
    pass


class ConditionalDirectiveStartToken(alanp.Token):
    pass


class ConditionalDirectiveEndToken(alanp.Token):
    pass


class CommaToken(alanp.Token):
    pass


class PlusToken(alanp.Token):
    pass


class AttributeToken(alanp.Token):
    pass


class ZeroParser(alanp.TokenParser):
    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        match = re.match("ifn?def::", text)
        if match:
            return (
                ConditionalDirectiveToken(match.group()),
                ConditionalDirectiveParser(),
            )

        if text.startswith("="):
            match = re.match("=+ ", text)
            assert match
            return (HeaderToken(match.group()), DelimitedTextParser("\n", self))
        if text.startswith("\n"):
            return (NewLineToken("\n"), ZeroParser())
        return DelimitedTextParser("\n", self).parse(text)


class DelimitedTextParser(alanp.TokenParser):
    def __init__(self, delimiter: str, next_parser: alanp.TokenParser):
        self.delimiter = delimiter
        self.next_parser = next_parser

    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        line = text.split(self.delimiter)[0]
        return (TextToken(line), self.next_parser)


class ConditionalDirectiveParser(alanp.TokenParser):
    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        if text.startswith("[]"):
            assert False, "not implemented yet"
        if text.startswith("["):
            return (ConditionalDirectiveStartToken("["), DelimitedTextParser("]", self))
        if text.startswith("]\n"):
            return (ConditionalDirectiveEndToken("]\n"), ZeroParser())
        if text.startswith(","):
            return (CommaToken(","), self)
        if text.startswith("+"):
            return (CommaToken("+"), self)
        end = re.search("[[,+]", text)
        assert end
        return (AttributeToken(text[0 : end.start()]), self)


@dataclasses.dataclass
class Block:
    pass


@dataclasses.dataclass
class HeaderBlock(Block):
    header_token: alanp.ParsedToken
    text_token: alanp.ParsedToken


@dataclasses.dataclass
class ParagraphBlock(Block):
    tokens: typing.List[alanp.ParsedToken]
    condition: typing.Optional[typing.List[alanp.ParsedToken]] = None


def make_blocks(text: str) -> typing.Generator[Block, None, None]:
    parse_token_state: typing.Optional[alanp.ParseTokenState] = alanp.ParseTokenState(
        ZeroParser(), text, 0
    )
    while True:
        assert parse_token_state
        (parsed_token, parse_token_state) = parse_token_state.parse()

        if isinstance(parsed_token.token, alanp.EofToken):
            return

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
            yield HeaderBlock(header_token=header_token, text_token=text_token)
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
                    yield ParagraphBlock(tokens=paragraph)
                    if isinstance(parsed_token.token, alanp.EofToken):
                        return
                    break

        if isinstance(parsed_token.token, ConditionalDirectiveToken):
            attribute_tokens = [parsed_token]

            while True:
                assert parse_token_state
                (parsed_token, parse_token_state) = parse_token_state.parse()
                assert parse_token_state
                if isinstance(parsed_token.token, ConditionalDirectiveStartToken):
                    break
                assert (
                    isinstance(parsed_token.token, AttributeToken)
                    or isinstance(parsed_token.token, CommaToken)
                    or isinstance(parsed_token.token, PlusToken)
                )
                attribute_tokens.append(parsed_token)

            (parsed_token, parse_token_state) = parse_token_state.parse()
            assert parse_token_state

            yield ParagraphBlock(tokens=[parsed_token], condition=attribute_tokens)

            (parsed_token, parse_token_state) = parse_token_state.parse()
            assert parse_token_state
            assert isinstance(parsed_token.token, ConditionalDirectiveEndToken)
