// typing mark simulation

#include <stdio.h>
#include <stdlib.h>
#define TAILLE_MAX 100

/*

*/

int main (void) {
float notes[TAILLE_MAX] = {0};
float plusG = 0, plusP = 0, somme = 0, moyenne = 0;
int p = 0, g = 0, supMoyenne = 0, compteur = 0;

printf("Saisissez des notes (entre 0 et 20, sinon erreur) !\n\n");
//store the marks 
for (int i = 0; i < TAILLE_MAX; i++){
	scanf("%f", &notes[i]);
	if ((notes[i] >= 0) && (notes[i] <= 20)){
		somme += notes[i];
		compteur++;
	} else {
		printf("Erreur lors de la saisie de notes.\n");
		notes[i] = 0;
		break;
	}
}

//print marks
for (int i = 0; i < compteur; i++){ //notes[i] != 0
	printf("%.2f", notes[i]);
	if(i+1 == 0)
		break;
	else
		printf(", ");

}
printf("\nVous avez saisi %d notes.\n", compteur);

moyenne = somme/compteur; printf("Moyenne = %.2f\n", moyenne);
for (int i = 0; i < compteur; i++){ //notes[i] != 0
	if (notes[i] > moyenne){
		printf("%.2f supérieur à la moyenne\n", notes[i]);
		supMoyenne++;
	}
	else if (notes[i] < moyenne)
		printf("%.2f inférieur à la moyenne\n", notes[i]);
	else
		printf("%.2f égal à la moyenne\n", notes[i]);
}
printf("%i note(s) est ou sont supérieure(s) à la moyenne.\n", supMoyenne);

plusG = plusP = notes[0];
for (int i = 0; i < compteur; i++){ //notes[i] != 0
	if (notes[i] >= plusG){
		plusG = notes[i];
		g = i+1;
	}
}
for (int i = 0; i < compteur; i++){ //notes[i] != 0
	if(notes[i] <= plusP){
		plusP = notes[i];
		p = i+1;
	}
}

printf("Note max = %.2f, trouvée à la position %d.\n", plusG, g);
printf("Note min = %.2f, trouvée à la position %d.\n", plusP, p);

return 0;
}