#include<iostream>
using namespace std;
int main()
{
 int T;
 cin>>T;
 for(int i=1;i<=T;i++)
 {
  int N;
  cin>>N;
  for(int k=0;k<N;k++)
  {
   char Name[N];
   int Score[N];
   cin>>Name[k]>>Score[k];
   char daizhenyang;
   for(int i=0;i<N;i++)
   {
     if(Name[i]==daizhenyang)
     {
      if(Name[0]==daizhenyang)
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