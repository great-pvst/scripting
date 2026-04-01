#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//programme qui remplace les voyelles (majuscules et minuscules) d'un mot par des espaces

void change_voyelle(char mot[]);

int main(){
    char chaine[255];
    printf("\tCe code remplace les voyelles par un espace\n\n");
    printf("Saisissez un mot : "); scanf("%s", chaine);
    change_voyelle(chaine);
    printf("%s\n", chaine);


    return 0;
}

void change_voyelle(char mot[]){
    char voyelle[]= {"aAeEiIoOuUyY"};
    unsigned long i = 0;
    while (i < strlen(mot)){
        for (unsigned long j = 0; j < strlen(voyelle); j++){
            if (mot[i] == voyelle[j])
                mot[i] = ' ';
            }
        i++;
    }
}