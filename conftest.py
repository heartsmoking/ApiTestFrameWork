#!/usr/bin/env python
# -*- coding:utf-8 -*-
# conf for global
"""
Author: ZhaoFeng
Email: 

Date: 2021/4/15 9:24
"""
from datetime import datetime
import pytest
from py.xml import html


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
    cells.insert(-2, html.td(report.exec_time, class_='col-time'))
    cells.pop()


def pytest_html_results_table_html(report, data):
    """去掉默认的日志捕获，只要异常说明"""
    # 这个没找到好的办法，自从吧pytest和pytest-html升级之后报告中输出的日志就变多了，
    # 以前只有Captured log call这一部分来着，现在没找到好办法解决,现在这个办法只是乱搞
    tt =  data[0]
    stt = '------------------------------Captured'
    slog = 'Captured log call'
    slog_n = -3
    for i in range(len(tt)):
        if isinstance(tt[i], str):
            if slog in tt[i]:
                slog_n = i
                break

    for i in range(len(tt)):
        if isinstance(tt[i], str):
            if stt in tt[i]:
                del tt[i:slog_n]
                break
    del data[:]
    if report.passed:

        data.append(html.div("No log output captured.", class_="empty log"))
    else:
    #     # failtext = [x for x in report.longreprtext.split('\n')]
    #     # fail_p = report.longreprtext
    #     fail_p = '<br/>'.join(qq)
    #     data.append(html.div(fail_p, class_="failed log"))
        data.append(tt)

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 设置执行时间的显示格式
    # setattr(report, "duration_formatter", "%H:%M:%S.%f")

    report.description = str(item.funcargs.get('description', None))
    report.URL = str(item.funcargs.get('url', None))
    report.assertions = str(item.funcargs.get('verify', None))
    runtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report.exec_time = runtime


    # 获取文档描述字符串，pytest和unittest用例获取方式不一样
    # pytest 的变量
    # report.description = str(item.function.__doc__)
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