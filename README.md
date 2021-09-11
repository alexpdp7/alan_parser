# Alan

An experiment in parsing.

Many lightweight languages such as AsciiDoc do not have context-free grammars or have extremely complex grammars.
For example, [you can configure with attributes how the AsciiDoc parser works](https://docs.asciidoctor.org/asciidoc/latest/subs/apply-subs-to-blocks/).

Alan is a library that simplifies writing parsing programs.
Alan helps you tokenize and create annotated ASTs with position information.

Alan does not force you into any kind of grammar.
Alan does not let you define languages declaratively with grammars, only as code.
Alan has no performance guarantees, Alan parsers might be inefficient.

## Plans

With the right abstractions, Alan should be able to:

* Print parsing errors prettily.
* Help implementing linters, and display linting errors prettily.

The interface of Alan is unstable and bound to change.
