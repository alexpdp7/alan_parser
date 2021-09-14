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


ifdef = _adoc(
    """\
ifndef::att1,att2[whatever]
"""
)


def test_tokenize_ifdef() -> None:
    tokens = list(
        alanp.tokenize(
            ifdef,
            adoc.ZeroParser(),
        )
    )
    assert tokens == [
        alanp.ParsedToken(pos=0, token=adoc.ConditionalDirectiveToken(text="ifndef::")),
        alanp.ParsedToken(pos=8, token=adoc.AttributeToken(text="att1")),
        alanp.ParsedToken(pos=12, token=adoc.CommaToken(text=",")),
        alanp.ParsedToken(pos=13, token=adoc.AttributeToken(text="att2")),
        alanp.ParsedToken(pos=17, token=adoc.ConditionalDirectiveStartToken(text="[")),
        alanp.ParsedToken(pos=18, token=adoc.TextToken(text="whatever")),
        alanp.ParsedToken(pos=26, token=adoc.ConditionalDirectiveEndToken(text="]\n")),
        alanp.ParsedToken(pos=28, token=alanp.EofToken(text="")),
    ]


def test_make_blocks_ifdef() -> None:
    blocks = list(adoc.make_blocks(ifdef))
    assert blocks == [
        adoc.ParagraphBlock(
            tokens=[alanp.ParsedToken(pos=18, token=adoc.TextToken(text="whatever"))],
            condition=[
                alanp.ParsedToken(
                    pos=0, token=adoc.ConditionalDirectiveToken(text="ifndef::")
                ),
                alanp.ParsedToken(pos=8, token=adoc.AttributeToken(text="att1")),
                alanp.ParsedToken(pos=12, token=adoc.CommaToken(text=",")),
                alanp.ParsedToken(pos=13, token=adoc.AttributeToken(text="att2")),
            ],
        )
    ]
