import textwrap

import alanp
from alanp import adoc


def _adoc(adoc: str) -> str:
    return textwrap.dedent(adoc)


simple = _adoc(
    """\
= Foo

Bar
"""
)


def test_tokenize_simple() -> None:
    tokens = list(
        alanp.tokenize(
            simple,
            adoc.ZeroParser(),
        )
    )
    assert tokens == [
        alanp.ParsedToken(pos=0, token=adoc.HeaderToken(text="= ")),
        alanp.ParsedToken(pos=2, token=adoc.TextToken(text="Foo")),
        alanp.ParsedToken(pos=5, token=adoc.NewLineToken(text="\n")),
        alanp.ParsedToken(pos=6, token=adoc.NewLineToken(text="\n")),
        alanp.ParsedToken(pos=7, token=adoc.TextToken(text="Bar")),
        alanp.ParsedToken(pos=10, token=adoc.NewLineToken(text="\n")),
        alanp.ParsedToken(pos=11, token=alanp.EofToken(text="")),
    ]


def test_make_blocks_simple() -> None:
    blocks = list(adoc.make_blocks(simple))
    assert blocks == [
        adoc.HeaderBlock(
            header_token=alanp.ParsedToken(pos=0, token=adoc.HeaderToken(text="= ")),
            text_token=alanp.ParsedToken(pos=2, token=adoc.TextToken(text="Foo")),
        ),
        adoc.ParagraphBlock(
            tokens=[
                alanp.ParsedToken(pos=7, token=adoc.TextToken(text="Bar")),
                alanp.ParsedToken(pos=10, token=adoc.NewLineToken(text="\n")),
            ]
        ),
    ]
