import abc
import dataclasses
import typing


@dataclasses.dataclass
class Token:
    text: str


class EofToken(Token):
    pass


@dataclasses.dataclass
class ParsedToken:
    pos: int
    token: Token


class TokenParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, text) -> typing.Tuple[Token, "TokenParser"]:
        pass


@dataclasses.dataclass
class ParseTokenState:
    token_parser: TokenParser
    text: str
    pos: int = 0

    def parse(self) -> typing.Tuple[ParsedToken, typing.Optional["ParseTokenState"]]:
        assert self.pos <= len(self.text)
        if self.pos == len(self.text):
            return (ParsedToken(self.pos, EofToken("")), None)
        (token, next_token_parser) = self.token_parser.parse(self.text[self.pos :])
        parsed_token = ParsedToken(self.pos, token)
        new_parse_token_state = ParseTokenState(
            next_token_parser, self.text, self.pos + len(token.text)
        )
        return (parsed_token, new_parse_token_state)


def tokenize(
    text: str, initial_token_parser: TokenParser
) -> typing.Generator[ParsedToken, None, None]:
    parse_token_state: typing.Optional[ParseTokenState] = ParseTokenState(
        initial_token_parser, text, 0
    )
    while True:
        assert parse_token_state
        (parsed_token, parse_token_state) = parse_token_state.parse()
        yield parsed_token
        if isinstance(parsed_token.token, EofToken):
            return
