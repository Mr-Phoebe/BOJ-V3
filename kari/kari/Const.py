# coding: utf-8
class Const():
    """
    Constants for the whole system
    """

    # Public Const
    LANG = (
            ( 'gcc', 'GNU C'),
            ( 'g++', 'GNU C++'),
            ( 'java', 'java'),
            #( 'Python', 'Python'),
            )

    BRUSH = {
            'gcc': 'c',
            'g++': 'cpp',
            'java': 'java',
    }

    # User Const
    USERNAME_MAX_LENGTH = 30
    USERNAME_MIN_LENGTH = 3
    NICKNAME_MAX_LENGTH = 30
    NICKNAME_MIN_LENGTH = 3
    PASSWD_MIN_LENGTH = 6
    PASSWD_MAX_LENGTH = 30
    GROUPNAME_MIN_LENGTH = 1
    GROUPNAME_MAX_LENGTH = 30
    SCHOOLNAME_MAX_LENGTH = 20
    SCHOOLABBR_MAX_LENGTH = 20
    GROUPNAME_MAX_LENGTH = 20
    UNIVNAME_MAX_LENGTH = 30
    UNIVABBR_MAX_LENGTH = 10
    EMAIL_MAX_LENGTH = 30
    CACHE_TIME_BOARD = 25
    CACHE_TIME_FIRST = 15
    CACHE_TIME_CLAFI = 30

    LOGIN_FAIL = u'用户名或密码不正确！'
    USERNAME_NOT_EXIST = u'用户名不存在！'
    USERNAME_ILLEGAL = u'用户名非法！用户名长度应在%d到%d之间且仅包含a-z,0-9,_'%(USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH)
    NICKNAME_ILLEGAL = u'昵称非法！用户名长度应在%d到%d之间且仅包含a-z,0-9,_'%(NICKNAME_MIN_LENGTH, NICKNAME_MAX_LENGTH)
    USERNAME_DUP = u'用户名已存在！'
    UNIVERSITY_NOT_EXIST = u'ID为{0}的学校不存在！'
    SCHOOL_NOT_EXIST = u'ID为{0}的学院不存在！'
    GROUP_NOT_EXIST = u'ID为{0}的分班不存在！'
    USER_NOT_IN_GROUP = u'该用户不存在相应的组中！'
    NOT_LOGGED_IN = u'您尚未登录！'
    LOGGED_IN = u'您已经登录过了！'
    PASSWD_INCONSISTENT = u'两次输入的密码不一致！'
    PASSWD_INCORRECT = u'密码不正确！'
    PASSWD_ILLEGAL = u'密码非法！密码长度应在%d到%d之间。' % (PASSWD_MIN_LENGTH, PASSWD_MAX_LENGTH)
    GROUPNAME_ILLEGAL = u'群组名称非法！名称长度应在%d到%d之间。' % (GROUPNAME_MIN_LENGTH, GROUPNAME_MAX_LENGTH)
    PASSWD_ILLEGAL = u'密码非法！密码长度应在%d到%d之间。' % (PASSWD_MIN_LENGTH, PASSWD_MAX_LENGTH)
    PASSWD_SALT = 'b2U1p9ta@cm#daiNIUshouSUno.1'
    ILLEGAL_SCHOOL_NAME = u'非法的学校名称！'
    ILLEGAL_SCHOOL_ABBR = u'非法的学校简称！'
    GENDER_CHOICE = (
                ('male', 'male'),
                ('female', 'female'),
                ('secret', 'secret'),
                )
    USER_PRIV_CHOICE = (
                ('student', 'student'),
                ('courseclass', 'courseclass'),
                ('course', 'course'),
                ('school', 'school'),
                ('university', 'university'),
                )

    # Contest Const
    CONTEST_PER_PAGE = 50 
    CONTEST_PAGES_AFTER = 5
    CONTEST_PAGES_BEFORE = 6
    CONTEST_TITLE_ERR = u'考试标题长度不能大于128!'
    CONTEST_TIME_ERR = u'考试开始时间不能早于当前时间!'
    CONTEST_END_TIME_ERR = u'考试结束时间不能早于当前时间'
    CONTEST_LEN_ERR = u'考试持续时间必须大于0!'
    CONTEST_BOARD_ERR = u'排行榜持续时间必须大于0!'
    CONTEST_PROB_ERR = u'不能使用不合法的题目!'
    CONTEST_NOTICE_TITLE_ERR = u'考试公告长度不能大于128!'
    CONTEST_NOT_EXIST = u'考试不存在！'
    CONTEST_PROB_NOT_EXIST = u'考试题目不存在！'
    CONTEST_NOTICE_NOT_EXIST = u'考试公告不存在！'
    NOT_PVLG = u'您没有足够的权限！'
    
    LANG_MASK = {
        'gcc': 1,
        'g++': 2,
        'java': 4,
    }

    # Problem Const
    PROBLEM_PER_PAGE = 100
    PROBLEM_DATA_PATH = "/var/www/oj/data/"

    # Submission Const
    SUBMISSION_CODE_PATH = '/var/www/oj/submission/'
    GENERAL_SUBMISSION_CODE_PATH = '/var/www/oj/general_submission/'
    SUBMISSION_TMP_PATH = '/var/www/oj/sub_temp/'
    STATUS_PER_PAGE = 50
    STATUS = (
            ( 'PD', 'Pending'),
            ( 'SE', 'System Error'),
            ( 'CL', 'Compiling'),
            ( 'CE', 'Compilation Error'),
            ( 'JD', 'Judging'),
            ( 'AC', 'Accepted'),
            ( 'PE', 'Presentation Error'),
            ( 'WA', 'Wrong Answer'),
            ( 'RE', 'Runtime Error'),
            ( 'TLE', 'Time Limit Exceed'),
            ( 'MLE', 'Memory Limit Exceed'),
            ( 'OLE', 'Output Limit Exceed'),
            ( 'EXT', 'Extended Judge Result'),
            )
    # translation
    STATUS_CN = {
            'Accepted': u'通过',
            'Presentation Error': u'格式错误',
            'Wrong Answer': u'答案错误',
            'Time Limit Exceed': u'超过时间限制',
            'Memory Limit Exceed': u'超过内存限制',
            'Runtime Error': u'运行时错误',
            'Compile Error': u'编译错误',
            'Output Limit Exceed': u'超过输出限制',
            'Pending': u'等待评测',
            'Judging': u'评测中',
            'Rejudging': u'重新评测中',
            'Compiling': u'编译中',
            'System Error': u'系统错误',
            }

    STATUS_COLOR = {
            'Accepted': 'status-ac',
            'Presentation Error': 'status-pe',
            'Wrong Answer': 'status-wa',
            'Time Limit Exceed': 'status-tle',
            'Memory Limit Exceed': 'status-mle',
            'Output Limit Exceed': 'status-ole',
            'Runtime Error': 'status-re',
            'Compile Error': 'status-ce',
            'Pending': 'status-pd',
            'Judging': 'status-jd',
            'Rejudging': 'status-rej',
            'Compiling': 'status-cl',
            'System Error': 'status-se',
            }

    # Course Const
    COURSE_NOT_EXIST = u'ID为{0}的课程不存在'
    USER_IS_NOT_ADMIN = u'权限不足！用户{0}不是管理员！'
    USER_CAN_NOT_DO_COURSE = u'权限不足！用户{0}没有操作课程的权限！'
    USER_CAN_NOT_DO_COURSECLASS = u'权限不足！用户{0}没有操作课程分班的权限！'
    USER_NOT_GROUP_MEMBER = u'用户{0}不是该班的分组成员'
    COURSECLASS_NOT_EXIST = 'ID为{0}的课程考试不存在！'
    UNIQUE_TOGETHER_VALIDATION_FAILED = u'联合unique约束不满足！'
    STUDENT_PER_PAGE = 200
    GROUP_PER_PAGE = 50
    COURSE_PER_PAGE = 50
    CLASS_PER_PAGE = 50
    
    RANKLIST_PER_PAGE = 50

    ERROR_PAGE = "error.html"
    NEW_ERROR_PAGE = "newtpl/error.html"

    CHEAT_PER_PAGE = 25
    CHEAT_DEFAULT_THRESHOLD = 90
