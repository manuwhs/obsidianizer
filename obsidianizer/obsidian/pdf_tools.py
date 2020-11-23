import pandas as pd
from obsidianizer.pdf_tools.annotations import find_position_candidates_in_list

from .utils import preprocess_folder_name


def get_vault_df_from_pdf(
    chapter_blocks: pd.DataFrame,
    subsection_blocks: pd.DataFrame,
    annotations_blocks: pd.DataFrame,
    filedir: str = "./Ecce/",
) -> None:
    """Creates the structure of markdown files related to the book"""

    filepaths = []
    relative_keyword_paths = []
    keywords = []
    markdowns = []

    # Find where the subsenctions fit in the chapters and subsections
    annotations_blocks["chapter_index"] = find_position_candidates_in_list(
        annotations_blocks, chapter_blocks, column="block_absolute_y0"
    )
    annotations_blocks["subsection_index"] = find_position_candidates_in_list(
        annotations_blocks, subsection_blocks, column="block_absolute_y0"
    )
    annotation_groups = annotations_blocks.groupby(
        ["chapter_index", "subsection_index"]
    ).groups

    # For every chapter, get the associated subsections
    for annotation_group in annotation_groups.keys():
        chapter_i = annotation_group[0]
        subsection_i = annotation_group[1]

        # Chapter related processing
        chapter_text = preprocess_folder_name(
            " ".join(chapter_blocks.iloc[chapter_i]["words"])
        )
        chapter_dir = filedir + chapter_text + "/"

        # Subsection related processing
        subsection_text = preprocess_folder_name(
            " ".join(subsection_blocks.iloc[subsection_i]["words"])
        )
        subsection_dir = chapter_dir + subsection_text + "/"

        # Annotation related
        for annotation_i in annotation_groups[annotation_group]:
            annotation = annotations_blocks.iloc[annotation_i]

            markdown = get_annotation_obsidian_markdown(annotation)
            filepath = get_annotation_filepath(annotation, subsection_dir)

            filepaths.append(filepath)
            relative_keyword_paths.append(subsection_dir)
            keywords.append(subsection_text)
            markdowns.append(markdown)

    vault_dict = {
        "filepath": filepaths,
        "keyword": keywords,
        "relative_keyword_path": relative_keyword_paths,
        "markdown": markdowns,
    }

    vault_df = pd.DataFrame(vault_dict)

    return vault_df


def get_annotation_obsidian_markdown(annotation: pd.Series) -> str:
    """Transforms an annotation row into the text to be added to an obsidian md file"""
    highlighted_text = annotation["highlighted_text"]
    annotation_text = annotation["annotation_text"]

    text = (
        f"## Quote \n{highlighted_text} \n\n## Interpretation  \n{annotation_text} \n\n"
    )

    return text


def get_annotation_filepath(annotation: pd.Series, subsection_dir: str) -> str:
    filepath = subsection_dir + subsection_dir.split("/")[-2] + ".md"
    return filepath
