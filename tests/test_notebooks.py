import os
import pathlib

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def notebook_tester_func(notebook_name: str = "2.Extract_Annotations_from_pdf.ipynb"):
    notebooks_path = str(pathlib.Path(__file__).parent.absolute()) + "/../notebooks/"
    notebooks_path_metadata = str(
        pathlib.Path(notebooks_path + "/" + notebook_name).parent.absolute()
    )
    test_notebook_path = notebooks_path + notebook_name

    nb_name, _ = os.path.splitext(os.path.basename(test_notebook_path))

    dirname = os.path.dirname(test_notebook_path)

    with open(test_notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    proc = ExecutePreprocessor(timeout=600, kernel_name="python3")
    proc.allow_errors = True

    proc.preprocess(nb, {"metadata": {"path": notebooks_path_metadata}})
    output_path = os.path.join(
        dirname + "/../test_outcomes/", "{}_all_output.ipynb".format(nb_name)
    )
    with open(output_path, mode="wt") as f:
        nbformat.write(nb, f)

    # Test the errors
    for cell in nb.cells:
        if "outputs" in cell:
            for output in cell["outputs"]:
                assert output.output_type != "error"

    return nb


def test_pdf_functionalities_notebooks():
    notebooks_to_test = ["documentation/2.Basic_pdf_functionalities.ipynb"]

    for notebook in notebooks_to_test:
        nb = notebook_tester_func(notebook)
    return nb


def test_basic_journal_processing_notebooks():
    notebooks_to_test = ["documentation/3.Basic_journal_processing.ipynb"]

    for notebook in notebooks_to_test:
        nb = notebook_tester_func(notebook)
    return nb


def test_basic_vault_processing_notebooks():
    notebooks_to_test = ["documentation/4.Vault_processing.ipynb"]

    for notebook in notebooks_to_test:
        nb = notebook_tester_func(notebook)
    return nb
