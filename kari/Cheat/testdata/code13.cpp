#include <cstdio>
 
const int MAXN = 1024;
int B[MAXN], C[MAXN];
 
#define LOWBIT(x) ((x)&(-(x)))

//插入单个元素 
void bit_update(int *a, int p, int d) {
	for ( ; p && p < MAXN ; p += LOWBIT(p))
		a[p] += d;
}

//查询区间
int bit_query(int *a, int p) {
	int s = 0;
	for ( ; p ; p -= LOWBIT(p))
		s += a[p];
	return s;
}
 
//插入区间
void bit_update2(int *a, int p, int d) {
	for ( ; p ; p -= LOWBIT(p))
		a[p] += d;
}

//查询单个元素值 
int bit_query2(int *a, int p) {
	int s = 0;
	for ( ; p && p < MAXN ; p += LOWBIT(p))
		s += a[p];
	return s;
}
 
inline void _insert(int p, int d) {
	bit_update(B, p, p*d);
	bit_update2(C, p-1, d);
}
 
inline int _query(int p) {
	return bit_query(B, p) + bit_query2(C, p) * p;
}
 
inline void insert_seg(int a, int b, int d) {
	_insert(a-1, -d);
	_insert(b, d);
}
 
inline int query_seg(int a, int b) {
	return _query(b) - _query(a-1);
}
 
int main() {
	int com, a, b, c;
	while (scanf("%d%d%d",&com,&a,&b) != EOF) {
		a += 2; b += 2;		//防止出现负数
		if (com == 0) {		//更新
			scanf("%d",&c);
			insert_seg(a, b, c);
		} else {			//查询
			printf("%d\n",query_seg(a,b));
		}
	}
	return 0;
}