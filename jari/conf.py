# -*- coding: utf-8 -*-
import resource
import cptrace
import syscall

#linux only rlimit
#define in /usr/include/{linux ver}/bits/resource.h
resource.RLIMIT_SIGPENDING = 11
resource.RLIMIT_MSGQUEUE = 12
resource.RLIMIT_RPTRIO = 14
resource.RLIMIT_PTTIME = 15

#linux only ptrace
#define in /usr/include/{linux ver}/sys/ptrace.h
cptrace.PTRACE_TRACEME = 0
cptrace.PTRACE_PEEKUSER = 3
cptrace.PTRACE_KILL = 8
cptrace.PTRACE_GETREGS = 12
cptrace.PTRACE_SYSCALL = 24
cptrace.ORIG_EAX = 11


class JudgeConf(object):

    @classmethod
    def init(cls):
        pass

    QUEUE_HOST = 'localhost' # queue host ip
    QUEUE_NAME = 'judge' # judge request queue name

    OLE_THRESHOLD = 4096
    OLE_RATIO = 5

    LANG = ('gcc', 'g++', 'java', 'python2',)

    SUB_STATUS = {
            'init':'init',
            'done':'done',
            'compiling':'compiling',
            'compilation error':'compilation error',
            'judging':'judging',
            'mle':5,  # total memory limit exceed unused now
            'tle':6,  # total time limit exceed unused now
            }

    JUDGE_RES = {
            'init':'init',
            'mle':'mle',
            'tle':'tle',
            're':'re',
            'wa':'wa',
            'pe':'pe',
            'ac':'ac',
            'se':'se',  #undefined result, system error
            'ole':'ole',
            }

#filename and filepath
    SUB_PATH = '/home/buptacm/oj/media/submission/'  # default code path
    CASE_PATH = '/home/buptacm/oj/media/data/'  # default data path {CASE_PATH}/{pid}/{x}.in and {x}.out
    RUN_PATH = '/home/buptacm/oj/judge/jari/run/'

    SRC_PREFIX = {
            'gcc':'src',
            'g++':'src',
            'java':'Main',
            'python':'src',
            }

    SRC_SUFFIX = {
            'gcc':'c',
            'g++':'cpp',
            'java':'java',
            'python':'py',
            }
   
    @classmethod
    def getSrcName(cls, lang):
        return '.'.join([cls.SRC_PREFIX[lang], cls.SRC_SUFFIX[lang]])

    def getSrcPath(cls, lang):
        return cls.RUN_PATH+cls.getSrcName(lang)

    @classmethod
    def getSubPath(cls, sid):
        return cls.SUB_PATH+str(sid)

    @classmethod
    def getExecPathO(cls):
        return cls.RUN_PATH+'homura.out'

    @classmethod
    def getCasePath(cls, pid):
        return cls.CASE_PATH+str(pid)+'/'

    @classmethod
    def getCasePathI(cls, pid, case_id):
        return cls.getCasePath(pid)+str(case_id)+'.in'
    
    @classmethod
    def getCasePathO(cls, pid, case_id):
        return cls.getCasePath(pid)+str(case_id)+'.out'

#COMPILE PARAM

    #resource limit to compiler
    CMPL_RLIM = {
            'RLIMIT_CPU':(5, 5),
            }

    #compiler execution
    CMPL_CMD = {
            'gcc':'gcc',
            'g++':'g++',
            'java':'javac',
            'python':None,
            }

    #compiling option
    CMPL_PARAM = {  
            'gcc': [
                CMPL_CMD['gcc'],
                '-o',
                RUN_PATH+SRC_PREFIX['gcc'],
                RUN_PATH+'.'.join([SRC_PREFIX['gcc'], SRC_SUFFIX['gcc']]),
                #'-O2',
                '-DONLINE_JUDGE',
                '-std=c99',
                '-lm',
                ],

            'g++': [
                CMPL_CMD['g++'],
                '-o',
                RUN_PATH+SRC_PREFIX['g++'],
                RUN_PATH+'.'.join([SRC_PREFIX['g++'], SRC_SUFFIX['g++']]),
                '-O2',
                '-DONLINE_JUDGE',
                ],

            'java': [
                CMPL_CMD['java'],
                RUN_PATH+'.'.join([SRC_PREFIX['java'], SRC_SUFFIX['java']]),
                '-d',
                RUN_PATH,
                ],

            'python2': None,
            }
    
#JUDGE PARAM

    #runtime rlimit. the first number of the tuple for soft limit, while the second for hard limit
    EXEC_RLIM = {
            'gcc': {
                resource.RLIMIT_NPROC:(1, 1),  #limit for number of processor
                resource.RLIMIT_FSIZE:(1073741824, 1073741824),  #maximum size of files the process may create
                resource.RLIMIT_CORE:(0, 0),  #core file size, 0 for no core file
                },
            'g++': {
                resource.RLIMIT_NPROC:(1, 1),
                resource.RLIMIT_FSIZE:(1073741824, 1073741824),
                resource.RLIMIT_CORE:(0, 0),
                },
            'java': {
                #resource.RLIMIT_NPROC:(1, 1),  #java vm uses multithreads
                resource.RLIMIT_FSIZE:(1073741824, 1073741824),
                resource.RLIMIT_CORE:(0, 0),
                },
            'python': None
            }
    
    #execution command
    EXEC_CMD = {
            'gcc': RUN_PATH+SRC_PREFIX['gcc'],
            'g++': RUN_PATH+SRC_PREFIX['g++'],
            'java': 'java',
            'python': 'python',
            }

    #execution param
    EXEC_PARAM = {
            'gcc': [EXEC_CMD['gcc'],],
            'g++': [EXEC_CMD['g++'],],
            'java': [
                EXEC_CMD['java'],
                '-classpath',
                RUN_PATH,
                SRC_PREFIX['java'],
            ],
            'python': [EXEC_CMD['python'], RUN_PATH+SRC_PREFIX['python']],
            }

    #time limit ratio
    EXEC_TL_RATIO = {
            'gcc': 1,
            'g++': 1,
            'java': 3,
            'python2': 2,
            }

    #memory limit ratio
    EXEC_ML_RATIO = {
            'gcc': 1,
            'g++': 1,
            'java': 2,
            'python2': 2,
            }

    #execution minimum time limit in millisecond
    EXEC_MIN_TL = {
            'gcc': 16,
            'g++': 16,
            'java': 16,
            'python2': 16,
            }

    #execution minimum memory limit in kb
    EXEC_MIN_ML = {
            'gcc': 1024,
            'g++': 1024,
            'java': 1024,
            'python2': 1024,
            }

    #maximum memory for execution
    EXEC_MAX_MEM = 1048576*1024

    # basic syscall policy
    SYSCALL = syscall.SYSCALL

    # ALL, NO, or extend as you may implement
    POLICY = {
            'gcc': 'ALL',
            'g++': 'ALL',
            'java': 'NO',
            'python': 'NO',
            }
