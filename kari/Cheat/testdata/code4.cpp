#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

struct data
{
    double x;
    double y;
    double r;
}pos[1005];

int main()
{
    int t,i,j,n,k,p;
    scanf("%d",&t);
    double a[1010][1010];
    double tmp;
    int s[1010];
    double dist[1010];
    double MIN;
    int v;
    for(i=0;i<t;i++)
    {
        scanf("%d",&n);
        scanf("%lf %lf",&pos[0].x,&pos[0].y);
        pos[0].r=0;
        scanf("%lf %lf",&pos[n+1].x,&pos[n+1].y);
        pos[n+1].r=0;
        for(j=1;j<=n;j++)
        {
            scanf("%lf %lf %lf",&pos[j].x,&pos[j].y,&pos[j].r);
        }
        for(j=0;j<=n+1;j++)
        {
            for(k=0;k<=n+1;k++)
            {
                if(j==k)
                {
                    a[j][k]=1000000000;
                    continue;
                }
                tmp=pow(pow(pos[j].x-pos[k].x,2.0)+pow(pos[j].y-pos[k].y,2.0),0.5);
                if(tmp==0)
                    a[j][k]=a[k][j]=0;
                else if(tmp>pos[j].r+pos[k].r)
                    a[j][k]=a[k][j]=tmp-pos[j].r-pos[k].r;
                else if(tmp==pos[j].r+pos[k].r) 
                {
                    a[j][k]=a[k][j]=0;
                }
                else
                {
                    a[j][k]=a[k][j]=0;
                }
            }
        }
    /*    for(j=0;j<n+2;j++)
        {
            for(p=0;p<n+2;p++)
            {        
                printf("%lf ",a[j][p]);
            }
            printf("\n");
        }
    */    
        for(j=0;j<=n+1;j++)
        {
            dist[j]=a[0][j];
            s[j]=0;
        }
        s[0]=1;
        for(j=0;j<=n+1;j++)
        {
            MIN=1000000000;
            for(p=0;p<=n+1;p++)
            {
                if(s[p]==0 && dist[p]<MIN)
                {
                    v=p;
                    MIN=dist[p];
                }
            }
            s[v]=1;
            if(v==n+1)
                break;
            for(p=0;p<=n+1;p++)
            {
                if(s[p]==0)
                {
                    if(dist[p]>a[v][p]+dist[v])
                        dist[p]=a[v][p]+dist[v];
                }
            }
        }
        printf("%.3lf\n",dist[n+1]);
    }
    return 0;
}