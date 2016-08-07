from User.models import User, Group
from Statistic.models import Board
from Contest.models import Contest, ContestProblem
from Problem.models import Problem
from Submission.models import Submission
from kari.const import Const
from rest_framework import serializers
import copy, math

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'username', 'nickname', 'priv', 'group_set')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'users')

class BoardSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField('get_board')

    def get_board(self, b):
        c = b.contest
        allSubmission = Submission.submissionList(c=c).order_by('sid')
        allUser = c.course_class.getAllStudents()
        allContestProblem = c.getContestProblem()

        problemInfos = {cp.problem_index:{'idx': cp.problem_index, 'total_score': cp.getScore(), 'score': 0, 'ac': 0} for cp in allContestProblem}
        userInfos = { userInfo.uid: {
            'uid': userInfo.uid,
            'username': userInfo.username,
            'nickname': userInfo.nickname,
            'score': 0,
            'problem_infos': copy.deepcopy(problemInfos)
            } for userInfo in allUser}

        for s in allSubmission:
            uid = s.user.uid
            if not uid in userInfos:
                continue
            idx = s.problem_index.problem_index
            if userInfos[uid]['problem_infos'][idx]['ac'] > 0 or s.status in Const.STATUS_NO_USE:
                continue
            submissionTime = int(math.ceil((s.submission_time-c.start_time).total_seconds()/60))
            if s.status == 'Accepted':
                userInfos[uid]['problem_infos'][idx]['ac'] = 1 - userInfos[uid]['problem_infos'][idx]['ac']
                userInfos[uid]['problem_infos'][idx]['ac_time'] = submissionTime
                userInfos[uid]['problem_infos'][idx]['score'] = max(problemInfos[idx]['total_score'] - problemInfos[idx]['total_score'] / 250 * submissionTime - 50 * (userInfos[uid]['problem_infos'][idx]['ac'] - 1), problemInfos[idx]['total_score'] / 250 * 75);
                userInfos[uid]['score'] += userInfos[uid]['problem_infos'][idx]['score']
            else:
                userInfos[uid]['problem_infos'][idx]['ac'] -= 1
                userInfos[uid]['problem_infos'][idx]['score'] = userInfos[uid]['problem_infos'][idx]['ac']

        problemInfos = sorted(problemInfos.values(), key=lambda problem: problem['idx'])
        userInfos = sorted(userInfos.values(), key=lambda user: user['score'], reverse=True)
        curRank = 0
        for idx, user in enumerate(userInfos):
            if idx == 0 or user['score'] != userInfos[idx-1]['score']: curRank += 1
            user['rank'] = curRank
        return {'problem_infos': problemInfos, 'user_infos': userInfos}

    class Meta:
        model = Board
        fields = ('board',)
