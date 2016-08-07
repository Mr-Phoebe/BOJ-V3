#include<iostream>
#include<cstdlib>
#include<cstdio>
#define INF 999999999
using namespace std;
int a[2000][2000];
int main ()
{
    int n,m;
    while (cin>>n>>m)
    {
          
          for (int i=0;i<n;i++)
              for (int j=0;j<n;j++)
                  a[i][j]=INF;
          for (int i=0;i<m;i++)
          {
              int temp1,temp2,temp3;
              cin>>temp1>>temp2>>temp3;
              temp1--;temp2--;
              if (a[temp1][temp2]>temp3)
              {
                   a[temp1][temp2]=temp3;
                   a[temp2][temp1]=temp3;
              }
          }
    
          int flag[2000];
          int low[2000];
          memset(flag,0,sizeof (flag));
          flag[0]=1;
          int s=0;
          for (int i=1;i<n;i++)
              low[i]=a[0][i];
          int pos=0;
          for (int i=1;i<n;i++)
          {
              int min=INF;
              int dis1,dis2;
              for (int j=0;j<n;j++)
                  if (flag[j]!=1&&low[j]<min)
                  {
                     min=low[j];
                     dis2=j;
                  }
              //check[pos][dis2]=1;
              pos=dis2;
              flag[dis2]=1;
              if(min>s)
                s=min;
              for (int j=0;j<n;j++)
                  if (flag[j]!=1&&a[dis2][j]<low[j])
                     low[j]=a[dis2][j];
          }
          cout<<s<<endl;
    
    }
}