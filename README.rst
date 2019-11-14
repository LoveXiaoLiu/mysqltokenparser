================
mysqltokenparser
================


.. image:: https://img.shields.io/pypi/v/mysqltokenparser.svg
        :target: https://pypi.python.org/pypi/mysqltokenparser

.. image:: https://img.shields.io/travis/LoveXiaoLiu/mysqltokenparser.svg
        :target: https://travis-ci.org/LoveXiaoLiu/mysqltokenparser

.. image:: https://readthedocs.org/projects/mysqltokenparser/badge/?version=latest
        :target: https://mysqltokenparser.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/LoveXiaoLiu/mysqltokenparser/shield.svg
     :target: https://pyup.io/repos/github/LoveXiaoLiu/mysqltokenparser/
     :alt: Updates



A awesome tool that easy to get MySQL's tokens.


* Free software: MIT license
* Documentation: https://mysqltokenparser.readthedocs.io.


Quickstart
----------

0x01 安装

.. code:: shell

   pip install mysqltokenparser

0x02 使用教程

.. code:: python

    import mysqltokenparser as mtp

    sql = u"""
        ALTER TABLE t_a_gun2_6_dw_pfm_emp_cm ADD INDEX idx_eob_date(empid_org_bus (200),pfm_date);
    """

    tokens = mtp.mysql_token_parser(sql)
    print tokens
    #{
    #    "type": "ddl",
    #    "data": {
    #        "type": "altertable",
    #        "data": {
    #            "tablename": "t_a_gun2_6_dw_pfm_emp_cm",
    #            "alter_data": [{
    #                "type": "addindex",
    #                "data": {
    #                    "indexdefinition": {
    #                        "columnnames": ["empid_org_bus", "pfm_date"]
    #                    },
    #                    "indexname": "idx_eob_date"
    #                }
    #            }]
    #        }
    #    }
    #}


Features
--------

* Current version only support create and alter table
* TODO：SUPPORT MORE SQL STATEMENTS

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
