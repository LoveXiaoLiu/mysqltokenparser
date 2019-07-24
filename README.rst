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
        CREATE TABLE `aaa`.`t_zcm_operation_luck_award_record` (
          `id` bigint(20) NOT NULL,
          `operation_seq` varchar(30) NOT NULL,
          `award_user_id` bigint(20) NOT NULL,
          `award_type` int(11) DEFAULT NULL,
          `award_id` varchar(40) DEFAULT NULL UNIQUE KEY,
          `award_content` varchar(20)  DEFAULT NULL,
          `award_reason` varchar(30)  DEFAULT NULL,
          `award_source` int(11) DEFAULT NULL,
          `state` tinyint(4) NOT NULL PRIMARY KEY,
          `addtime` datetime NOT NULL,
          `updatetime` datetime NOT NULL,
          `ip` varchar(50)  DEFAULT NULL,
          `imei` varchar(50)  DEFAULT NULL,
          `intext` int(11) DEFAULT NULL,
          `longext` bigint(20) DEFAULT NULL,
          `strext` varchar(200)  DEFAULT NULL,
          PRIMARY KEY (id),
          UNIQUE KEY `idx_op_seq_uid_type` (`operation_seq`,`award_user_id`,`award_type`),
          KEY `idx_op_uid_type` (`award_user_id`,`award_type`),
          KEY `idx_op_uid_sss` (longext(10))
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """

    token_obj = mtp.mysql_token_parser(sql)
    tokens = token_obj.get_tokens()
    print tokens
    # {
    #     'uniquekey': ['award_id'],
    #     'columnnames': [u'id', u'operation_seq', u'award_user_id', u'award_type', u'award_id', u'award_content', u'award_reason', u'award_source', u'state', u'addtime', u'updatetime', u'ip', u'imei', u'intext', u'longext', u'strext'],
    #     'tablenames': [u'aaa.t_zcm_operation_luck_award_record'],
    #     'sqltype': ['ddl'],
    #     'primarykey': ['state'],
    #     'indexnames': [u'id', u'operation_seq,award_user_id,award_type', u'award_user_id,award_type', u'longext(10)']
    # }


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
