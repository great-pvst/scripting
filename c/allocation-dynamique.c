#include <stdio.h>
#include <stdlib.h>

/*
allocation dynamique
    on s'en sert le plus souvent pour créer des tableaux. elle permet de créer un tableau qui a exactement la taille d'une variable.
*/

//prototype malloc
void* malloc(size_t nombre_octets_necessaires);
/*
cette fonction renvoie un pointeur indiquant l'adresse reservee par le système. ce sera un pointeur sur n'importe quel type. on peut dire que c'est un pointeur universel.
si l'allocation échoue, notre pointeur contiendra l'adresse NULL.
*/

//prototype free
void free(void* pointeur); //ici pointeur = memoire_allouee


int main (int argc, char* argv[]){

    printf("taille de int = %d octets\n", sizeof(int));

    int* mem_allouee = NULL;

    mem_allouee = malloc(sizeof(int));

    if (mem_allouee == NULL) // Si l'allocation a échoué
    {
        exit(0); // On arrête immédiatement le programme
    }

    // On peut continuer le programme normalement sinon
    printf("\nQuel âge avez-vous ? ");
    scanf("%d", mem_allouee);
    printf("Vous avez %d ans\n\n", *mem_allouee);

    //fin d'utilisation de la mémoire, on la libère
    free(mem_allouee);

    //illustration allocation dynamique
    int nb_d_amis = 0, i;
    int* age_amis = NULL; // Ce pointeur va servir de tableau après l'appel du malloc

    // On demande le nombre d'amis à l'utilisateur
    printf("Combien d'amis avez-vous ? "); 
    scanf("%d", &nb_d_amis);

    if (nb_d_amis > 0) // Il faut qu'il ait au moins un ami
    {
        age_amis = malloc(nb_d_amis * sizeof(int)); // On alloue de la mémoire pour le tableau
        if (age_amis == NULL) // On vérifie si l'allocation a marché ou non
        {
            exit(0);
        }

        // On demande l'âge des amis un à un
        for (i = 0 ; i < nb_d_amis ; i++)
        {
            printf("Quel âge a l'ami numero %d ? ", i + 1);
            scanf("%d", &age_amis[i]);
        }

        // On affiche les âges stockés un à un
        printf("\nVos amis ont respectivement les âges suivants :\n");
        for (i = 0 ; i < nb_d_amis ; i++)
        {
            printf("%d ans\n", age_amis[i]);
        }

        // On libère la mémoire allouée
        free(age_amis);

    return 0;
    }
}