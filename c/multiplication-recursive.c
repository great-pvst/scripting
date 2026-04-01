// affiche une multiplication recursive
#include <stdio.h>
#include <stdlib.h>



void multiplication_recursive(int a, int b) {
while (b > 0 && a > 0)
{
	if (b%2 != 0){
		printf("%i * %i = %d * %d + %d \n", a,b,a,b-1,a);
		b--;
	}
	
	else {
		printf("%i * %i = %d * %d \n", a,b,a*2,b/2);
		b--;
	}
		
}
}


int main(int argc, char* argv[])
{
	int a = 0, b = 0;

	printf("Multiplication récursive\n\nEntrez le multiplicande (constante) : "); scanf("%d", &a);
	printf("Entrez le multiplicateur (variable) : "); scanf("%d", &b); printf("\n");
	
	multiplication_recursive(a,b);
//-----------------------------------------------------------------------------------------

return 0;
}