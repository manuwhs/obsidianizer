from typing import Any, List

import fitz


def _check_contain(
    r_word: fitz.Rect, points: List[Any], _threshold_intersection: float = 0.2
) -> bool:
    """If `r_word` is contained in the rectangular area.

    The area of the intersection should be large enough compared to the
    area of the given word.

    Args:
        r_word (fitz.Rect): rectangular area of a single word.
        points (list): list of points in the rectangular area of the
            given part of a highlight.

    Returns:
        bool: whether `r_word` is contained in the rectangular area.
    """
    # `r` is mutable, so everytime a new `r` should be initiated.
    r = fitz.Quad(points).rect
    r.intersect(r_word)

    if r.getArea() >= r_word.getArea() * _threshold_intersection:
        contain = True
    else:
        contain = False
    return contain
