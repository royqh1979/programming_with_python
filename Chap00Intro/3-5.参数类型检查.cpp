#include <stdio.h>

int add(int a,int b){
	return a+b;
}

int main(){
	int sum,sum2;
	sum=add(3,5);
	printf("%d\n",sum);
	sum2=add(3,"ÄãºÃ!");
	printf("%d\n",sum2);
	return 0; 
}
