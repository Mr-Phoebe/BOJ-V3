#include<stdio.h>
#include<stdlib.h>
int main()
{
    
    int T,n,i,l,k,daming,chengji,max;
    char m[]="daizhenyang",a[20];
    
    scanf("%d",&T);
    for(k=1;k<=T;k++)
      {fflush(stdin);
       scanf("%d",&n);
       max=0;
       for(daming=0,l=1;l<=n;l++)
         {scanf("%s %d",a,&chengji);
          for(i=0;a[i]!='\0'&&m[i]!='\0';i++);
          if(a[i]=='\0'&&m[i]=='\0')
            daming=chengji;
          else{
               if(chengji>=max)
                  max=chengji;
               }
               }
       if(daming!=0&&daming>=max)
          printf("Daizhenyang is the champion of the world!\n");
       else if(daming!=0)
          printf("I can not believe that!\n");
          else
          printf("What a pity!\n");
       }
       return 0;
}
