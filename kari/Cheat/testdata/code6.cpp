#include<iostream.h>
using namespace std;
int main()
{
 int cas;
 cin>>cas;
 for(int j=1;j<=cas;j++)
 {
  int m;
  cin>>m;
  for(int i=0;i<m;i++)
  {
   char a[m];
   int b[m];
   cin>>a[i]>>b[i];
   char daizhenyang;
   for(int k=0;k<m;k++)
   {
     if(a[k]==daizhenyang)
     {
      if(a[0]==daizhenyang)
     {
      cout<<"Daizhenyang is the champion of the world!"<<endl;
     }
     else{cout<<"I can not believe that!"<<endl;}
     }
     else{cout<<"What a pity!"<<endl;}
   }
  }
 }
}