#include <stdio.h>

int main()
{
	int n;
	int r = 0;
	while (1)
	{
		scanf("%d", &n);
		if (!n) break;

		r = 0;
		n = 2 * n - 1;
		for (int i = 0; i < n; i++)
		{
			int c;
			scanf("%d", &c);
			r ^= c;
		}

		printf("%d\n", r);
	}

	return 0;
}