newtheme-sphinx-theme
=====================

{{DESCRIPTION}}

Instalação
----------

.. code-block:: bash

   pip install newtheme-sphinx-theme

No ``conf.py`` do projeto:

.. code-block:: python

   html_theme = "newtheme_sphinx_theme"

Opções
------

.. list-table::
   :header-rows: 1

   * - Opção
     - Padrão
     - Uso
   * - ``primary_color``
     - ``""``
     - Cor principal (links e cabeçalho), ex.: ``"#1351b4"``
   * - ``github_url``
     - ``""``
     - Link do repositório no cabeçalho
   * - ``footer_text``
     - ``""``
     - Texto extra no rodapé (aceita HTML)

.. code-block:: python

   html_theme_options = {
       "primary_color": "#1351b4",
       "github_url": "https://github.com/org/repo",
   }
