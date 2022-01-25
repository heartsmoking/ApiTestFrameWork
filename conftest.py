#!/usr/bin/env python
# -*- coding:utf-8 -*-
# conf for global
"""
Author: ZhaoFeng
Email: 

Date: 2021/4/15 9:24
"""
import time
import pytest
from py.xml import html

runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# 显示__doc__内容
# def pytest_itemcollected(item):
#     par = item.parent.obj
#     node = item.obj
#     pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
#     suf = node.__doc__.strip() if node.__doc__ else node.__name__
#     if pref or suf:
#         item._nodeid = ' '.join((pref, suf))
# @pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "接 口 测 试 报 告"

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("测试报告")])

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(2, html.th('Test'))  #增加一列，解决用例参数入参为中文时正常显示
    cells.pop(3) #将原有的test删除
    cells.insert(3, html.th('URL'))
    cells.insert(4, html.th('Assertions'))
    cells.insert(-2, html.th('Exec_Time', class_='sortable time', col='time'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(3)
    cells.insert(3, html.td(report.URL))
    cells.insert(4, html.td(report.assertions))
    cells.insert(-2, html.td(runtime, class_='col-time'))
    cells.pop()


def pytest_html_results_table_html(report, data):
    """去掉默认的日志捕获，只要异常说明"""
    del data[:]
    if report.passed:
        data.append(html.div("No log output captured.", class_="empty log"))
    else:
        # failtext = [x for x in report.longreprtext.split('\n')]
        # fail_p = [html.p(p) for p in failtext]
        fail_p = report.longreprtext
        data.append(html.div(fail_p, class_="failed log"))

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 设置执行时间的显示格式
    # setattr(report, "duration_formatter", "%H:%M:%S.%f")
    # pytest 的变量
    report.description = str(item.funcargs.get('description', None))
    report.URL = str(item.funcargs.get('url', None))
    report.assertions = str(item.funcargs.get('verify', None))
    # unittest 的变量
    # report.description = item._testcase._testMethodDoc
    # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 设置编码显示中文


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")