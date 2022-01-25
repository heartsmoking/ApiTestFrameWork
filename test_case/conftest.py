#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author: ZhaoFeng
Email: 

Date: 2022/1/21 17:27
"""
# conf for test_case
import pytest
from core.testBase import *
from pytest_check.check_methods import set_stop_on_fail

@pytest.fixture(scope='class',autouse=True)
def Request():
    Request = BaseTest()
    return Request


@pytest.fixture(scope='module',autouse=True)
def setup(request):
    def teardown():
        print("结束测试")
    request.addfinalizer(teardown)
    print("开始测试")
    # 如果不需要多重断言，一个断言失败后后续不再执行则设置True
    # set_stop_on_fail(True)





