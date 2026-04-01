#include <stdio.h>
#include <stdlib.h>
#include <time.h>

//demande le resultat d'un produit entier à l'utilisateur, si faux l'utilisateur tente de nouveau
int main (int argc, char *argv[]) {
printf("Tapez le bon résultat pour quitter\n\n");

int nb_entre = 0, essai = 0, a = 0, b = 0;

do {
	essai++;
	srand(time(NULL));
	
	a =  rand() % 100 + 1; b =  rand() % 100 + 1;
	printf("%d * %d = ", a, b); scanf("%d", &nb_entre);
	
	if (a * b == nb_entre) printf("Bravo ! Vous avez trouvé en %d essai(s).\n", essai);
	else printf("Faux, recommencez !\n");
} while (nb_entre != a*b);

return 0;
}

// pistes :
// - gérer les erreurs de saisie (ex : si l'utilisateur tape une lettre au lieu d'un nombre)
// - ajouter un compteur d'essais pour que l'utilisateur puisse voir combien de fois il a tenté avant de trouver la bonne réponse
// - ajouter un système de score basé sur le nombre d'essais (ex : plus le nombre d'essais est faible, meilleur est le score)