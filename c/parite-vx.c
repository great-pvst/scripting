#include <stdio.h>
#include <stdlib.h>

//programme qui renvoie 1 si un nombre est impair, 0 sinon.
int parite(int nombre);

int main(){
int nombre_saisi = 0;
printf("\tMachine qui dit la parité d'un nombre.\n\nEntrez un nombre : ");
scanf("%d", &nombre_saisi);
if (parite(nombre_saisi))
    printf("%d est pair.\n", nombre_saisi);
else
    printf("%d est impair.\n", nombre_saisi);
return 0;
}

int parite(int nombre){
if (nombre % 2 == 0)
    return 1;
else
    return 0;

}