#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int com(char *a)
{
    int i=1;
    if(a[0]!='d') i=0;
    if(a[1]!='a') i=0;
    if(a[2]!='i') i=0;
    if(a[3]!='z') i=0;
    if(a[4]!='h') i=0;
    if(a[5]!='e') i=0;
    if(a[6]!='n') i=0;
    if(a[7]!='y') i=0;
    if(a[8]!='a') i=0;
    if(a[9]!='n') i=0;
    if(a[10]!='g') i=0;
    if(a[11]!='\0') i=0;
    if(i==1) return 1;
    else     return 0;
    }
int main()
{
    char name[100],d[100]="daizhenyang";
    int t,n,f,i,dscor,scor,max;
    scanf("%d",&t);
    while(t-->0)
    {
                f=0;
                scanf("%d",&n);
                for(i=1;i<=n;i++)
                   {
                                 max=0;
                                 scanf("%s",name);
                                 scanf("%d",&scor);
                                 if(com(name)==1) {f=1;dscor=scor;}
                                 if(max<scor) max=scor;
                                 }
                if(f==0) printf("What a pity!\n");
                else if(dscor>=max) printf("Daizhenyang is the champion of the world!\n");
                else printf("I can not believe that!\n");
                }

    return 0;
}