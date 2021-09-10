import abc
import dataclasses


@dataclasses.dataclass
class Token:
    text: str


@dataclasses.dataclass
class ParsedToken:
    pos: int
    token: Token


class TokenParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, text) -> Token:
        pass


def parse_tokens(text: str, token_parser: TokenParser, pos: int = 0):
    while pos < len(text):
        token = token_parser.parse(text[pos:])
        yield ParsedToken(pos, token)
        pos += len(token.text)
