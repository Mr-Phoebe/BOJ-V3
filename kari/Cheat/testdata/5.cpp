nclude <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_VAL -1

int main()
{
        int T, N, A0, A1, B0, B1, i;

            int min, t, p, q;

                scanf("%d", &T);
                    while(T--){
                                scanf("%d", &N);
                                        scanf("%d", &A0);
                                                min = -1;
                                                        B0 = B1 = -100000000;
                                                                for(i = 1; i
                                                                    <= N - 1;
                                                                    i++){
                                                                                scanf("%d",
                                                                                &A1);
                                                                                            if(!min)
                                                                                                continue;
                                                                                                            if(A0
                                                                                                                &
                                                                                                                1)
                                                                                                                p
                                                                                                                =
                                                                                                                (A0
                                                                                                                >> 1)
                                                                                                                >> +
                                                                                                                >> 1;
                                                                                                                            else
                                                                                                                                p
                                                                                                                                =
                                                                                                                                A0
                                                                                                                                >> 1;
                                                                                                                                            if(B1
                                                                                                                                                !=
                                                                                                                                                -100000000
                                                                                                                                                &&
                                                                                                                                                p
                                                                                                                                                <
                                                                                                                                                A0
                                                                                                                                                - B1)
                                                                                                                                                  p
                                                                                                                                                  =
                                                                                                                                                  A0
                                                                                                                                                  - B1;
                                                                                                                                                              
                                                                                                                                                                          q
                                                                                                                                                                          =
                                                                                                                                                                          A1
                                                                                                                                                                          >> 1;
                                                                                                                                                                                      if(B0
                                                                                                                                                                                          !=
                                                                                                                                                                                          -100000000
                                                                                                                                                                                          &&
                                                                                                                                                                                          q
                                                                                                                                                                                          > A0
                                                                                                                                                                                          > -
                                                                                                                                                                                          > B0)
                                                                                                                                                                                          > q
                                                                                                                                                                                          > =
                                                                                                                                                                                          > A0
                                                                                                                                                                                          > -
                                                                                                                                                                                          > B0;
                                                                                                                                                                                                      if(q
                                                                                                                                                                                                          <
                                                                                                                                                                                                          p){
                                                                                                                                                                                                                          min
                                                                                                                                                                                                                          =
                                                                                                                                                                                                                          0;
                                                                                                                                                                                                                                          continue;
                                                                                                                                                                                                                                                      }
                                                                                                                                                                                                                                                                  t
                                                                                                                                                                                                                                                                  =
                                                                                                                                                                                                                                                                  q
                                                                                                                                                                                                                                                                  - p
                                                                                                                                                                                                                                                                    +
                                                                                                                                                                                                                                                                    1;
                                                                                                                                                                                                                                                                                if(min
                                                                                                                                                                                                                                                                                    ==
                                                                                                                                                                                                                                                                                    -1
                                                                                                                                                                                                                                                                                    ||
                                                                                                                                                                                                                                                                                    t
                                                                                                                                                                                                                                                                                    <
                                                                                                                                                                                                                                                                                    min)
                                                                                                                                                                                                                                                                                    min
                                                                                                                                                                                                                                                                                    =
                                                                                                                                                                                                                                                                                    t;
                                                                                                                                                                                                                                                                                                A0
                                                                                                                                                                                                                                                                                                =
                                                                                                                                                                                                                                                                                                A1;
                                                                                                                                                                                                                                                                                                            B0
                                                                                                                                                                                                                                                                                                            =
                                                                                                                                                                                                                                                                                                            p;
                                                                                                                                                                                                                                                                                                                        B1
                                                                                                                                                                                                                                                                                                                        =
                                                                                                                                                                                                                                                                                                                        q;
                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                        printf("%d\n",
                                                                                                                                                                                                                                                                                                                                        min);
                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                0;
}
