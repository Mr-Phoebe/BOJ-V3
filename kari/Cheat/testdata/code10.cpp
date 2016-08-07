#include  </usr/include/mysql/mysql.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/times.h>
#include <sys/ptrace.h>
#include <sys/resource.h>
#include <iostream>
#include <stdlib.h>
#include <errno.h>
#include <sys/stat.h>
#include <time.h>
#include <math.h>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <ctype.h>
#define GET(a, i){a[i/32]&(1UL<<(i%32)}
#define SET(a, i){a[i/32]|=(1UL<<(i%32)}
#define see(x) //(cerr<<"Line:["<<__LINE__<<"]:"<<#x<<" = "<<x<<endl)
#define DB_QUERY_FAILED -1
#define DB_UPDATE_FAILED -1
#define DB_UPDATE_SUCCEED 1
#define DB_QUERY_SUCCEED 1
#define MAX_CODE_LENGTH 1055360
#define QUERY_QUEENING 0
#define QUERY_JUDGING -1

using namespace std;
typedef struct Query_Information{
	int uid;
	int contest_id;
	int solution_id[2];//be sure solution_id[0]<solution_id[1]
	char*code[2];
	double similar_score;
}QUERY;

int usleep_sec[10]={1000,2000,4000,8000,16000,32000,64000,128000,256000,512000};
int query_next_pair(MYSQL*resource,QUERY & query_info,int thread_id){
	int sql_ret=0;
	char sql_cmd[256]={0};
	MYSQL_RES* sql_res=NULL;
	MYSQL_ROW sql_row;
	int sleep_level=0;
	//db status
	int uid=0,solution_id_0=1,solution_id_1=2,contest_id=5;
	while(true){
		if(sql_res!=NULL){
			mysql_free_result(sql_res);
			sql_res=NULL;
		}
		snprintf(sql_cmd,sizeof(sql_cmd),"SELECT * FROM Similar WHERE status=%d LIMIT 1",QUERY_QUEENING);
		sql_ret=mysql_query(resource,sql_cmd);
		if(sql_ret!=0){
			//log
			return DB_QUERY_FAILED;
		}
		sql_res=mysql_store_result(resource);
		if(sql_res==NULL){
			//log
			return DB_QUERY_FAILED;
		}
		sql_row=mysql_fetch_row(sql_res);
		if(sql_row!=NULL){
			//log
			break;
		}
		usleep(usleep_sec[sleep_level++]);
		if(sleep_level>=9)sleep_level=9;
	}
	if(sql_res!=NULL){
		mysql_free_result(sql_res);
		sql_res=NULL;
	}
	snprintf(sql_cmd,sizeof(sql_cmd),"UPDATE Similar SET status=%d WHERE uid=%s",QUERY_JUDGING,sql_row[uid]);
	sql_ret=mysql_query(resource,sql_cmd);
	if(sql_ret!=0){
		see(sql_cmd);
		return DB_QUERY_FAILED;
	}
	sscanf(sql_row[uid],"%d",&query_info.uid);
	sscanf(sql_row[contest_id],"%d",&query_info.contest_id);
	sscanf(sql_row[solution_id_0],"%d",&query_info.solution_id[0]);
	sscanf(sql_row[solution_id_1],"%d",&query_info.solution_id[1]);
	return DB_QUERY_SUCCEED;	
}
MYSQL*do_connect_mysql()  //Connect to database
{
	MYSQL*mysql=(MYSQL*)calloc(sizeof(MYSQL),1);
    mysql_init(mysql);   //init mysql
    if (!mysql_real_connect(mysql,"localhost","root","TheMoon123","onlinejudge",0,NULL,0))
    {   //if
        free(mysql);
		fprintf(stderr, "Failed to connect to database: Error: %s\n",mysql_error(mysql));
        return NULL;
    }   //if
	if(mysql!=NULL){
		int sql_ret=mysql_query(mysql,"SET NAMES utf8");
		if(sql_ret!=0){
			//log
		}
	}
    return mysql;
}
#define MAX_USERS 2
int update_similar_score(MYSQL*resource,QUERY&query_info,int thread_id){
	int sql_ret=0;
	char sql_cmd[256]={0};
	snprintf(sql_cmd,sizeof(sql_cmd),"UPDATE Similar SET status=%d,similar_score=%lf WHERE uid=%d",thread_id,query_info.similar_score,query_info.uid);	
	sql_ret=mysql_query(resource,sql_cmd);
	if(sql_ret!=0){
		see(sql_cmd);
		return DB_UPDATE_FAILED;
	}
	return DB_UPDATE_SUCCEED;
}
int query_next_code(MYSQL*resource,QUERY&query_info){
	int sql_ret=0;
	MYSQL_RES*sql_res=NULL;
	MYSQL_ROW sql_row;
	char sql_cmd[256]={0};
	for(int i=0;i<MAX_USERS;i++){
		snprintf(sql_cmd,sizeof(sql_cmd),"SELECT code FROM solution_%d WHERE solution_id=%d",query_info.contest_id, query_info.solution_id[i]);
		sql_ret=mysql_query(resource,sql_cmd);
		if(sql_ret!=0){
			//log
			return DB_QUERY_FAILED;
		}
		sql_res=mysql_store_result(resource);
		if(sql_res==NULL){
			//log
			return DB_QUERY_FAILED;
		}
		sql_row=mysql_fetch_row(sql_res);
		if(sql_row==NULL){
			//log
			if(sql_res!=NULL){
				mysql_free_result(sql_res);
				sql_res=NULL;
			}
			return DB_QUERY_FAILED;
		}
		if(query_info.code[i]==NULL){
			query_info.code[i]=(char*)calloc(MAX_CODE_LENGTH+1,1);
		}
		snprintf(query_info.code[i],MAX_CODE_LENGTH,"%s",sql_row[0]);
		see("god...");
		if(sql_res!=NULL){
			mysql_free_result(sql_res);
			sql_res=NULL;
		}
	}
	//log
	return DB_QUERY_SUCCEED;
}
int Array[4][MAX_CODE_LENGTH+10];
int cnt[512],*SA,*nSA,*Rank,*Height,*nRank;
const int Offset=256;
char text[MAX_CODE_LENGTH+10];
int ang[2][MAX_CODE_LENGTH];
double arccosin(int len){
       double ans = 0.0,m1 = 0.0,m2 = 0.0; 
       int i;
       for(i = 1;i<len;++i){
             m1 += (double)(ang[0][i]*ang[0][i]);
             m2 += (double)(ang[1][i]*ang[1][i]);
             ans += (double)ang[0][i]*ang[1][i];
       }
       m1 = sqrt(m1);
       m2 = sqrt(m2);
       ans = ans/m1/m2;
       return acos(ans);
}
#define MAXC_LENGTH 2048
char str[2][MAX_CODE_LENGTH];
unsigned int bits1[MAXC_LENGTH/32] = {0};
unsigned int bits2[MAXC_LENGTH/32] = {0};
double solve1(int len1,int len2){
       int pre = 0;
       int m,t = 0;
       int MW = max(0,max(len1,len2)/2-1);
       double p = 0.1;
       while(pre<len1&&pre<len2&&(str[0][pre]==str[1][pre]))pre++;
       m = pre;
       for(int i = pre;i<len1;++i){
             for(int j = max(p,i-MW);j<len2&&j<=i+MW;++j){
                     if(!GET(str[1],j)&&(str[0][i]==str[1][j])){
                            SET(str[0],i);
                            SET(str[1],j);
                            m++;
                            break;
                     }
             }  
       }
       for(int i = pre,j = pre;i<len1&&j<len2;++i){
               if(!GET(str[0],i))continue;
               while(j<len2&&!GET(str[1],j))j++;
               if(j<len2&&str[0][i]!=str[1][j])t++;
               j++;
       }
       double ans = 0.0;
       if(m>0){
               ans = ((double)m/len1+(double)m/len2+(double)(m-t/2)/m)/3;
               ans+=(double)pre*p*(1.0-ans);
       }
       return ans;
}
double probably2(double s,double len1,double len2){
	return (s)/((len1+len2)/2-1);
}
double probably1(double s){
	return s;
}
int dp[2][MAX_CODE_LENGTH];
int  solve2(int len1,int len2){
     int i , j =1,cost,now_i=0,above ,left ,diag;
     memset(dp,0,sizeof(dp));
     int ans = 0;
     for(i=1,now_i=0;i<len1;i++,now_i=1-now_i){  
       for(j=1;j<len2;j++){
               if(str[0][i]==str[1][j]) 
                   dp[now_i][j] = dp[1-now_i][j-1]+1;
               else
                   dp[now_i][j] = 0;
               ans = max(ans,dp[now_i][j]);                  
       }
     }
     return  ans;
}
#define judge(x) (x=='('||x==')'||x=='{'||x=='}')
double test_2(QUERY&query_info){
    int len[2]={0},similar=0;
	for(int j = 0 ; j  < 2 ; j ++){
        for(int i = 0 ,lent=strlen(query_info.code[j]); i  < lent ; i ++){  
			if(isgraph(query_info.code[j][i])||query_info.code[j][i]<0)
				str[j][len[j]++]=query_info.code[j][i];
        }
        str[j][len[j]]=0;
    }
    similar=solve2(len[0],len[1]); 
    return probably2(similar,len[0],len[1])*100;
}
double test_1(QUERY&query_info){
	int len[2]={0},similar=0; 
	for(int j = 0 ; j <2; j++){
		//puts(query_info.code[j]);
		for(int i = 0,lent=strlen(query_info.code[j]) ; i  < lent ; i ++){
            if(judge(query_info.code[j][i]))  
                str[j][len[j]++]=query_info.code[j][i];
        }
		see(len[j]);
        str[j][len[j]]=0;
	}
    similar=solve1(len[0],len[1]);
	see(similar);
	see(len[0]);
	see(len[1]);
    return  probably1(similar)*100;
}
void similar_judge(QUERY&query_info){
	query_info.similar_score=0;
	query_info.similar_score+=test_1(query_info)*0.5;
	see(query_info.similar_score);
	query_info.similar_score+=test_2(query_info)*0.5;
	see(query_info.similar_score);
}
int main(int argv,char **argc){
	int thread_id=atoi(argc[1]);
	QUERY query_info;
	memset(&query_info,0,sizeof(query_info));
	MYSQL*mysql=do_connect_mysql();	
	if(mysql==NULL){
		//log
		exit(0);
	}
	while(true){
		int query_ret=query_next_pair(mysql,query_info,thread_id);
		if(query_ret!=DB_QUERY_SUCCEED){
			//log
			see("query failed");
			break;
		}
		query_ret=query_next_code(mysql,query_info);
		see("here?");
		if(query_ret!=DB_QUERY_SUCCEED){
			//log
			see("get code error");
			break;
		}
		see("this");
		similar_judge(query_info);
		see("flag");
		query_ret=update_similar_score(mysql,query_info,thread_id);
		if(query_ret!=DB_UPDATE_SUCCEED){
			see("update failed");
			//log
			break;
		}
	}
}
