#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main()
{
    short T,i,j;
    int N,score[100],k=10000,temp;
    char a[20];
    scanf("%hd",&T);
    while(T--)
    {
              i=0;
              scanf("%d",&N);
              while(N--)
              {
                        getchar();
                        scanf("%s%d",a,&score[i]);
                        if(strcmp(a,"daizhenyang")==0)
                        {
                             k=score[i];
                             j=i;
                         }
                             i++;
              }
              while(i--)
              {
                        if(score[i]>k)
                        {
                              k=score[i];
                              printf("I can not believe that!\n"); 
                              break;      
                        }
                        else if(k==10000)
                        {
                             printf("What a pity!\n");
                             break; 
                        }                
              }
              if(score[j]==k&&k!=10000)
              printf("Daizhenyang is the champion of the world!\n");
              k=10000;
    }
    return 0;
}
