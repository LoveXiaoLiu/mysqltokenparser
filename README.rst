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



Get the mysql's tokens by the tool.


* Free software: MIT license
* Documentation: https://mysqltokenparser.readthedocs.io.


Quickstart
----------

示例代码::

   pip install mysqltokenparser1

   import mysqltokenparser as mtp
   mtp.mysql_token_parser("select name from student")
   tn = mtp.get_tablename()
   in = mtp.get_indexname()
   cn = mtp.get_columnnames()
   print "table name:", tn
   print "index name:", in
   print "column name:", cn


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
