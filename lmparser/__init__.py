import abc
import re
import typing


class Text:
    def __init__(self, s):
        self.s = s

    def get_segment(self):
        return LeafSegment(self, 0, len(self.s))

    def __getitem__(self, key):
        return self.s.__getitem__(key)


class LeafSegment:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

    def get_segment_text(self) -> str:
        return self.text[self.start : self.end]

    def is_empty(self) -> bool:
        return self.end == self.start

    def parse_re(self, pattern, segment_type):
        match = re.match(pattern, self.get_segment_text())
        if not match:
            return (None, None)
        parsed, remaining = self.split_at(match.end())
        return parsed.as_type(segment_type), remaining

    def split_at(self, pos: int):
        return (
            LeafSegment(self.text, self.start, self.start + pos),
            LeafSegment(self.text, self.start + pos, self.end),
        )

    def as_type(self, type):
        return type(self.text, self.start, self.end)

    def as_dict(self) -> dict:
        return {
            "type": type(self).__name__,
            "text": self.get_segment_text(),
            "start": self.start,
            "end": self.end,
        }

    def __repr__(self):
        return f"({type(self).__name__}: {repr(self.get_segment_text())})"


class ParentSegment:
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return f"({type(self).__name__}: {repr(self.children)}"

    def as_dict(self) -> dict:
        return {
            "type": type(self).__name__,
            "children": [c.as_dict() for c in self.children],
        }


class Parser(abc.ABC):
    @abc.abstractmethod
    def parse(self, segment):
        """returns left, right, next_parser"""


def parse_str(s, parser):
    return parse_segment(Text(s).get_segment(), parser)


def parse_segment(remaining_segment, parser):
    segments = []
    while not remaining_segment.is_empty():
        parsed, remaining_segment, parser = parser.parse(remaining_segment)
        segments.append(parsed)
    return segments
