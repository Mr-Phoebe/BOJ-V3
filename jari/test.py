#!/usr/bin/env python
import time
from compile import Compile
from sub import Sub
from judge import Judge
c = Compile()
s = Sub()
s.sid = 1
s.lang = 'g++'
c.compile(s)
print 'ce:'+s.ce
print 'status:'+str(s.status)
s.pid = 15
s.case_cnt = 1
s.time_lim = 1000
s.mem_lim = 10240
s.case_lim = [{'time':1000, 'mem':4000},]
j = Judge()
j.judge(s)
print 'status:'+str(s.status)
print s.case_res

