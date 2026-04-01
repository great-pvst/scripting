// reverse letters 
#include <stdio.h>
#include <stdlib.h>


int longueur_mot(char chaine[]);
void affichage_inverse_mot(char mot[]);

int main (int argc, char *argv[]){
	int nb_caractere = 0;
	char tableau_mot[100];

    printf("Saisissez un mot : ");
    scanf("%s", tableau_mot);

    affichage_inverse_mot(tableau_mot);printf("\n");

    return 0;
}

// word length
int longueur_mot(char chaine[]){
    int taille_mot = 0;

    while (chaine[taille_mot] != '\0')
        taille_mot++;

    return taille_mot;
}

//for printing the reverse word
void affichage_inverse_mot(char mot[]){
    int taille_mot = longueur_mot(mot);
    for (int i = taille_mot - 1; i >= 0; i--)
        printf("%c", mot[i]);
}