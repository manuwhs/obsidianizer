from collections import namedtuple

WORD_IN_PAGE = namedtuple(
    "word", ["x0", "y0", "x1", "y1", "word", "block_no", "line_no", "word_no"]
)
ANNOTATION = namedtuple(  # noqa
    "annotation",
    [
        "highlighted_text",
        "annotation_text",
        "x0",
        "y0",
        "x1",
        "y1",
        "is_subcomment",
        "datetime",
        "author",
    ],
)
