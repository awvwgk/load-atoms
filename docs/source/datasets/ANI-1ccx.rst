.. This file is autogenerated by dev/scripts/generate_page.py

ANI-1ccx
========

.. grid:: 1 1 2 2
    
    .. grid-item::

        .. raw:: html
            :file: ../_static/visualisations/ANI-1ccx.html

    .. grid-item::
        :class: info-card

        The ANI-1ccx dataset comprises an "optimally spanning" subset of the :doc:`/datasets/ANI-1x` dataset,
        with each structure being re-labelled with the total structure energy using the 
        "gold standard" CCSD(T)/CBS level of theory. Internall, files are downloaded from
        `FigShare <https://springernature.figshare.com/collections/The_ANI-1ccx_and_ANI-1x_data_sets_coupled-cluster_and_density_functional_theory_properties_for_molecules/4712477>`__.
        


.. code-block:: pycon

    >>> from load_atoms import load_dataset
    >>> load_dataset("ANI-1ccx")
    ANI-1ccx:
        structures: 489,571
        atoms: 6,763,288
        species:
            H: 45.52%
            C: 29.58%
            N: 15.30%
            O: 9.60%
        properties:
            per atom: (dft_forces)
            per structure: (1x_idx, cc_energy, dft_dipole, dft_energy)
    


License
-------

This dataset is licensed under the `CC0 <https://creativecommons.org/publicdomain/zero/1.0/>`_ license.


Citation
--------

If you use this dataset in your work, please cite the following:

.. code-block:: latex
    
    @article{Smith-19-07,
        title = {
            Approaching Coupled Cluster Accuracy with a 
            General-Purpose Neural Network Potential 
            through Transfer Learning
        },
        author = {
            Smith, Justin S. and Nebgen, Benjamin T. and Zubatyuk, Roman 
            and Lubbers, Nicholas and Devereux, Christian and Barros, Kipton 
            and Tretiak, Sergei and Isayev, Olexandr and Roitberg, Adrian E.
        },
        year = {2019},
        journal = {Nature Communications},
        volume = {10},
        number = {1},
        pages = {2903},
        doi = {10.1038/s41467-019-10827-4},
    }
    
    @article{Smith-20-05,
        title = {
            The ANI-1ccx and ANI-1x Data Sets, Coupled-Cluster
            and Density Functional Theory Properties for Molecules
        },
        author = {
            Smith, Justin S. and Zubatyuk, Roman and Nebgen, Benjamin and 
            Lubbers, Nicholas and Barros, Kipton and Roitberg, Adrian E. and 
            Isayev, Olexandr and Tretiak, Sergei
        },
        year = {2020},
        journal = {Scientific Data},
        volume = {7},
        number = {1},
        pages = {134},
        doi = {10.1038/s41597-020-0473-z},
    }
    
    
    @article{Smith-18-05,
        title = {
            Less Is More: Sampling Chemical Space with Active Learning
        },
        author = {
            Smith, Justin S. and Nebgen, Ben and Lubbers, Nicholas and 
            Isayev, Olexandr and Roitberg, Adrian E.
        },
        year = {2018},
        journal = {The Journal of Chemical Physics},
        volume = {148},
        number = {24},
        doi = {10.1063/1.5023802},
    }


Properties
----------

**Per-atom**:

.. list-table::
    :header-rows: 1

    * - Property
      - Units
      - Type
      - Description
    * - :code:`dft_forces`
      - eV/Å
      - :class:`ndarray(N, 3) <numpy.ndarray>`
      - force vectors (as labelled with :math:`\omega`\ B97x/6-31G(d))


**Per-structure**:
    
.. list-table::
    :header-rows: 1

    * - Property
      - Units
      - Type
      - Description
    * - :code:`cc_energy`
      - eV
      - :class:`~float64`
      - energy of the structure (as labelled with CCSD(T)/CBS)

    * - :code:`dft_energy`
      - eV
      - :class:`~float64`
      - energy of the structure (as labelled with :math:`\omega`\ B97x/6-31G(d))

    * - :code:`dft_dipole`
      - e Å
      - :class:`ndarray(3,) <numpy.ndarray>`
      - dipole moment of the structure (as labelled with :math:`\omega`\ B97x/6-31G(d))

    * - :code:`1x_idx`
      - 
      - :class:`~int`
      - index of the structure in the :doc:`/datasets/ANI-1x` dataset



