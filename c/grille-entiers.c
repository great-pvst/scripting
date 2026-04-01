// print a number grid (1-100)
#include <stdio.h>
#include <stdlib.h>
#define TAILLETAB 100
/*

*/

int main (int argc, char* argv[]){
int tabInt2[TAILLETAB];
for (int i = 0; i < TAILLETAB; i++){
	tabInt2[i] = i;
	printf("%d", *(tabInt2 + i));
	if (i == 99) break;
	else {
		printf(",");
		if ((i + 1) % 10 == 0){
			printf("\n");
		}
	}
};
printf("\n");

return 0;
}