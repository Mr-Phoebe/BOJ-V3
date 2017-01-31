/*
USER_ID: bupt#2016210885
PROBLEM: 287
SUBMISSION_TIME: 2017-01-31 20:31:20
*/
# include <stdio.h>
# include <string.h>
int main()
{
	char a[2][100];
	char b[50];
	char c[50];
	int i,j;
	for(i=0;i<1;i++)
	scanf("%s",a[i]);
	j=strlen(a[0]);
	for(i=0;i<j;i++)
	{
		b[i]=a[0][j-1-i];
		
	}
	for(i=0;i<j-1;i++)
	c[i+1]=b[i];
	c[0]=b[j-1];
	for(i=0;i<j;i++)
	printf("%c",c[i]);
	return 0;
}