/**
 * 使用goto跳转 
 */ 
#include <stdio.h>
#include <stdbool.h>

int main() {
	int a,b,c;
	goto label2;
label1:
	b=5+a;
	goto label4;
label2:
	a=10;
	goto label1;
label3:
	a+=b;
label4:
	c=50;
	if (a<c)
		goto label3;
	printf("a=%d,b=%d,c=%d",a,b,c);
	return 0;
}


