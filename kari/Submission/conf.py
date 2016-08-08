
# coding: utf
# constant field
STATUS_ABBR = (
        ('Pending', 'Pending'),
        ('Compiling', 'Compiling'),
        ('Compile Error', 'Compile Error'),
        ('Judging', 'Judging'),
        ('System Error', 'System Error'),
        ('Accepted', 'Accepted'),
        ('Presentation Error', 'Presentation Error'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Runtime Error', 'Rhntime Error'),
        ('Time Limit Exceed', 'Time Limit Exceed'),
        ('Memory Limit Exceed', 'Memory Limit Exceed'),
        ('Output Limit Exceed', 'Output Limit Exceed'),
        ('Rejudging', 'Rejudging'),
        )

SUB_STATUS = {
        'init':'Init',
        'done':'Done',
        'compiling':'Compiling',
        'compilation error':'Compile Error',
        'judging':'Judging',
        'mle':5,  # total memory limit exceed unused now
        'tle':6,  # total time limit exceed unused now
        }

JUDGE_RES = {
        'init':'Init',
        'mle':'Memory Limit Exceed',
        'tle':'Time Limit Exceed',
        're':'Runtime Error',
        'wa':'Wrong Answer',
        'pe':'Presentation Error',
        'ac':'Accepted',
        'se':'System Error',#undefined result, system error
        'ole':'Output Limit Exceed',#undefined result, system error
        }

JUDGE_RES_CN = {
        'init':u'初始化',
        'mle': u'超过内存限制',
        'tle': u'超过时间限制',
        're': u'运行时错误',
        'wa': u'答案错误',
        'pe': u'格式错误',
        'ac': u'通过',
        'se': u'系统错误',
        'ole': u'超过输出限制',
        }

FILE_TYPE = { 'gcc': 'c',
        'g++': 'cpp',
        'java': 'java'}

