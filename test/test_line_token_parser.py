import typing

import alanp


class LineTokenParser(alanp.TokenParser):
    def parse(self, text: str) -> typing.Tuple[alanp.Token, alanp.TokenParser]:
        return (alanp.Token(text.split("\n")[0] + "\n"), self)


def test_line_token_parser() -> None:
    parsed = alanp.tokenize(
        """This
is
a
test
""",
        LineTokenParser(),
    )
    assert list(parsed) == [
        alanp.ParsedToken(pos=0, token=alanp.Token(text="This\n")),
        alanp.ParsedToken(pos=5, token=alanp.Token(text="is\n")),
        alanp.ParsedToken(pos=8, token=alanp.Token(text="a\n")),
        alanp.ParsedToken(pos=10, token=alanp.Token(text="test\n")),
        alanp.ParsedToken(pos=15, token=alanp.EofToken(text="")),
    ]
