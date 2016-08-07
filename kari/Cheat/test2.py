#!/usr/bin/dev python
import copy
#Str=["(){()$()(){$()()$()()${()}()${(){(($))(($())){$}}()()($){}()${}()$}()$}}","(){()(){()(){()(())()}}}"]
Str=["xyzbbbccc","abcdeyzbbbxxx"]
#Str=["abcde","abxd"]
#Str=["#include<stdio.h>intmain(){inte[16385];intT,n,i,a,b,c,d,t,j,l,k=0;scanf(\"%d\",&T);for(i=0;i<16384;i++)e[i]=0;while(T--){k=0;scanf(\"%d\",&n);if(n<=0||n>32768)printf(\"00\n\");elseif(n%4==0){a=n/4;b=n/2;printf(\"%d%d\n\",a,b);}elseif(n%4!=0&&n%2==0){c=n/2;for(i=c;i>=0;i--){d=(n-(*i))/4;if((n-(*i))%4==0&&d>=0){e[i]=d+i;}elsee[i]=0;}for(j=0;j<=c;j++)for(i=1;i<=c-j;i++)if(e[i]<e[i-1]){t=e[i];e[i]=e[i-1];e[i-1]=t;}for(i=c;e[i]!=0;i--){k++;}printf(\"%d%d\n\",e[k],e[c]);}elseprintf(\"00\n\");}return;}","#include<stdio.h>intmain(){inti,j,k,T,n;scanf(\"%d\",&T);while(T--){scanf(\"%d\",&n);if(n%2!=0)printf(\"00\n\");else{i=n/4;j=n/2;k=(n%4)/2;printf(\"%d%d\n\",i+k,j);}}return0;}"]
len1=len(Str[0])
len2=len(Str[1])
ans=0
l1=0
l2=0
global text
text=''
for i in range(1,len1):
    text+=str(Str[0][i])#.append(Str[0][i])
    l1+=1
text+=str(chr(0))
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
L = l2

#print L

global Array
Array=[[0]*(200000)]*4
global SA
SA=[0]*200000
global nSA
nSA=[0]*200000
global Rank
Rank=[0]*200000
global nRank
global Height
cnt=[0]*200000
for i in range(0,L):
         #   print L
          #  print i
           # print text[i]
    cnt[ord(text[i])]+=1

#print cnt[0]
#for i in range(0,L):
 #   print cnt[i]

for i in range(1,256):
    cnt[i]+=cnt[i-1]

#for i in range(0,L):
 #   print cnt[i]

for i in range(0,L):
    cnt[ord(text[i])]-=1
    SA[cnt[ord(text[i])]]=i
#    print cnt[ord(text[i])]

#for i in range(0,L):
 #   print SA[i]
#for i in range(0,L):
 #   print cnt[i]
for i in range(1,L):
  #  print "%d %d" %(i,SA[5])
    Rank[SA[i]] = Rank[SA[i-1]]
    if text[SA[i]]!=text[SA[i-1]]:
        Rank[SA[i]]+=1
    #print "%d %d" %(i,SA[5])
 #       print "%d %d %d" %(i,SA[i],Rank[SA[i]])

#for i in range(0,L):
 #   print Rank[i]

k = 1
while k<L and Rank[SA[L-1]]<L-1:
         #   print k
            
    for i in range(0,L):
        cnt[Rank[SA[i]]]=i+1
    
   # if k==2:
    #    tmp=[]
     #   for i in range(0,L):
      #      tmp.append(SA[i])
       # print tmp
    
    for i in range(L-1,-1,-1):
        #print i
        if SA[i]>=k:
           # print "xxx"
            cnt[Rank[SA[i]-k]]-=1
            nSA[cnt[Rank[SA[i]-k]]]=SA[i]-k
          #  print "%d %d" %(cnt[Rank[SA[i]-k]],SA[i]-k)

   # if k==1:
    #    tmp=[]
     #   for i in range(0,L):
      #      tmp.append(SA[i])
       # print tmp

    for i in range(L-k,L):
        cnt[Rank[i]]-=1
        nSA[cnt[Rank[i]]]=i

 #   if k==1:
  #      tmp=[]
   #     for i in range(0,L):
    #        tmp.append(SA[i])
     #   print tmp

    nRank=SA
  #  if k==1:
   #     tmp=[]
    #    for i in range(0,L):
     #       tmp.append(SA[i])
      #  print tmp
    SA=nSA
  #  if k==1:
   #     tmp = []
    #    for i in range(0,L):
     #       tmp.append(SA[i])
      #  print tmp
    nRank[SA[0]]=0
    for i in range(1,L):
        nRank[SA[i]]=nRank[SA[i-1]]
        if Rank[SA[i]]!=Rank[SA[i-1]] or Rank[SA[i]+k]!=Rank[SA[i-1]+k]:
            nRank[SA[i]]+=1
    
    #if k==1:
     #   tmp = []
      #  for i in range(0,L):
       #     tmp.append(SA[i])
        #print tmp

    nSA=Rank
    #print nSA
    Rank=nRank
   # print Rank
    k*=2

Height=[0]*200000
k = 0
#tmp=[]
#print text
#for i in range(0,L):
    #print SA[i]
 #   tmp.append(SA[i])
#print tmp

for i in range(0,L):
    if Rank[i]==0:
        Height[Rank[i]]=0
    else:
        if SA[Rank[i]-1]==i:
            Height[Rank[i]]=k
            continue
        j=SA[Rank[i]-1]
        while i+k<L and j+k<L and text[i+k]!='$' and text[j+k]!='$' and text[i+k]==text[j+k]:
            k+=1
        Height[Rank[i]]=k
        if k>0:
            k-=1
lenall=l2
s = 0
t = 0
     #   print lenall
for i in range(1,lenall):
      #      print i
       #     print i-1
    if (SA[i]<l1 and SA[i-1]>=l1) or (SA[i]>=l1 and SA[i-1]<l1):
        if Height[i]>ans:
            ans=Height[i]
            s = min(SA[i],SA[i-1])
            t = max(SA[i],SA[i-1])

print "%d %d %d" %(ans,s,t-l1)
