#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//programme qui dit combien de fois un caractère est présent dans une chaîne

int recherche_caractere(char mot[], char caractere[]);

int main(int argc, char *argv[]){
    char mot_saisi[200], caractere_saisi[100];
    printf("  Ce code affiche le nombre de fois qu'un caractère est présent dans une chaîne.\n\n");
    printf("Saisissez un mot (même insignifiant) : "); scanf("%s", &mot_saisi);
    printf("Quel caractère cherchez-vous (respectez la casse) : "); scanf("%s", &caractere_saisi);
    int nb_fois = recherche_caractere(mot_saisi, caractere_saisi);
    printf("Le caractère %s se trouve %d fois dans le mot %s !\n", caractere_saisi, nb_fois, mot_saisi);
    return 0;
}

int recherche_caractere(char mot[], char caractere[]){
    int nb_fois = 0;
    for (unsigned long i = 0; i <= strlen(mot); i++){ //mot[i] != ' '
        if (mot[i] == caractere[0])
            nb_fois++;
        }

    return nb_fois;
}