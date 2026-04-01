//indice de masse corporelle : visite médicale
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//#define TAILLE_TAB 256

float calculImc(float m, float t){ return m/(t*t);}

int main () {
printf("\t***Pour des raisons de sécurité et de qualité, les médecins ne traiteront pas plus de 30 patients par jour***\n");
const int TAILLE_TAB = 30;
int nombrePatient = 0, compteur = 0;
float tailleMoyenne = 0, masseMoyenne = 0;
float taillePatient[TAILLE_TAB], massePatient[TAILLE_TAB], imc[TAILLE_TAB];

printf("\nEntrez les différentes tailles (en mètres) des patients (Tapez 0 pour arrêter la saisie) :\n");
//récupératon de la taille
for (nombrePatient = 0; nombrePatient < TAILLE_TAB; nombrePatient++)
{
	scanf("%e", &taillePatient[nombrePatient]);
	if (taillePatient[nombrePatient] == 0) break;
}


printf("\nLes patients sont au nombre de %d.\n", nombrePatient);

printf("Entrez, cette fois, leur masse respective (en kilogrammes) :\n");
//récupération de la masse
do
{
	scanf("%e", &massePatient[compteur]);
	compteur++;
} while (compteur < nombrePatient);

//calcul et affichage de la moyenne de taille et masse.
for(int i = 0; i <= nombrePatient; i++)
{
	tailleMoyenne += taillePatient[i];
	masseMoyenne += massePatient[i];
}

tailleMoyenne = tailleMoyenne/nombrePatient; masseMoyenne = masseMoyenne/nombrePatient;
printf("\nLes patients ont en moyenne une taille de %.2f m pour une masse moyenne de %.2f kg.\n", tailleMoyenne, masseMoyenne);
printf("%d\n", nombrePatient);

//calcul de l'indice de masse corporelle (IMC)
for (compteur = 0; compteur < nombrePatient; compteur++) imc[compteur] = calculImc((float)massePatient[compteur], (float)taillePatient[compteur]);

//affichage de celui-ci pour chaque utilisateur
for(int i = 0; i < nombrePatient; i++){
	if (imc[i] == 0) printf("Aucun calcul d'IMC n'a été effectué !\n");
	else {
        if (imc[i] < 18.5) printf("Patient %d, IMC = %.2f (faible)\n", i+1, imc[i]);
        else if(imc[i] > 25) printf("Patient %d, IMC = %.2f (trop)\n", i+1, imc[i]);
        else printf("Patient %d, IMC = %.2f (normal)\n", i+1, imc[i]);
	}
}
return 0;
}

// pistes
// - ajouter une gestion d'erreur pour les saisies (ex : taille ou masse négative, caractères non numériques, etc.)