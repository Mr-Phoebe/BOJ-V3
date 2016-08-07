#include <iostream>
#include <cmath>
#include <algorithm>
#include <iomanip>
 
using namespace std;

const double EPS = 1e-8;
const int N = 10000 + 3;
 
struct Point
{
    double x;
    double y;
};
 
double xmult(Point a, Point b, Point c)   
{
    return (((b.x - a.x) * (c.y - a.y)) - (c.x - a.x) * (b.y - a.y));
}
bool cmp(Point a, Point b)
{
    if (fabs(a.y - b.y) <= EPS)
        return a.x < b.x;
    return a.y < b.y;
}

double Area(Point *p, int nv)
{
    if (nv < 3) return 0;
    int i;
    double ret = 0;
    for (i = 2; i < nv; i++)
    {
        ret += xmult(p[0], p[i - 1], p[i]) / 2.0;
    }
    return ret;
}

int Graham_Scan(Point *p, int nv, Point *res)  
{
    int i, top;
 
    sort(p, p + nv, cmp);
    if (nv < 0) return 0;
    res[0] = p[0];
    if (nv == 1) return 1;
    res[1] = p[1];
    if (nv == 2) return 2;
   
    top = 1;
    for (i = 2; i < nv; i++)   
    {
        while (top >= 1 && xmult(res[top], res[top - 1], p[i]) > 0) top--;
        res[++top] = p[i];
    }
    for (i = nv - 2; i >= 0; i--)
    {
        while (top >= 1 && xmult(res[top], res[top - 1], p[i]) > 0) top--;
        res[++top] = p[i];
    }
 
    return top;
}
 
 
Point p[N], res[N];
int main(){  
    unsigned long int n,p,q;  
    while(1){  
        scanf("%d", &n);  
        if(n==0)  
            break;  
        p=0;  
        for(int i=0;i<2*n-1;i++){  
            scanf("%d",&q);  
            p=p^q;  
        }  
        printf("%d\n",p);  
    }  
    return 0;  
}

