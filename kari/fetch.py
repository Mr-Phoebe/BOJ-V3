from Submission.models import *
from Contest.models import *
from kari.settings import *

lower_bound = 84778
upper_bound = 88174

contest = Contest.getById(167)

for id in xrange(lower_bound, upper_bound + 1):
    s = Submission.getById(id)
    p = s.problem_index
    if (p.contest == contest):
        import os
        os.system('cp /home/buptacm/oj/media/submission/%d /home/buptacm/backup_codes' % id)
        print id
