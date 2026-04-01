// print all pair numbers after user typing
#include <stdio.h>
#include <stdlib.h>

/*

des fonctions ?

*/

int main(int argc, char* argv[])
{
unsigned int nb_entre = 0;
printf("\n***Ce bout affiche tous les nombres pairs entre 0 et le nombre entré.***\n");
//----------------------------------------------------

printf("Entrez un entier positif : "); scanf("%d", &nb_entre);
for (unsigned int i = 0; i < nb_entre; i += 2) printf("%d ", i);

printf("\n");

//----------------------------------------------------
return 0;
}
