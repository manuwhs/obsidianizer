import itertools
import os
import re
from typing import Dict, List, Optional

import pandas as pd


class DuplicatedKeywordException(Exception):
    def __init__(self, duplicated_keyword: str):
        message = f"""Handling of vaults with dupilcated markdown file names not implemented yet.
        The duplicated keyword is: {duplicated_keyword}"""
        super().__init__(message)


def preprocess_folder_name(folder_name: str) -> str:
    filtered_folder_name = re.sub(r"[^a-zA-Z0-9 ]", "", folder_name)
    return filtered_folder_name


def mkdir_if_needed(path: str) -> None:
    try:
        os.makedirs(path)
    except OSError as error:  # noqa
        pass  # print(error)


def add_annotation_to_obsidian_tree(filename: str, text: str) -> None:
    """Creates file if needed, otherwise it appends the markdown to the end"""

    if os.path.exists(filename):
        text = "\n\n" + text
        append_write = "a+"  # append if already exists
    else:
        append_write = "w"  # make a new file if not

    fp = open(filename, append_write)
    fp.write(text)
    fp.close()


def remove_renaming_from_backlinks(backlinks: List[str]) -> List[str]:
    # Handle renaming of backlinks [XXX:yyy]
    curated_backlinks = []
    for backlink in backlinks:
        if backlink.find("|") != -1:
            backlink = backlink[: backlink.find("|")]

        curated_backlinks.append(backlink)
    return curated_backlinks


def remove_relative_path_from_backlinks(backlinks: List[str]) -> List[str]:
    # Handle ducplicated backlinks [XXX/ZZZ:yyy]
    curated_backlinks = []
    for backlink in backlinks:
        backlink = backlink.split("/")[-1]

        curated_backlinks.append(backlink)
    return curated_backlinks


def remove_subsection_from_backlinks(backlinks: List[str]) -> List[str]:
    # Handle ducplicated backlinks [XXX/ZZZ:yyy#]
    curated_backlinks = []
    for backlink in backlinks:
        backlink = backlink.split("#")[0]

        curated_backlinks.append(backlink)
    return curated_backlinks


def get_backlinks(text: str) -> List[str]:
    """Returns a list with the backlinks in the given text
    TODO: Handle the duplicated entries better"""

    backlinks = re.findall(r"\[\[.*?\]\]", text)
    backlinks = [backlink[2:-2] for backlink in backlinks]

    # Handle renaming of backlinks [XXX:yyy]
    backlinks = remove_renaming_from_backlinks(backlinks)
    # Handle ducplicated backlinks [XXX/ZZZ:yyy]
    backlinks = remove_relative_path_from_backlinks(backlinks)
    # Handle [XXX#subsection]
    backlinks = remove_subsection_from_backlinks(backlinks)

    # Strip since obsidian allows spaces and we should not.
    backlinks = [x.strip() for x in backlinks]

    # Remove image links:
    # TODO: improve in the future to actually detect the ! in ![[XX]] or by extension
    backlinks = [x for x in backlinks if "." not in x]

    return backlinks


def get_vault_df_unique_backlinks(vault_df: pd.DataFrame) -> List[str]:
    """Returns the list of unique referenced backlinks in markdown of the vault_df"""
    backlinks = vault_df["markdown"].apply(get_backlinks)
    unique_backlinks = pd.Series(itertools.chain.from_iterable(backlinks)).unique()
    return unique_backlinks


def get_subbacklinks_from_other_backlinks(
    short_backlinks: List[str], long_backlinks: List[str]
) -> Dict[str, List[str]]:
    """This function returns, for every backlink in long_backlinks, which of the
    backlinks in short_backlinks it contains.
    The comparison is done in lower case.
    """
    short_backlinks_lowercase = [x.lower() for x in short_backlinks]
    long_backlinks_lowercase = [x.lower() for x in long_backlinks]

    sub_backlinks_dict = dict()

    for i in range(len(long_backlinks_lowercase)):
        long_backlink = long_backlinks_lowercase[i]
        sub_backlinks = [
            short_backlinks[j]
            for j in range(len(short_backlinks_lowercase))
            if short_backlinks_lowercase[j] in long_backlink
        ]

        # Remove itself as a backlink just in case
        if long_backlinks[i] in sub_backlinks:
            sub_backlinks.remove(long_backlinks[i])

        if len(sub_backlinks):
            sub_backlinks_dict[long_backlinks[i]] = sub_backlinks

    return sub_backlinks_dict


def add_sublinks_to_vault_df(
    vault_df: pd.DataFrame, relative_keyword_path: Optional[str] = None
) -> pd.DataFrame:
    """It adds at the end of the markdown, the related other backlinks among the given list.
    If relative_keyword_path is not None, it will only combine the within that relative keyword path
    """

    if relative_keyword_path is not None:
        n = len(relative_keyword_path)
        vault_df = vault_df[
            vault_df["relative_keyword_path"][:n] == relative_keyword_path
        ]
    else:
        vault_df = vault_df.copy()

    unique_backlinks = get_vault_df_unique_backlinks(vault_df)
    sub_backlinks_dict = get_subbacklinks_from_other_backlinks(
        unique_backlinks, unique_backlinks
    )

    for long_backlink in sub_backlinks_dict.keys():
        related_backlinks_text = "\n\nRelated backlinks: "
        for backlink in sub_backlinks_dict[long_backlink]:
            related_backlinks_text += f"[[{backlink}]]"

        # Get the entry in the vault that has the keyword
        index_keyword = vault_df[
            vault_df["keyword"].map(lambda x: x.encode("utf-8"))
            == long_backlink.encode("utf-8")
        ].index

        # TODO: Handle duplicated keywords in the future
        if len(index_keyword) > 1:
            raise DuplicatedKeywordException(long_backlink)

        vault_df.loc[index_keyword[0]]["markdown"] += related_backlinks_text
    return vault_df


def get_duplicated_vault_keywords(vault_df: pd.DataFrame) -> Dict[str, List[int]]:
    """Returns dictionary with the repeated keywords that need to be handled in a special way.
    The dictionary contains the keyword as key and the list of indexes as value
    """

    df = vault_df.reset_index().groupby("keyword").agg({"index": ["count", list]})
    df.columns = [" ".join(col).strip() for col in df.columns.values]
    df = df[df["index count"] > 1]

    duplicated_keywords_dict = df["index list"].to_dict()
    return duplicated_keywords_dict
