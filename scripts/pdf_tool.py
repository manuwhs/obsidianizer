import click
import fitz
import pandas as pd
from obsidianizer.nlp.text_cleanup import get_most_used_words
from obsidianizer.obsidian.pdf_tools import get_vault_df_from_pdf_by_page
from obsidianizer.obsidian.transformations import create_common_words_vault, join_vaults
from obsidianizer.obsidian.vault import save_vault
from obsidianizer.pdf_tools.annotations import AnnotationExtractionMode
from obsidianizer.pdf_tools.documents import extract_book_annotations

# For the help menu
EXTRACTION_MODE_OPTIONS = "\n".join([f"{x[1]}: {x[0]}" for x in AnnotationExtractionMode.list()])


@click.group(
    help="""Tool manage pdfs. Examples:

    1) List the available folders in your account:\n
        python pdf_tool.py extract-annotations -f "./my_pdf.pdf" --output "./output_vault/" --output-format vault --mode 3 --most-common-words-as-backlinks 20
"""
)
def main():
    pass


@main.command(help="Extracts the annotations of a given pdf.")
@click.option("-f", "--filepath", help="Path of the pdf to extract the annotations from", required=True)
@click.option(
    "--output",
    help="Name of the output file or vault containing the annotations.",
    required=True,
)
@click.option(
    "--output-format",
    default="csv",
    help="The format of the output containing the annotations: Options: 1) csv. 2) vault",
)
@click.option(
    "-m",
    "--mode",
    type=int,
    default=0,
    help="Annotation extraction modes: \n" + EXTRACTION_MODE_OPTIONS,
)
@click.option(
    "--most-common-words-as-backlinks",
    type=int,
    default=0,
    help="Number of the most common words to set as backlinks in the vault",
)
def extract_annotations(
    filepath: str,
    output: str,
    output_format: str,
    mode: int,
    most_common_words_as_backlinks: int,
):
    book = fitz.open(filepath)
    annotations_blocks = extract_book_annotations(book, mode=AnnotationExtractionMode(mode))

    if output_format == "csv":
        annotations_blocks.to_csv(output)
    elif output_format == "vault":
        vault_df = get_vault_df_from_pdf_by_page(annotations_blocks, output)
        if most_common_words_as_backlinks > 0:
            words = get_most_used_words(annotations_blocks["highlighted_text"])
            important_words = list(pd.Series(words[0:most_common_words_as_backlinks]).index)
            common_words_vault = create_common_words_vault(important_words, output)
            vault_df = join_vaults(vault_df, common_words_vault, True)
        save_vault(vault_df)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
