from typing import List

from obsidianizer.pdf_tools import WORD_IN_PAGE


def get_blocks_of_words(words_in_page: List[WORD_IN_PAGE]) -> List[List[WORD_IN_PAGE]]:
    """Deprecated
    Returns a summary of the blocks there are.
    """
    block_no_aux = 0
    words_in_block: List[List[WORD_IN_PAGE]] = [[]]

    for word in words_in_page:
        if word.block_no == block_no_aux:
            words_in_block[block_no_aux].append(word.word)
        else:
            block_no_aux = word.block_no
            words_in_block.append([word.word])
    return words_in_block
