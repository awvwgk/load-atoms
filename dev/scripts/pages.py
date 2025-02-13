from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Callable, TypedDict

import numpy as np
import yaml
from ase.data import chemical_symbols
from load_atoms import load_dataset, view
from load_atoms.atoms_dataset import AtomsDataset
from load_atoms.database.database_entry import (
    LICENSE_URLS,
    DatabaseEntry,
    PropertyDescription,
)
from load_atoms.utils import lpad

os.environ["LOAD_ATOMS_DEBUG"] = "1"

# this file is at dev/scripts/pages.py
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_DOC_SOURCE = _PROJECT_ROOT / "docs/source"
_DOWNLOAD_DIR = _PROJECT_ROOT / "testing-datasets"


def build_docs_page_for(name: str):
    # avoid downloading the dataset so that if local changes have been made,
    # they are reflected in the documentation preview
    # copy over the folder if it doesn't exist
    shutil.copy(
        _PROJECT_ROOT / "database" / name / f"{name}.yaml",
        _DOWNLOAD_DIR / "database-entries" / f"{name}.yaml",
    )
    # simulate download by moving any non-yaml files to the temp folder
    for file in (_PROJECT_ROOT / "database" / name).glob("*"):
        if file.suffix == ".yaml":
            continue
        # copy file
        relative_path = file.relative_to(_PROJECT_ROOT / "database" / name)
        temp_folder = _DOWNLOAD_DIR / "raw-downloads" / name
        temp_folder.mkdir(exist_ok=True, parents=True)
        shutil.copy(file, temp_folder / relative_path)

    dataset = load_dataset(name, root=_DOWNLOAD_DIR)

    compute_info(dataset)

    raw_rst = "\n\n".join(func(dataset) for func in _page_component_generators)
    with open(_DOC_SOURCE / "datasets" / f"{name}.rst", "w") as f:
        f.write(raw_rst)


def build_datasets_index():
    # load all DatabaseEntry's
    entry_files = sorted(
        (_PROJECT_ROOT / "database").glob("**/*.yaml"),
        key=lambda f: f.name.lower(),
    )
    entries = [DatabaseEntry.from_yaml_file(f) for f in entry_files]

    # 2. create table and place in database-summary.rst
    table = info_table(entries)

    header = """\
.. This file is autogenerated by dev/scripts/generate_page.py

Summary
=======

:code:`load_atoms` maintains a database of (named) datasets for ease of use. 
These can be downloaded from the internet (and cached locally) using 
:func:`~load_atoms.load_dataset`:

"""
    (_DOC_SOURCE / "database-summary.rst").write_text(header + table)

    # 3. build per-category pages
    toc = """\
.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Datasets

   database-summary
"""
    categories = sorted(set(e.category for e in entries))
    for category in categories:
        toc += f"   category/{category.lower().replace(' ', '-')}\n"

    (_DOC_SOURCE / "datasets-index.rst").write_text(toc)

    for category in categories:
        category_entries = [e for e in entries if e.category == category]
        title = (
            "#" * len(category) + "\n" + category + "\n" + "#" * len(category)
        )
        table = summary_cards(category_entries)
        toctree = """\
.. toctree::
    :maxdepth: 1
    :hidden:

"""
        for entry in category_entries:
            toctree += f"    ../datasets/{entry.name}\n"

        file_contents = f"""\
.. This file is autogenerated by dev/scripts/generate_page.py

{title}

{table}

{toctree}
"""
        (
            _DOC_SOURCE
            / "category"
            / f"{category.lower().replace(' ', '-')}.rst"
        ).write_text(file_contents)


ComponentGenerator = Callable[[AtomsDataset], str]
_page_component_generators: list[ComponentGenerator] = []


def register_component(func: ComponentGenerator):
    _page_component_generators.append(func)
    return func


@register_component
def auto_generated_warning(dataset: AtomsDataset) -> str:
    return ".. This file is autogenerated by dev/scripts/generate_page.py"


