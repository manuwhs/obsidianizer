import glob
import os
from typing import Optional

import pandas as pd
from obsidianizer.obsidian.utils import add_annotation_to_obsidian_tree, mkdir_if_needed


def load_vault(path: str) -> pd.DataFrame:
    """Returns pandas dataframe with all the md documents in the folder structure and their content."""

    filepaths = [f for f in glob.glob(path + "**/*.md", recursive=True)]
    file_keyword = [f.split("/")[-1][:-3] for f in filepaths]

    relative_keyword_path = [f[len(path) : -3] for f in filepaths]

    file_contents = []

    for filepath in filepaths:
        with open(filepath) as f:
            file_contents.append(f.read())

    files_dict = {
        "filepath": filepaths,
        "keyword": file_keyword,
        "relative_keyword_path": relative_keyword_path,
        "markdown": file_contents,
    }
    return pd.DataFrame(files_dict)


def save_vault(vault_df: pd.DataFrame, vault_path: Optional[str] = None) -> None:
    """Writed the vault dataframe to disk.
    If two rows have the same filepath, it will simply append text after the other
    adding \n\n.

    If the vault_path is specified, it will overwrite the filepath part.
    TODO: Probably do not use the filepath part in the future.
    """

    for i, row in vault_df.iterrows():
        if vault_path is None:
            filepath = row["filepath"]
        else:
            # Replace the filepath
            # TODO: probably in the future the filepath property will not be used.
            filepath = (
                vault_path + row["relative_keyword_path"] + row["keyword"] + ".md"
            )

        mkdir_if_needed(os.path.dirname(filepath))
        add_annotation_to_obsidian_tree(filepath, row["markdown"])
