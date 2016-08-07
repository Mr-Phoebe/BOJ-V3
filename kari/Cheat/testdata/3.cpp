#include<stdio.h>
#include<string.h>
main()
{
      int t,n,i,j,k,l,s[10000],m;
      char name[10000][100];
      scanf("%d",&t);
      for(i=1,m=0;i<=t;i++)
      {
         scanf("%d",&n);
         for(j=0;j<=n-1;j++)
         {
             scanf("%s %d",name[j],&s[j]);
             if(s[j]>m)
                m=s[j]; 
         }
         for(j=0,l=0;j<=n-1;j++)
         {
            if(strcmp(name[j],"daizhenyang")==0)
            {
               if(s[j]==m)
                  printf("Daizhenyang is the champion of the world!\n");
               else
                  printf("I can not believe that!\n");
               l=1;
               break;
            }
         }
         if(l==0)
            printf("What a pity!\n");
      }
  
      return 0; 
}