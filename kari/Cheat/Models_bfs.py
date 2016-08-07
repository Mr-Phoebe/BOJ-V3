# -*- coding: utf-8 -*-

from django.db import models,transaction
from kari.const import Const
from django.core.exceptions import ValidationError
from Submission.models import Submission
from User.models import User
from Problem.models import Problem
import math
import re
# Create your models here.


keywords=["int","long","for","while","if","else","break","continue","return","true","false","double","do","signed","unsigned"]
symbol=["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\","\n","\r"]
mapKeyword={}
mapSymbol={}
treeMem=[] 

class QUERY:
    uid=0
    similar_score=0.0
    codes=[]
    def __init__(self):
        self.uid = 0
        self.similar_score = 0.0
        self.codes=[]

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
    KEYNUM=15
    SYMNUM=30

    #keywords=["int","long","for","while","if","else","break","continue","return","true","false","double","do","signed","unsigned"]
    #symbol=["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"]
    #mapKeyword={}
    #mapSymbol={}
    #treeMem=[] 

    ctid = models.AutoField(primary_key=True)
    contest_problem = models.CharField(max_length=100)
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=Const.USERNAME_MAX_LENGTH+10)
    code_file1 = models.FilePathField( path='code')
    code_file2 = models.FilePathField( path='code')
    status = models.IntegerField()
    ratio = models.FloatField()

    @classmethod
    def addRecord(cls, contestid):

        already = cls.objects.all()
        #return
        submissions = Submission.submissionList(c=contestid, sta='Accepted')
       # return
        is_user_in = {}
        record_list = []
        for ss in submissions:
            user = ss.user
            ok = is_user_in.get(user, 0)
            if ok==0:
                is_user_in[user]=1
                record = []
                record.append(ss.problem_index)
                record.append(ss.user)
                record.append(ss.code_file)
                record_list.append(record)

        length = len(record_list)

        for i in range(length): 
            for j in range(length):
                if i<j and record_list[i][0]==record_list[j][0] and record_list[i][1]!=record_list[j][1]: 
                    ct = Cheat()
                    ct.contest_problem = record_list[i][0]
                    ct.user1 = record_list[i][1]
                    ct.user2 = record_list[j][1]
                    ct.code_file1 = record_list[i][2]
                    ct.code_file2 = record_list[j][2]
                    ct.status = -1
                    ct.ratio = 0
                    already_one = already.filter(contest_problem=ct.contest_problem)
                    already_one = already_one.filter(user1=ct.user1)
                    already_one = already_one.filter(user2=ct.user2)
                    if already_one.count()==0 :
                        ct.save()

    @classmethod
    def getCheatList(cls):
        cheat_list = cls.objects.all()
        cheat_list = cheat_list.filter(ratio__gte=90)
        return cheat_list

    def update(self,status,score):
        self.status=status
        self.ratio=score
        self.save()

    @classmethod
    def init(cls):
        for i in range(0,cls.KEYNUM):
            mapKeyword[keywords[i]]=chr(i+ord('a'))

        for i in range(0,26):
            tmp=chr(ord('a')+i)
            tmp2=chr(ord('A')+i)
            mapSymbol[tmp]=i
            mapSymbol[tmp2]=i+26
            if i<10:
                tmp3=chr(ord('0')+i)
                mapSymbol[tmp3]=i+52
        for i in range(0,cls.SYMNUM):
            tmp=symbol[i]
            mapSymbol[tmp]=62+i

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
        query_info.codes.append(pairs[0].code_file1)
        query_info.codes.append(pairs[0].code_file2)
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
    def suffixArray(cls,L):
        global Array
        Array=[[0]*(cls.MAX_CODE_LENGTH*3+10)]*4
        global SA
        SA=Array[0]
        global nSA
        nSA=Array[1]
        global Rank
        Rank=Array[2]
        global nRank
        global Height
        cnt=[0]*cls.MAX_CODE_LENGTH
        for i in range(0,L):
         #   print L
          #  print i
           # print text[i]
            cnt[ord(text[i])]+=1
        for i in range(1,256):
            cnt[i]+=cnt[i-1]
        for i in range(0,L):
            SA[--cnt[ord(text[i])]]=i

        Rank[SA[0]]=0
        for i in range(1,L):
            Rank[SA[i]]=Rank[SA[i-1]]
            if text[SA[i]]!=text[SA[i-1]]:
                Rank[SA[i]]+=1

        k = 1
        while k<L and Rank[SA[L-1]]<L-1:
         #   print k
            
            for i in range(0,L):
                cnt[Rank[SA[i]]]=i+1
            for i in range(L-1,-1):
                if SA[i]>=k:
                    nSA[--cnt[Rank[SA[i]-k]]]=SA[i]-k
            for i in range(L-k,L):
                nSA[--cnt[Rank[i]]]=i
            nRank=SA
            SA=nSA
            nRank[SA[0]]=0
            for i in range(1,L):
                nRank[SA[i]]=nRank[SA[i-1]]
                if Rank[SA[i]]!=Rank[SA[i-1]] or Rank[SA[i]+k]!=Rank[SA[i-1]+k]:
                    nRank[SA[i]]+=1
            nSA=Rank
            Rank=nRank
            k*=2

        Height=Array[3]
        k = 0
        for i in range(0,L):
            if Rank[i]==0:
                Height[Rank[i]]=0
            else:
                if SA[Rank[i]-1]==i:
                    Height[Rank[i]]=k
                    continue
                j=SA[Rank[i]-1]
                while i+k<L and j+k<L and text[i+k]==text[j+k]:
                    k+=1
                Height[Rank[i]]=k
                if k>0:
                    k-=1

    @classmethod
    def solve4(cls,Str,len1,len2):
        ans=0
        l1=0
        l2=0
        global text
        text=''
        for i in range(1,len1):
            text+=str(Str[0][i])#.append(Str[0][i])
            l1+=1
        l2 = l1
        for i in range(1,len2):
            text+=str(Str[1][i])#.append(Str[1][i])
            l2+=1
        text+="$"#.append('$')
        l2+=1
      #  print l2
      #  print text[0]
     #   print "text="
      #  print text
        cls.suffixArray(l2)
        lenall=l2
     #   print lenall
        for i in range(1,lenall):
      #      print i
       #     print i-1
            if (SA[i]<l1 and SA[i-1]>=l1) or (SA[i]>=l1 and SA[i-1]<l1):
                if Height[i]>ans:
                    ans=Height[i]

        return ans

    @classmethod
    def solve2(cls,Str,len1,len2):
        t_m=[0]*cls.MAX_CODE_LENGTH
        p_m=t_m
        Set=[]
        tlen = len(Str[0])
        plen = len(Str[1])
        ans = 0
        MML = 4
        MaxLen=MML+1
        while MaxLen>MML:
            MaxLen = MML
            for i in range(0,tlen):
                for j in range(0,plen):
                    k = 0
                    while i+k<tlen and j+k<plen and Str[0][i+k]!='$' and Str[1][j+k]!='$' and Str[0][i+k]==Str[1][j+k]:
                        k+=1
                    if k==MaxLen:
                        if len(Set)==0:
                            SetItem=[]
                            SetItem.append(k)
                            SetItem.append(i)
                            SetItem.append(j)
                            Set.append(SetItem)
                    if k>MaxLen:
                        Set=[]
                        SetItem=[]
                        SetItem.append(k)
                        SetItem.append(i)
                        SetItem.append(j)
                        Set.append(SetItem)
                        MaxLen=k

            size=len(Set)
            for i in range(0,size):
                s = Set[i][1]
                t = Set[i][2]
                k = Set[i][0]
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
            Set=[]
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
        for i in range(1,len1):
            for j in range(1,len2):
                dp[now_i][j]=dp[1-now_i][j]
                if dp[now_i][j-1]>dp[now_i][j]:
                    dp[now_i][j]=dp[now_i][j-1]
                if Str[0][i]==Str[1][j]:
                    if dp[1-now_i][j-1]+1>dp[now_i][j]:
                        dp[now_i][j] = dp[1-now_i][j-1]+1
            now_i = 1-now_i

        return dp[1-now_i][j-1]

    @classmethod
    def test1(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in range(0,2):
            code=open(query_info.codes[j])
           # print query_info.codes[j]
            try:
                all_code=code.read()
            finally:
                code.close()
           # print all_code
            lent=len(all_code)
            temp=''
            for i in range(0,lent):
                if i<lent-1 and all_code[i]=='/' and all_code[i+1]=='/':
                    while i<lent and all_code[i]!='\n':
                        i+=1
                    continue
                if i<lent-1 and all_code[i]=='/' and all_code[i+1]=='*':
                    while i<lent-1 and not (all_code[i]=='*' and all_code[i+1]=='/'):
                        i+=1
                    continue
                temp+=all_code[i]
            temp=re.findall('\w+|{|}',temp)
            tempLen=len(temp)
            for i in range(tempLen):
                if temp[i] in mapKeyword:
                    Str[j]+=str(mapKeyword[temp[i]])#append(mapKeyword[temp[i]])
                    length[j]+=1
                if temp[i]=='{' or temp[i]=='}':
                    Str[j]+=str(temp[i])#.append(temp[i])
                    length[j]+=1

      #  print "str1="
      #  print Str
        similar=cls.solve1(Str,length[0],length[1])
        return cls.probably1(similar, length[0], length[1])*100

    @classmethod
    def test2(cls,query_info):
        length=[0]*2
        similar=0
        Str=['','']
        for j in range(0,2):
            code=open(query_info.codes[j])
            try:
                all_code=code.read()
            finally:
                code.close()
            lent=len(all_code)
            for i in range(0,lent):
                if i<lent-1 and all_code[i]=='/' and all_code[i+1]=='/':
                    while i<lent and all_code[i]!='\n':
                        i+=1
                    continue
                if i<lent-1 and all_code[i]!='/' and all_code[i+1]=='*':
                    while i<lent-1 and not (all_code[i]=='*' and all_code[i+1]=='/'):
                        i+=1
                    continue
                if all_code[i]!=' ':
                    Str[j]+=str(all_code[i])#.append(query_info.codes[j][i])
                    length[j]+=1

       # print "str2="
       # print Str
        similar=cls.solve2(Str,length[0],length[1])
       # print similar
        return cls.probably2(similar,length[0],length[1])*100

    @classmethod
    def solve3(cls,Str,len1,len2):
        num=[[0]*100,[0]*100]
        for j in range(0,2):
            lent=len(Str[j])
            for i in range(0,lent):
                tmp=Str[j][i]
                if not mapSymbol.has_key(tmp):
                    continue
                num[j][mapSymbol[tmp]]+=1
        up=0
        down1=0
        down2=0
        for i in range(62+cls.SYMNUM):
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
        for j in range(0,2):
            code=open(query_info.codes[j])
            try:
                all_code=code.read()
            finally:
                code.close()
            lent=len(all_code)
            for i in range(0,lent):
                if i<lent-1 and all_code[i]=='/' and all_code[i+1]=='/':
                    while i<lent and all_code[i]!='\n':
                        i+=1
                    continue
                if i<lent-1 and all_code[i]!='/' and all_code[i+1]=='*':
                    while i<lent-1 and not (all_code[i]=='*' and all_code[i+1]=='/'):
                        i+=1
                    continue
                if all_code[i]!=' ':
                    Str[j]+=str(all_code[i])
                    length[j]+=1
        similar=cls.solve3(Str,length[0],length[1])
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
            break
