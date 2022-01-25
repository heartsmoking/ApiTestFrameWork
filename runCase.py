#!/user/bin/env python
#coding=utf-8
'''
@project : ApiTestFrameWork
@author  : ZhaoFeng
#@file   : runCase.py
#@ide    : PyCharm
#@time   : 2022-01-22 15:27:00
'''

'''
    pytest用例执行文件
'''
if __name__ == '__main__':
    import pytest
    import time
    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    pytest.main(['--show-capture=stderr','./test_case/test_case.py','--html=report/{}_report.html'.format(now)])
    # pytest.main(['--show-capture=log','-r','A','./test_case/test_case.py'])
    # --capture=sys 支持 sys和fd默认fd  使用-s参数则关闭 -s就相当于--capture=no
    # import unittest
    # import os
    # from HTMLTestRunner import HTMLTestRunner
    # base_dir = os.path.abspath(os.path.dirname(__file__))
    # case_dir = os.path.join(base_dir, "test_case")
    # testcases = unittest.TestLoader().discover(case_dir,pattern='test_case.py')
    # report_file = os.path.join(base_dir, "report", '{}_report.html'.format(now))
    # with open(report_file, 'wb') as report:
    #     runner = HTMLTestRunner.HTMLTestRunner(stream=report, title='测试报告',description='注：为减少时间人力成本，提高转测质量，特每次对测试环境待发布的代码会对基础功能模块进行单元测试，进一步的提高测试效率,如下为用例执行结果，请查阅！')
    #     runner.run(testcases)
    # # runner = unittest.TextTestRunner()
    # # runner.run(testcases)