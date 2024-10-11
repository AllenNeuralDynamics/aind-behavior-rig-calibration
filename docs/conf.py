# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import glob
import os
import sys

import erdantic as erd
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath("../src"))
import aind_behavior_services

SOURCE_ROOT = "https://github.com/AllenNeuralDynamics/Aind.Behavior.Services/tree/main/src/"


project = "AIND Behavior Services"
copyright = "2024, Allen Institute for Neural Dynamics"
author = "Bruno Cruz"
release = aind_behavior_services.__version__


# -- Generate jsons --------------------------------------------------------------

json_root_path = os.path.abspath("../src/schemas")
json_files = glob.glob(os.path.join(json_root_path, "*.json"))
rst_target_path = os.path.abspath("json_schemas")

leaf_template = """
{json_file_name}
----------------------------------------------------

`Download Schema <https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/schemas/{json_file_name}.json>`_

.. jsonschema:: https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/schemas/{json_file_name}.json
   :lift_definitions:
   :auto_reference:

"""

for json_file in json_files:
    json_file_name = os.path.basename(json_file)
    with open(os.path.join(rst_target_path, f"{json_file_name.replace('.json', '')}.rst"), "w") as f:
        f.write(leaf_template.format(json_file_name=json_file_name.replace(".json", "")))


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx-jsonschema",
    "sphinx_jinja",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.linkcode",
    "sphinx_mdinclude",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_copybutton",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autosummary_generate = True

autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_title = "AIND Behavior Services"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "light_logo": "light-logo.svg",
    "dark_logo": "dark-logo.svg",
}

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# -- Options for linkcode extension ---------------------------------------


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    return f"{SOURCE_ROOT}/{filename}.py"


# -- Class diagram generation


def export_model_diagram(model: BaseModel, root: str = "_static") -> None:
    diagram = erd.create(model)
    diagram.draw(f"{root}/{model.__name__}.svg")


_diagram_root = "_static"
export_model_diagram(aind_behavior_services.session.AindBehaviorSessionModel, _diagram_root)
