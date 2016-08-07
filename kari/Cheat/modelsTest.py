import math
import re
from lcs import lcs
from conf import rule
# Create your models here.


keywords=["int","long","short","switch","char","struct","for","while","if","else","break","continue","return","float","double","do","signed","unsigned"]
symbol=["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"]
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

MAX_LEN = 128
DB_QUERY_FAILED = -1
DB_UPDATE_FAILED=-1
DB_UPDATE_SUCCEED=1
DB_QUERY_SUCCEED=1
MAX_CODE_LENGTH=1055360
QUERY_QUEENING=-1
QUERY_JUDGING=0
MAX_USERS=2
KEYNUM=18
SYMNUM=28

#keywords=["int","long","for","while","if","else","break","continue","return","true","false","double","do","signed","unsigned"]
#symbol=["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"]
#mapKeyword={}
#mapSymbol={}
#treeMem=[] 

def init():
    for i in range(0,KEYNUM):
        mapKeyword[keywords[i]]=chr(i+ord('a'))

    for i in range(0,26):
        tmp=chr(ord('a')+i)
        tmp2=chr(ord('A')+i)
        mapSymbol[tmp]=i
        mapSymbol[tmp2]=i+26
        if i<10:
            tmp3=chr(ord('0')+i)
            mapSymbol[tmp3]=i+52
    for i in range(0,SYMNUM):
        tmp=symbol[i]
        mapSymbol[tmp]=62+i

def solve2(Str,len1,len2):
    #t_m=[0]*cls.MAX_CODE_LENGTH
   # p_m=t_m
    Set=[]
    tlen = len(Str[0])
    plen = len(Str[1])
  #  print Str[0]
  #  print Str[1]
   # print min(plen,tlen)
    ans = 0
  #  MML = min(tlen,plen)
   # if MML>200:
    #    MML = 10
    #else:
     #   MML = max(MML/25,4)
    MML = 4
    MaxLen=MML+1
   # print Str[0]
   # print Str[1]
    while MaxLen>MML:
        MaxLen = MML
        j = 1
        now_i=0
      #  dp=[cls.MAX_CODE_LENGTH*[0],cls.MAX_CODE_LENGTH*[0]]
        k,s,t = lcs(Str[0],Str[1])

    #    print k
     #   print Str[0][s:s+k]+"   XXX  "+Str[1][t:t+k]+"   OOO  "
            
        if k<MaxLen:
            continue
            #print Str[0][s:s+k]
            #print Str[1][t:t+k]
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
    #Set=[]
     #   print k
      #  print Str
    return ans

def probably2(s,len1,len2):
    return 2.0*float(s)/(float(len1+len2))

def probably1(s,len1,len2):
    return float(s)/(float(len1+len2)*0.5)

def solve1(Str,len1,len2):
    j = 1
    now_i=0
    dp=[65536*[0],65536*[0]]
    for i in range(1,len1+1):
        for j in range(1,len2+1):
            dp[now_i][j]=dp[1-now_i][j]
            if dp[now_i][j-1]>dp[now_i][j]:
                dp[now_i][j]=dp[now_i][j-1]
            if Str[0][i-1]==Str[1][j-1]:
                if dp[1-now_i][j-1]+1>dp[now_i][j]:
                    dp[now_i][j] = dp[1-now_i][j-1]+1
        now_i = 1-now_i

    return dp[1-now_i][j]

def test1(query_info):
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
        all_code=re.sub(rule["gcc"],"",all_code)
       # print all_code
        lent=len(all_code)
        temp=''
        for i in range(0,lent):
            temp+=all_code[i]
      #  print temp
        temp=re.findall('\w+|{|}',temp)
        tempLen=len(temp)
        for i in range(tempLen):
            if temp[i] in mapKeyword:
                Str[j]+=str(mapKeyword[temp[i]])#append(mapKeyword[temp[i]])
                length[j]+=1
            if temp[i]=='{' or temp[i]=='}':
                Str[j]+=str(temp[i])#.append(temp[i])
                length[j]+=1

 #   print "str1="
  #  print Str
    similar=solve1(Str,length[0],length[1])
 #   print similar
    return probably1(similar, length[0], length[1])*100

def test2(query_info):
    length=[0]*2
    similar=0
    Str=['','']
    for j in range(0,2):
        code=open(query_info.codes[j])
        try:
            all_code=code.read()
        finally:
            code.close()
        all_code=re.sub(rule["gcc"],"",all_code)
        lent=len(all_code)
        for i in range(0,lent):
            if all_code[i]!=' ' and all_code[i]!='\r' and all_code[i]!='\n' and all_code[i]!='\t':
                Str[j]+=str(all_code[i])#.append(query_info.codes[j][i])
                length[j]+=1

   # print "str2="
 #   print Str
  #  print length[0],length[1]
    similar=solve2(Str,length[0],length[1])
   # print similar
    return probably2(similar,length[0],length[1])*100


def solve3(Str,len1,len2):
    num=[[0]*100,[0]*100]
    for j in range(0,2):
        lent=len(Str[j])
        for i in range(0,lent):
            tmp=Str[j][i]
            if not mapSymbol.has_key(tmp):
                continue
            num[j][mapSymbol[tmp]]+=1
 #   print num[0]
  #  print num[1]
    up=0
    down1=0
    down2=0
    for i in range(62+SYMNUM):
        up+=float(num[0][i]*num[1][i])
        down1+=float(num[0][i]*num[0][i])
        down2+=float(num[1][i]*num[1][i])
    down1 = math.sqrt(down1)
    down2 = math.sqrt(down2)
    similar=up/down1/down2
    return similar

def test3(query_info):
    length=[0,0]
    similar=0
    Str=['','']
    for j in range(0,2):
        code=open(query_info.codes[j])
        try:
            all_code=code.read()
        finally:
            code.close()
        all_code = re.sub(rule["gcc"],"",all_code)
        lent=len(all_code)
        for i in range(0,lent):
           # if all_code[i]!=' ':
            Str[j]+=str(all_code[i])
            length[j]+=1
    similar=solve3(Str,length[0],length[1])
    return similar*100

def similarJudge(query_info):
    query_info.similar_score=0.0
    query_info.similar_score+=test1(query_info)*0.5
 #   print "score1="
    print query_info.similar_score
    query_info.similar_score+=test2(query_info)*0.5
   # print "score2="
    print query_info.similar_score
    query_score_acos=test3(query_info)
 #   print query_score_acos
   # print "acos="
   # print query_score_acos
    if query_score_acos==100:
        query_info.similar_score=query_score_acos

def antiCheat():
    init()
    query_info = QUERY()
  #  query_info.codes=["/home/buptacm/oj/media/submission//912test2.cpp","/home/buptacm/oj/media/submission//912test.cpp"]
#1003,875 309,258
    query_info.codes=["./testdata/code27.cpp","./testdata/code28.cpp"]
 #   query_info.codes=["1144","1158"]
    similarJudge(query_info)
    print query_info.similar_score
        #break

antiCheat()
