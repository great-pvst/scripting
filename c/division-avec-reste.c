// division
#include <stdio.h>
#include <stdlib.h>


void division_avec_reste(int dividende, int diviseur)
{
	int q = 0;
	while (dividende - diviseur >= 0)
	{
		dividende = dividende - diviseur;
		q++;
	}
	printf ("Quotient = %d et Reste = %d\n", q, dividende);
}



int main(){
	printf("Division sans opérande '/', du plus grand entier par le plus petit\n");
	
	int a = 0, b = 0;
	printf("Entier 1 : "); scanf("%d", &a); printf("Entier 2 : "); scanf("%d", &b);

	if (a > b) division_avec_reste(a,b);
	else division_avec_reste(b,a);
	

return 0;
}