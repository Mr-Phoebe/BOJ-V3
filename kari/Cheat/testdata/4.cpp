#include<stdio.h>
#include<string.h>
main()
{
      int T,N,i,j,k,q,x[10000],p;
      char a[10000][100];
      scanf("%d",&T);
      for(j=1,p=0;j<=T;j++)
      {
         scanf("%d",&N);
         for(i=0;i<=N-1;i++)
         {
             scanf("%s %d",a[i],&x[i]);
             if(x[i]>p)
                p=x[i]; 
         }
         for(i=0,q=0;i<=N-1;i++)
         {
            if(strcmp(a[i],"daizhenyang")==0)
            {
               if(x[i]==p)
                  printf("Daizhenyang is the champion of the world!\n");
               else
                  printf("I can not believe that!\n");
               q=1;
               break;
            }
         }
         if(q==0)
            printf("What a pity!\n");
      }
  
      return 0; 
}
