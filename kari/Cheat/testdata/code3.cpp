#include<iostream> 
#include<cstdio> 
#include<cstring> 
#include<cmath> 

using namespace std; 

int n,k,i,j,x,y,mid; 
int matrix[8][8]; 
double const maxn = 999999999; 
double sum[8][8][8][8] = {0}; 
double dp[16][8][8][8][8] = {0}; 
double total = 0,temp = 0,average = 0; 

double min(double a, double b) 
{ 
return a<b? a:b; 
}; 

int main(){ 

scanf("%d",&n); 
for(i = 0; i < 8; i++) 
for(j = 0; j < 8; j++){ 
scanf("%d",&matrix[i][j]); 
total += matrix[i][j]; 
} 
average = total / (n*1.0); 

for(i = 0; i < 8; i++) 
for(j = 0; j < 8; j++) 
for(x = i; x < 8; x++){ 
total = 0; 
for(y = j; y < 8; y++){ 
total += matrix[x][y]; 
if(x == i) 
sum[i][j][x][y] = total; 
else 
sum[i][j][x][y] = total + sum[i][j][x-1][y]; 
} 
} 

for(i = 0; i < 8; i++) 
for(j = 0; j < 8; j++) 
for(x = i; x < 8; x++) 
for(y = j; y < 8; y++){ 
sum[i][j][x][y] *= sum[i][j][x][y]; 
dp[0][i][j][x][y] = sum[i][j][x][y]; 
} 

for(k = 1; k < n ; k++) 
for(i = 0; i < 8; i++) 
for(j = 0; j < 8; j++) 
for(x = i; x < 8; x++) 
for(y = j; y < 8; y++){ 
dp[k][i][j][x][y] = maxn; 

for(mid = i; mid < x; mid ++){ 
temp = min(dp[k-1][i][j][mid][y] + sum[mid+1][j][x][y] 
,dp[k-1][mid+1][j][x][y] + sum[i][j][mid][y]); 
dp[k][i][j][x][y] = min(temp,dp[k][i][j][x][y]); 
} 
for(mid = j; mid < y; mid ++){ 
temp = min(dp[k-1][i][j][x][mid] + sum[i][mid+1][x][y] 
,dp[k-1][i][mid+1][x][y] + sum[i][j][x][mid]); 
dp[k][i][j][x][y] = min(temp,dp[k][i][j][x][y]); 
} 
} 

double answer = dp[n-1][0][0][7][7]/(n*1.0) - average * average; 

printf("%.3lf\n",sqrt(answer)); 
return 0; 
}