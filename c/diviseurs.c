// integer divisors
#include <stdio.h>
#include <stdlib.h>


int main(){
printf("Liste des diviseurs d'un entier\n\n");

long liste[1000], saisi = 0, j = 0, total = 0;
printf("Entier : "); scanf("%ld", &saisi);

if(saisi <= 0){
	printf("Valeur non permise\n");
	return 0;
}
else if(saisi == 1){
	printf("Le nombre doit être supérieur à 1... sinon ce n'est pas fun !\n"); scanf("%ld", &saisi);}
else {
	liste[j] = 1;
	for(long i = 1; i <= saisi; i++){
		if(saisi%i == 0){
			liste[j] = i;
			j++;
		}
	}
	printf("Diviseurs de %ld : [", saisi);
	for(long i = 0; j > 0; j--){
		if(j-1 == 0)
			{printf("%ld]", liste[i]);total = i+1;}
		else printf("%ld;", liste[i]);
		i++;
	}
}
printf("\nNombre total de diviseurs = %ld\n", total);


return 0;
}