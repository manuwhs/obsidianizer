import os
import re


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
