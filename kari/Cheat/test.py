
#Str=["abcdefghijk","xbcdssghijpt"]
Str=["#include<stdio.h>intmain(){inte[16385];intT,n,i,a,b,c,d,t,j,l,k=0;scanf(\"%d\",&T);for(i=0;i<16384;i++)e[i]=0;while(T--){k=0;scanf(\"%d\",&n);if(n<=0||n>32768)printf(\"00\n\");elseif(n%4==0){a=n/4;b=n/2;printf(\"%d%d\n\",a,b);}elseif(n%4!=0&&n%2==0){c=n/2;for(i=c;i>=0;i--){d=(n-(*i))/4;if((n-(*i))%4==0&&d>=0){e[i]=d+i;}elsee[i]=0;}for(j=0;j<=c;j++)for(i=1;i<=c-j;i++)if(e[i]<e[i-1]){t=e[i];e[i]=e[i-1];e[i-1]=t;}for(i=c;e[i]!=0;i--){k++;}printf(\"%d%d\n\",e[k],e[c]);}elseprintf(\"00\n\");}return;}","#include<stdio.h>intmain(){inti,j,k,T,n;scanf(\"%d\",&T);while(T--){scanf(\"%d\",&n);if(n%2!=0)printf(\"00\n\");else{i=n/4;j=n/2;k=(n%4)/2;printf(\"%d%d\n\",i+k,j);}}return0;}"]
#Str=["#include<stdio.h>intmain(){inte[16385];intT,n,i,a,b,c,d,t,j,l,k=0;scanf(\"%d\",&T);for(i=0;i<16384;i++)e[i]=0;","#include<stdio.h>intmain(){inti,j,k,T,n;scanf(\"%d\",&T);while(T--){scanf(\"%d\",&n);}"]
Set=[]
Set=[]
tlen = len(Str[0])
plen = len(Str[1])
ans = 0
MML = 2
MaxLen=MML+1
while MaxLen>MML:
    MaxLen = MML
    j = 1
    now_i=0
    dp=[200000*[0],200000*[0]]
    k = 0
    a = 0
    b = 0
        #    print Str
    for i in range(1,tlen):
        for j in range(1,plen):
            if Str[0][i]!='$' and Str[1][j]!='$' and Str[0][i]==Str[1][j]:
                dp[now_i][j] = dp[1-now_i][j-1]+1
                        #k = max(k,dp[now_i][j])
                if dp[now_i][j]>k:
                    k = dp[now_i][j]
                    a = i-dp[now_i][j]+1
                    b = j-dp[now_i][j]+1
                    #print "%d %d %d" %(k,i,j)
            else:
                dp[now_i][j] = 0
                          #  print Str[0][a:a+k]
                           # print Str[1][b:b+k]
        now_i = 1-now_i

    if k>=MaxLen:
        Set=[]
        SetItem=[]
        SetItem.append(k)
        SetItem.append(a)
        SetItem.append(b)
        Set.append(SetItem)
        MaxLen=k
       # print Str[0][a:a+k]+"   $$$    "+ Str[1][b:b+k]+"   OOO   "


    size=len(Set)
    for i in range(0,size):
        s = Set[i][1]
        t = Set[i][2]
        k = Set[i][0]
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
    print "%d %d %d" %(k,s,t)
    break
    Set=[]

print tlen+plen

