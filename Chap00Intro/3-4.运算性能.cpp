#include <time.h> 
#include <stdio.h> 

long long sum(int n){
	int i;
	long long s=0;
	for (i=1;i<=n;i++) {
		s=s+i;
	}
	return s;
}

int main(){
	time_t start,end;
	int elasped;
	int i;
	long long t=0;
	start=clock();
	for (i=0;i<1000;i++) {
		t=t+sum(100000);
	}
	end=clock();
	elasped=end-start;
	printf("所用时间:%.3f\n", elasped/1000.0);
	printf("t=%I64d\n",t);
	return 0; 
} 