@register_component
def title(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    name = dataset.description.name
    return name + "\n" + "=" * len(name)


@register_component
def header(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    idx: int = dataset.description.representative_structure  # type: ignore
    if idx is None:
        # get first structure with more than 1 atom
        for i, s in enumerate(dataset):
            if len(s) > 1:
                idx = i
                break

    html_visualisation = view(dataset[idx], show_bonds=True)
    viz = '<div class="viz">' + html_visualisation.data + "</div>"

    file_name = f"_static/visualisations/{dataset.description.name}.html"
    (_DOC_SOURCE / "_static/visualisations").mkdir(exist_ok=True)
    with open(_DOC_SOURCE / file_name, "w") as f:
        f.write(viz)

    info = str(dataset.description.description).replace("\n", "\n        ")
    return f"""\
.. grid:: 1 1 2 2
    
    .. grid-item::

        .. raw:: html
            :file: ../{file_name}

    .. grid-item::
        :class: info-card

        {info}
"""


@register_component
def code_block(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    summary = str(dataset).replace("\n", "\n    ")
    return f"""\
.. code-block:: pycon

    >>> from load_atoms import load_dataset
    >>> load_dataset("{dataset.description.name}")
    {summary}
"""


@register_component
def license(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    if dataset.description.license is None:
        return ""

    license = dataset.description.license
    url = LICENSE_URLS[license]
    return f"""\
License
-------

This dataset is licensed under the `{license} <{url}>`_ license.
"""


@register_component
def citation(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    if dataset.description.citation is None:
        return ""

    citation = dataset.description.citation.replace("\n", "\n    ")
    return f"""\
Citation
--------

If you use this dataset in your work, please cite the following:

.. code-block:: latex
    
    {citation}
"""


def _build_table(
    descriptions: dict[str, PropertyDescription],
    mappping: dict[str, Any],
    replace_first_dim: bool,
):
    def get_type(name: str):
        values = mappping[name]
        if isinstance(values, np.ndarray):
            shape = list(values.shape)
            if replace_first_dim:
                shape[0] = "N"  # type: ignore
            to_show = f"ndarray{tuple(shape)}".replace("'", "")
            _type = f":class:`{to_show} <numpy.ndarray>`"
        else:
            _type = f":class:`~{type(values).__name__}`"
        return _type

    header = """\
.. list-table::
    :header-rows: 1

    * - Property
      - Units
      - Type
      - Description
"""

    rows = []
    for name, description in descriptions.items():
        units = description.units if description.units is not None else ""
        desc = description.desc.replace("\n", "\n        ")
        rows.append(
            f"""\
    * - :code:`{name}`
      - {units}
      - {get_type(name)}
      - {desc}
"""
        )

    return header + "\n".join(rows)


@register_component
def property_info(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    if dataset.description.per_atom_properties is None:
        per_atom_properties = ""
    else:
        per_atom_properties = """\
**Per-atom**:

{}""".format(
            _build_table(
                dataset.description.per_atom_properties,
                dataset[0].arrays,
                replace_first_dim=True,
            )
        )

    if dataset.description.per_structure_properties is None:
        per_structure = ""
    else:
        per_structure = """\
**Per-structure**:
    
{}""".format(
            _build_table(
                dataset.description.per_structure_properties,
                dataset[0].info,
                replace_first_dim=False,
            )
        )

    if not (per_atom_properties + per_structure):
        return ""

    return f"""\
Properties
----------

{per_atom_properties}

{per_structure}
"""


@register_component
def importer_code(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    name = dataset.description.name
    return f"""\
Miscellaneous information
-------------------------

``{dataset.description.name}`` is imported as an 
:class:`~load_atoms.atoms_dataset.{type(dataset).__name__}`:

.. dropdown:: Importer script for :code:`{name}`

    .. literalinclude:: ../../../src/load_atoms/database/importers/{DatabaseEntry.importer_file_stem(name)}.py
       :language: python
"""  # noqa: E501


@register_component
def database_entry(dataset: AtomsDataset) -> str:
    assert dataset.description is not None
    name = dataset.description.name
    file = _PROJECT_ROOT / "database" / name / f"{name}.yaml"
    entry = lpad(file.read_text(), 8)
    return f"""\

.. dropdown:: :class:`~load_atoms.database.DatabaseEntry` for :code:`{name}`

    .. code-block:: yaml

{entry}
"""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# save expensive information to avoid recomputation

_INFO_DIR = Path(__file__).parent / "info"
_INFO_DIR.mkdir(exist_ok=True)


class ComputedInfo(TypedDict):
    n_structures: int
    n_atoms: int
    elements: list[str]


def compute_info(dataset: AtomsDataset) -> ComputedInfo:
    assert dataset.description is not None
    Zs = np.unique(dataset.arrays["numbers"])
    elements = [chemical_symbols[Z] for Z in sorted(Zs)]

    d = dict(
        n_structures=len(dataset),
        n_atoms=dataset.n_atoms,
        elements=elements,
    )

    with open(
        _INFO_DIR / f"{dataset.description.name}-computed.yaml", "w"
    ) as f:
        yaml.dump(d, f)

    return d  # type: ignore


def get_info(dataset_name: str) -> ComputedInfo:
    if not (_INFO_DIR / f"{dataset_name}-computed.yaml").exists():
        dataset = load_dataset(dataset_name, root=_DOWNLOAD_DIR)
        return compute_info(dataset)
    else:
        with open(_INFO_DIR / f"{dataset_name}-computed.yaml") as f:
            return yaml.safe_load(f)


def info_table(entries: list[DatabaseEntry]) -> str:
    header = """\
.. list-table::
    :header-rows: 1

    * - 
      - Elements
      - # Atoms
      - # Structures
      - License
      - Year
"""

    rows = []
    for entry in entries:
        entry_info = get_info(entry.name)

        if entry.license is None:
            license = "None"
        else:
            license = f"`{entry.license} <{LICENSE_URLS[entry.license]}>`_"

        rows.append(
            f"""\
    * - :doc:`{entry.name} <../datasets/{entry.name}>`
      - {", ".join(entry_info["elements"])}
      - {entry_info["n_atoms"]:,}
      - {entry_info["n_structures"]:,}
      - {license}
      - {entry.year}"""
        )

    return header + "\n".join(rows)


def summary_cards(entries: list[DatabaseEntry]) -> str:
    parts = []
    for entry in entries:
        description = lpad(entry.description)
        parts.append(
            f"""
.. grid-item-card::
    :class-item: info-card

    .. centered:: :doc:`{entry.name} <../datasets/{entry.name}>`

{description}
"""
        )

    grid = """\
.. grid:: 2

""" + "\n".join(lpad(p) for p in parts)
    return grid
