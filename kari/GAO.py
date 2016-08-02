from Submission.models import *
from User.models import *
from Contest.models import *
import os

def sad(cid):
    c = Contest.getById(cid)
    studentList = c.course_class.getAllStudents()
    for u in studentList:
        gao(c,u)

def gao(c,u):
    subList = Submission.submissionList(c = c, u = u)
    contestDir = '/home/buptacm/'+str(c.cid)
    userDir = contestDir+'/'+str(u)
    try:
        os.mkdir(contestDir)
    except:
        pass
    try:
        os.mkdir(userDir)
    except:
        pass
    for sub in subList:
        subDir = userDir+'/'+str(sub)+'.txt'
        f = open(subDir,'w')
        res = eval(sub.other_info)['status']
        f.write('//'+res+'\n')
        f.write(open(sub.code_file).read())
