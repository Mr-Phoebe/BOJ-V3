# -*- coding: utf-8 -*-

from django.db import models, transaction
from kari.const import Const
from django.core.exceptions import ValidationError
from Submission.models import Submission
from User.models import User
from Problem.models import Problem
import math
import re
from lcs import lcs
from conf import keywords, symbol, lang, rule
# Create your models here.


mapKeywords={"g++":{},"gcc":{},"java":{}}
mapSymbol={"g++":{},"gcc":{},"java":{}}
treeMem=[] 

class QUERY:
    uid=0
    similar_score=0.0
    lan=''
    subs=[]
    def __init__(self):
        self.uid = 0
        self.similar_score = 0.0
        self.subs=[]
        lan=''

class Cheat(models.Model):

    MAX_LEN = 128
    DB_QUERY_FAILED = -1
    DB_UPDATE_FAILED=-1
    DB_UPDATE_SUCCEED=1
    DB_QUERY_SUCCEED=1
    MAX_CODE_LENGTH=1055360
    QUERY_QUEENING=-1
    QUERY_JUDGING=0
    MAX_USERS=2

    #keywords=["int","long","for","while","if","else","break","continue","return","true","false","double","do","signed","unsigned"]
    #symbol=["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"]
    #mapKeyword={}
    #mapSymbol={}
    #treeMem=[] 

    ctid = models.AutoField(primary_key=True)
    contest_problem = models.ForeignKey('Contest.ContestProblem',related_name='anticheat_contest_problem')
    sub1 = models.ForeignKey('Submission.Submission',related_name='the_first_submission')
    sub2 = models.ForeignKey('Submission.Submission',related_name='the_second_submission')
    #contest_problem = models.CharField(max_length=100)
    #user1 = models.CharField(max_length=100)
    #user2 = models.CharField(max_length=Const.USERNAME_MAX_LENGTH+10)
    #code_file1 = models.FilePathField( path='code')
    #code_file2 = models.FilePathField( path='code')
    status = models.IntegerField()
    ratio = models.FloatField()

    class Meta:
        index_together = [
            ['sub1', 'sub2'],
        ]

    @classmethod
    def addRecord(cls, cp_set):

        formalSubmissions=[]
        for cp in cp_set:
            already = cls.objects.filter(contest_problem=cp)
            if already:
                continue
            submissions = Submission.submissionList(cp=cp, sta='Accepted').order_by('sid')
            usertable = {}
          #  submissions2 = []
            for ss in submissions:
                user = ss.user
                ok = usertable.get(user,0)
                if ok==0:
                    usertable[user] = ss.sid
            for i in submissions:
                if i.sid!=usertable[i.user]:
                    continue
                for j in submissions:
                    if j.sid==usertable[j.user] and i.sid<j.sid and i.code_language==j.code_language and i.user!=j.user:
                        ct = Cheat()
                        ct.contest_problem = cp
                        ct.sub1 = i
                        ct.sub2 = j
                        ct.status = -1
                        ct.ratio = 0
                        formalSubmissions.append(ct)
                        #ct.save()
        cls.objects.bulk_create(formalSubmissions)

        """
        already = cls.objects.all()
        submissions=[]
        cpLen = len(cp_set)
        for cp in cp_set:
            submissions.extend(list(Submission.submissionList(cp=cp, sta='Accepted')))
        is_user_in = {}
        records = []
        for ss in submissions:
            user = ss.user
            ok = is_user_in.get(user, 0)
            if ok==0:
                is_user_in[user]=1
                records.append(ss)

        length = len(records)

        for record1 in submissions: 
            for record2 in submissions:
                if record1.sid<record2.sid and record1.problem_index==record2.problem_index and record1.code_language==record2.code_language and record1.user!=record2.user: 
                    ct = Cheat()
                    ct.contest_problem = record1.problem_index
                    ct.sub1 = record1
                    ct.sub2 = record2
                    ct.status = -1
                    ct.ratio = 0
                    already_one = already.filter(contest_problem=ct.contest_problem)
                    already_one = already_one.filter(sub1=ct.sub1)
                    already_one = already_one.filter(sub2=ct.sub2)
                    if already_one.count()==0 :
                        ct.save()
        """

    @classmethod
    def getCheatList(cls, contest, threshold):
        return cls.objects.select_related('contest_problem', 'sub1__user', 'sub2__user').filter(contest_problem__contest = contest).filter(ratio__gte=threshold).order_by('-ratio')
        
    def update(self,status,score):
        self.status=status
        self.ratio=score
        self.save()

    @classmethod
    def init(cls):
        lent = len(lang)
        for i in xrange(0,lent):
            lanType=lang[i]
            keyLen = len(keywords[lanType])
            for j in xrange(0,keyLen):
                mapKeywords[lanType][keywords[lanType][j]] = chr(j+ord('a'))
            for j in xrange(0,26):
                tmp = chr(ord('a')+j)
                tmp2 = chr(ord('A')+j)
                mapSymbol[lanType][tmp] = j
                mapSymbol[lanType][tmp2] = j+26
                if j<10:
                    tmp3 = chr(ord('0')+j)
                    mapSymbol[lanType][tmp3] = j+52
            symLen = len(symbol[lanType])
            for j in xrange(0,symLen):
                tmp = symbol[lanType][j]
                mapSymbol[lanType][tmp] = 62+j

    @classmethod
    def queryNextPair(cls,query_info):
        sql_ret = 0
        pairs = cls.objects.filter(status=cls.QUERY_QUEENING)[:1]
        if pairs.count()==0:
            return cls.DB_QUERY_FAILED
      #  print pairs[0]
       # pairs[7].update(cls.QUERY_JUDGING,query_info.similar_score)
       # print pairs[7].ctid
        query_info.uid=pairs[0].ctid
        pair = cls.objects.get(ctid=query_info.uid)
        pair.update(cls.QUERY_JUDGING,query_info.similar_score)
       # print query_info.uid
       # print pairs[0].code_file1+" "+pairs[0].code_file2
        query_info.subs.append(pair.sub1)
        query_info.subs.append(pair.sub2)
     #   print query_info.codes[0]+" "+query_info.codes[1]
        return cls.DB_QUERY_SUCCEED

    @classmethod
    def updateSimilarScore(cls,query_info):
        sql_ret=0
        pair=cls.objects.get(ctid=query_info.uid)
       # print pair.ctid
        pair.update(cls.DB_UPDATE_SUCCEED,query_info.similar_score)
        return cls.DB_UPDATE_SUCCEED

    @classmethod
    def solve2(cls,Str,len1,len2):
        tlen = len(Str[0])
        plen = len(Str[1])
    #    print Str[0]
     #   print Str[1]
       # print min(plen,tlen)
        ans = 0
        MML = 4
        MaxLen=MML+1
       # print Str[0]
       # print Str[1]
        while MaxLen>MML:
            MaxLen = MML
            j = 1
            now_i=0
            #dp=[cls.MAX_CODE_LENGTH*[0],cls.MAX_CODE_LENGTH*[0]]
            
            k,s,t = lcs(Str[0],Str[1])

            if k<MaxLen:
                continue
            if s+k<tlen and Str[0][s+k]!='$':
                Str[0] = Str[0][0:s]+"$"+Str[0][s+k:tlen]
            else:
                Str[0] = Str[0][0:s]+Str[0][s+k:tlen]
            tlen=len(Str[0])
            if t+k<plen and Str[1][t+k]!='$':
                Str[1] = Str[1][0:t]+"$"+Str[1][t+k:plen]
            else:
                Str[1] = Str[1][0:t]+Str[1][t+k:plen]
            plen=len(Str[1])
            ans+=k
            MaxLen = k
        return ans

    @classmethod
    def probably2(cls,s,len1,len2):
        return 2.0*float(s)/(float(len1+len2))

    @classmethod
    def probably1(cls,s,len1,len2):
        return float(s)/(float(len1+len2)*0.5)

    @classmethod
    def solve1(cls,Str,len1,len2):
        j = 1
        now_i=0
        dp=[cls.MAX_CODE_LENGTH*[0],cls.MAX_CODE_LENGTH*[0]]
        for i in xrange(1,len1+1):
            for j in xrange(1,len2+1):
                dp[now_i][j]=dp[1-now_i][j]
                if dp[now_i][j-1]>dp[now_i][j]:
                    dp[now_i][j]=dp[now_i][j-1]
                if Str[0][i-1]==Str[1][j-1]:
                    if dp[1-now_i][j-1]+1>dp[now_i][j]:
                        dp[now_i][j] = dp[1-now_i][j-1]+1
            now_i = 1-now_i

        return dp[1-now_i][j]

    @classmethod
    def test1(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in xrange(0,2):
            code=open(query_info.subs[j].code_file)
            
           # print query_info.codes[j]
            try:
                all_code=code.read().decode('utf-8', 'ignore')
            finally:
                code.close()
            all_code = re.sub(rule[query_info.subs[j].code_language],"",all_code)
        #    print all_code
            lent=len(all_code)
            temp=''
            for i in xrange(0,lent):
                temp+=all_code[i]
            temp=re.findall('\w+|{|}',temp)
            tempLen=len(temp)
         #   print mapKeywords[query_info.subs[j].code_language]
            for i in xrange(tempLen):
                if temp[i] in mapKeywords[query_info.subs[j].code_language]:
                    Str[j]+=str(mapKeywords[query_info.subs[j].code_language][temp[i]])#append(mapKeyword[temp[i]])
                    length[j]+=1
                if temp[i]=='{' or temp[i]=='}':
                    Str[j]+=str(temp[i])#.append(temp[i])
                    length[j]+=1

      #  print "str1="
    #    print Str[0]
     #   print Str[1]
      #  print length[0],length[1]
        similar=cls.solve1(Str,length[0],length[1])
    #    print similar
        return cls.probably1(similar, length[0], length[1])*100

    @classmethod
    def test2(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in xrange(0,2):
            code=open(query_info.subs[j].code_file)
            try:
                all_code=code.read().decode('utf-8', 'ignore')
            finally:
                code.close()
            all_code = re.sub(rule[query_info.subs[j].code_language],"",all_code)
            lent=len(all_code)
            for i in xrange(0,lent):
                if all_code[i]!=' ' and all_code[i]!='\r' and all_code[i]!='\n' and all_code[i]!='\t':
                    Str[j]+=str(all_code[i])#.append(query_info.codes[j][i])
                    length[j]+=1

       # print "str2="
       # print Str
    #    print Str[0]
     #   print Str[1]
     #   print length[0],length[1]
        similar=cls.solve2(Str,length[0],length[1])
     #   print similar
        return cls.probably2(similar,length[0],length[1])*100

    
    @classmethod
    def solve3(cls,lanType,Str,len1,len2):
        num=[[0]*100,[0]*100]
     #   print mapSymbol[lanType]
        for j in xrange(0,2):
            lent=len(Str[j])
            for i in xrange(0,lent):
                tmp=Str[j][i]
                if not mapSymbol[lanType].has_key(tmp):
                    continue
                num[j][mapSymbol[lanType][tmp]]+=1
      #  print num[0]
       # print num[1]
        up=0
        down1=0
        down2=0
        symnum = len(symbol[lanType])
        for i in xrange(62+symnum):
            up+=float(num[0][i]*num[1][i])
            down1+=float(num[0][i]*num[0][i])
            down2+=float(num[1][i]*num[1][i])
        down1 = math.sqrt(down1)
        down2 = math.sqrt(down2)
        similar=up/down1/down2
        return similar

    @classmethod
    def test3(cls,query_info):
        length=[0,0]
        similar=0
        Str=['','']
        for j in xrange(0,2):
            code=open(query_info.subs[j].code_file)
            try:
                all_code=code.read().decode('utf-8', 'ignore')
            finally:
                code.close()
            all_code = re.sub(rule[query_info.subs[j].code_language],"",all_code)
            lent=len(all_code)
            for i in xrange(0,lent):
                Str[j]+=str(all_code[i])
                length[j]+=1
        similar=cls.solve3(query_info.subs[0].code_language,Str,length[0],length[1])
        return similar*100

    @classmethod
    def similarJudge(cls,query_info):
        query_info.similar_score=0.0
        query_info.similar_score+=cls.test1(query_info)*0.5
     #   print "score1="
      #  print query_info.similar_score
        query_info.similar_score+=cls.test2(query_info)*0.5
       # print "score2="
       # print query_info.similar_score
        query_score_acos=cls.test3(query_info)
       # print "acos="
       # print query_score_acos
        if query_score_acos==100:
            query_info.similar_score=query_score_acos

    @classmethod
    def antiCheat(cls):
        cls.init()
        while(True):
            query_info = QUERY()
           # print query_info.codes
            query_ret=cls.queryNextPair(query_info)
        #    break
            if query_ret!=cls.DB_QUERY_SUCCEED:
                break
            cls.similarJudge(query_info)
          #  print query_info.similar_score
            query_ret=cls.updateSimilarScore(query_info)
            if query_ret!=cls.DB_UPDATE_SUCCEED:
                break
            print query_info.uid
       #     if query_info.uid>=70:
        #        break
