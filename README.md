`lmparser` was an experiment in parsing.

Archived, because currently I think Prolog is the best option to write parsers for lightweight markup languages.
See this [AsciiDoc Prolog parser](https://github.com/alexpdp7/prolog-asciidoc).

# The problem

Many lightweight markup languages, such as Markdown and AsciiDoc, cannot be parsed easily (or at all) using conventional parsing systems like ANTLR, lex/yacc, etc.
Those languages often use hand-rolled parsers or need hacks on top of a conventional parser.

When writing hand-rolled parsers, creating an AST with proper annotations about source code position properly is an additional burden on top of writing a parser.
When using conventional parsers, the resulting parser definition is often hard to understand, especially when implementing hacks on top of the parser.

Having a proper AST, makes writing tools such as the following much simpler.

* A linter/formatter that ensures some conventions are followed (such as a sentence per line, or disallowing some styles, etc.)
* Spell checkers/grammar validators (that skip verbatim blocks, etc.)
* Transformers (tools that can perform smart search and replace)
* Link checkers (extracting all links in a document and ensuring they can be fetched)

# The proposal

`lmparser` proposes a framework for writing hand-rolled parsers that helps creating a proper AST.
The framework takes care of building the AST and provides functions that parse text, keeping track of parsing positions.

Writing complete parsers for lightweight markup languages seems to still be a daunting task, even with a framework defined for this purpose.
But probably many teams using lightweight markup languages are not using all features from the language, or they do not need a proper AST for everything.

This experiment should provide information on whether an adequate framework can enable teams to build useful tools for working on their lightweight markup texts.

# Further doubts

This experiment is implemented in Python for quick prototyping, but it remains to be seen if it's the best choice.

* It is a very popular language, and many teams may already have Python know-how.
* Even the current rough prototype has some complex typing.
  Statically-typed languages, or languages with algebraic types, may make writing parsers easier.
* Some common parsing patterns may benefit from abstractions such as macros or higher-order programming that are more ergonomic in other languages-
* Languages that can compile to small self-contained binaries, WASM/JS, or run on the JVM might open more possibilities for embedding parsers in other tools, or simplifying their distribution.

* Rust, Haskell, OCaml, or F# might be more suitable languages, but they are also less popular and more complex than Python.
* Javascript/Typescript are more popular, and may improve the distribution situation.

# Further references

Some references about the complexities of parsing lightweight markup languages.

https://www.tweag.io/blog/2021-06-15-asciidoc-haskell-pandoc/
