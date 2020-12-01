from typing import List

import pandas as pd


def create_common_words_vault(
    tokens: List[str], vault_path: str, relative_vault_path: str = "common_tokens/"
):
    """Converts a set of keywords into a vault df."""

    filepaths = []
    relative_keyword_paths = []
    keywords = []
    markdowns = []

    for keyword in tokens:
        filepaths.append(vault_path + relative_vault_path + keyword + ".md")
        relative_keyword_paths.append(relative_vault_path)
        keywords.append(keyword)
        markdowns.append("")

    vault_dict = {
        "filepath": filepaths,
        "keyword": keywords,
        "relative_keyword_path": relative_keyword_paths,
        "markdown": markdowns,
    }
    vault_df = pd.DataFrame(vault_dict)
    return vault_df


def highlight_obsidian_tokens(text: str, tokens: List[str]) -> str:
    # TODO: Sort tokens by length of words to avoid highlighting a word that should not
    # Improve this by maybe creating n grams or by checking that the word is not in [[]]
    # also maybe by lower case detection and replacing with the original text as well.

    for token in tokens:
        text = text.replace(token, f"[[{token}]]")
    return text


def highlight_tokens_in_vault(
    vault_df: pd.DataFrame, tokens: List[str]
) -> pd.DataFrame:
    """Highlights the list of tokens in the given vault"""

    vault_df = vault_df.copy(deep=True)

    for i, row in vault_df.iterrows():
        vault_df.iloc[i]["markdown"] = highlight_obsidian_tokens(
            vault_df.iloc[i]["markdown"], tokens
        )

    return vault_df


def join_vaults(
    vault_left: pd.DataFrame, vault_right: pd.DataFrame, merge_keywords: bool = True
) -> pd.DataFrame:
    """Joins two vautls together.
    If merge_keywords is True, it will look for the keywords in vault_left and associate them to
    It resets the index.

    TODO: Check for duplicated keywords, probably include the relative path as well to avoid conflicts.
    How to choose which one gets selected?
    """
    if merge_keywords:
        tokens_to_highlight = vault_right["keyword"].unique()
        vault_left = highlight_tokens_in_vault(vault_left, tokens_to_highlight)

    return pd.concat([vault_left, vault_right]).reset_index(drop=True)
