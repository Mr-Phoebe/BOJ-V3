nclude <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAXV -1

int main()
{
        int t, n, ax, ay, bx, by, j;

            int minv, T, P, Q;

                scanf("%d", &t);
                    while(t--){
                                scanf("%d", &n);
                                        scanf("%d", &ax);
                                                minv = -1;
                                                        bx = by = -100000000;
                                                                for(j = 1; j
                                                                    <= n - 1;
                                                                    j++){
                                                                                scanf("%d",
                                                                                &ay);
                                                                                            if(!minv)
                                                                                                continue;
                                                                                                            if(ax
                                                                                                                &
                                                                                                                1)
                                                                                                                P
                                                                                                                =
                                                                                                                (ax
                                                                                                                >> 1)
                                                                                                                >> +
                                                                                                                >> 1;
                                                                                                                            else
                                                                                                                                P
                                                                                                                                =
                                                                                                                                ax
                                                                                                                                >> 1;
                                                                                                                                            if(by
                                                                                                                                                !=
                                                                                                                                                -100000000
                                                                                                                                                &&
                                                                                                                                                P
                                                                                                                                                <
                                                                                                                                                ax
                                                                                                                                                - by)
                                                                                                                                                  P
                                                                                                                                                  =
                                                                                                                                                  ax
                                                                                                                                                  - by;
                                                                                                                                                              
                                                                                                                                                                          Q
                                                                                                                                                                          =
                                                                                                                                                                          ay
                                                                                                                                                                          >> 1;
                                                                                                                                                                                      if(bx
                                                                                                                                                                                          !=
                                                                                                                                                                                          -100000000
                                                                                                                                                                                          &&
                                                                                                                                                                                          Q
                                                                                                                                                                                          > ax
                                                                                                                                                                                          > -
                                                                                                                                                                                          > bx)
                                                                                                                                                                                          > Q
                                                                                                                                                                                          > =
                                                                                                                                                                                          > ax
                                                                                                                                                                                          > -
                                                                                                                                                                                          > bx;
                                                                                                                                                                                                      if(Q
                                                                                                                                                                                                          <
                                                                                                                                                                                                          P){
                                                                                                                                                                                                                          minv
                                                                                                                                                                                                                          =
                                                                                                                                                                                                                          0;
                                                                                                                                                                                                                                          continue;
                                                                                                                                                                                                                                                      }
                                                                                                                                                                                                                                                                  T
                                                                                                                                                                                                                                                                  =
                                                                                                                                                                                                                                                                  Q
                                                                                                                                                                                                                                                                  - P
                                                                                                                                                                                                                                                                    +
                                                                                                                                                                                                                                                                    1;
                                                                                                                                                                                                                                                                                if(minv
                                                                                                                                                                                                                                                                                    ==
                                                                                                                                                                                                                                                                                    -1
                                                                                                                                                                                                                                                                                    ||
                                                                                                                                                                                                                                                                                    T
                                                                                                                                                                                                                                                                                    <
                                                                                                                                                                                                                                                                                    minv)
                                                                                                                                                                                                                                                                                    minv
                                                                                                                                                                                                                                                                                    =
                                                                                                                                                                                                                                                                                    T;
                                                                                                                                                                                                                                                                                                ax
                                                                                                                                                                                                                                                                                                =
                                                                                                                                                                                                                                                                                                ay;
                                                                                                                                                                                                                                                                                                            bx
                                                                                                                                                                                                                                                                                                            =
                                                                                                                                                                                                                                                                                                            P;
                                                                                                                                                                                                                                                                                                                        by
                                                                                                                                                                                                                                                                                                                        =
                                                                                                                                                                                                                                                                                                                        Q;
                                                                                                                                                                                                                                                                                                                                }
                                                                                                                                                                                                                                                                                                                                        printf("%d\n",
                                                                                                                                                                                                                                                                                                                                        minv);
                                                                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                                                                                return
                                                                                                                                                                                                                                                                                                                                                0;
}
