#include <stdio.h>
#include <stdlib.h>
main()
{
	int T, N, count = 1;
	scanf("%d", &T);
	while(T--)
	{
		scanf("%d", &N);
		printf("Case #%d: Alice\n", count++);
	}
}