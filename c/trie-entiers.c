#include <stdio.h>
#include <stdlib.h>
//ce programme trie les éléments par ordre croissant

void affiche_tab(int tab_entiers[]);
void tri_tab(int tab_entiers[], int longueur_tab);
void echanger(int* i, int* j);

int main(){
    int tab_entiers[22] = {15,20,19,12,0,5,8,6,10,14,3,1,18,13,16,2,7,4,21,9,17,11};
    printf("\tVoici une série de valeurs.\n");
    affiche_tab(tab_entiers);
    printf("\n\nNous l'avons ordonée !\n");
    tri_tab(tab_entiers, 22); printf("\n");

return 0;
}

void echanger(int* i, int* j) {
    int temp;

    temp = *i;
    *i = *j;
    *j = temp;
}

void affiche_tab(int tab_entiers[]){
    for (int i = 0; i < 22; i++) printf("%d ", *(tab_entiers + i));
}

void tri_tab(int tab_entiers[], int longueur_tab){
    //affiche_tab(tab_entiers);
    int min = 0;
    
    for (int i = 0; i < longueur_tab-1; i++){
        min = i;
        for (int j = i+1; j < longueur_tab; j++){
            if (tab_entiers[j] < tab_entiers[min]) min = j;
        }
        if (min != i) echanger(&tab_entiers[i], &tab_entiers[min]);
    }
    affiche_tab(tab_entiers);
}

// pistes
// - ajouter une autre fonction de tri différente (tri à bulles, tri par insertion, tri rapide, etc.) et comparer les résultats
// - proposer la saisie d'une série de valeurs à trier par l'utilisateur