Miscellaneous information
-------------------------

``ANI-1ccx`` is imported as an 
:class:`~load_atoms.atoms_dataset.LmdbAtomsDataset`:

.. dropdown:: Importer script for :code:`ANI-1ccx`

    .. literalinclude:: ../../../src/load_atoms/database/importers/ani_1ccx.py
       :language: python



.. dropdown:: :class:`~load_atoms.database.DatabaseEntry` for :code:`ANI-1ccx`

    .. code-block:: yaml

        name: ANI-1ccx
        year: 2019
        category: Benchmarks
        license: CC0
        minimum_load_atoms_version: 0.3
        format: lmdb
        description: |
            The ANI-1ccx dataset comprises an "optimally spanning" subset of the :doc:`/datasets/ANI-1x` dataset,
            with each structure being re-labelled with the total structure energy using the 
            "gold standard" CCSD(T)/CBS level of theory. Internall, files are downloaded from
            `FigShare <https://springernature.figshare.com/collections/The_ANI-1ccx_and_ANI-1x_data_sets_coupled-cluster_and_density_functional_theory_properties_for_molecules/4712477>`__.
        citation: |
            @article{Smith-19-07,
                title = {
                    Approaching Coupled Cluster Accuracy with a 
                    General-Purpose Neural Network Potential 
                    through Transfer Learning
                },
                author = {
                    Smith, Justin S. and Nebgen, Benjamin T. and Zubatyuk, Roman 
                    and Lubbers, Nicholas and Devereux, Christian and Barros, Kipton 
                    and Tretiak, Sergei and Isayev, Olexandr and Roitberg, Adrian E.
                },
                year = {2019},
                journal = {Nature Communications},
                volume = {10},
                number = {1},
                pages = {2903},
                doi = {10.1038/s41467-019-10827-4},
            }
        
            @article{Smith-20-05,
                title = {
                    The ANI-1ccx and ANI-1x Data Sets, Coupled-Cluster
                    and Density Functional Theory Properties for Molecules
                },
                author = {
                    Smith, Justin S. and Zubatyuk, Roman and Nebgen, Benjamin and 
                    Lubbers, Nicholas and Barros, Kipton and Roitberg, Adrian E. and 
                    Isayev, Olexandr and Tretiak, Sergei
                },
                year = {2020},
                journal = {Scientific Data},
                volume = {7},
                number = {1},
                pages = {134},
                doi = {10.1038/s41597-020-0473-z},
            }
        
        
            @article{Smith-18-05,
                title = {
                    Less Is More: Sampling Chemical Space with Active Learning
                },
                author = {
                    Smith, Justin S. and Nebgen, Ben and Lubbers, Nicholas and 
                    Isayev, Olexandr and Roitberg, Adrian E.
                },
                year = {2018},
                journal = {The Journal of Chemical Physics},
                volume = {148},
                number = {24},
                doi = {10.1063/1.5023802},
            }
        
        
        per_atom_properties:
            dft_forces:
                desc: force vectors (as labelled with :math:`\omega`\ B97x/6-31G(d))
                units: eV/Å
        per_structure_properties:
            cc_energy:
                desc: energy of the structure (as labelled with CCSD(T)/CBS)
                units: eV
            dft_energy:
                desc: energy of the structure (as labelled with :math:`\omega`\ B97x/6-31G(d))
                units: eV
            dft_dipole:
                desc: dipole moment of the structure (as labelled with :math:`\omega`\ B97x/6-31G(d))
                units: e Å
            1x_idx:
                desc: index of the structure in the :doc:`/datasets/ANI-1x` dataset
        
        representative_structure: 413_000
        
        
