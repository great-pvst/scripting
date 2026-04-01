#include <stdlib.h>
#include <stdio.h>

#define TAILLE_MAX 1000 //taille des tableaux
/*on peut lire et écrire dans des fichiers en langage C. */

//prototype fopen
FILE* fopen(const char* nom_du_fichier, const char* mode_ouverture);
/*
mode d'ouverture = soit seulement écrire soit seulement écrire ou encore les deux à la fois
    "r" = lecture seule (fichier existant au préalable). plus souvent utilisé
    "w" = écriture seule. plus souvent utilisé
    "a" = mode ajout (écrire en partant de la fin du fichier)
    "a+" = ajout en lecture/ écriture à la fin
    "r+" = lecture et écriture (fichier existant au préalable). plus souvent utilisé
    "w+" = lecture et écriture, avec suppression du contenu au préalable (le fichier est d'abord vidé de son contenu)
*/

//prototype fclose
int fclose(FILE* pointeur_sur_fichier);
/*
cette fonction renvoie un int : soit 0 (fermeture réussie) soit EOF (fermeture échouée).
EOF = End Of File
*/

//prototype fputc
int fputc(int caractere, FILE* pointeur_sur_fichier);
/*
la fonction retourne un int. EOF si l'écriture a échoué, sinon une autre valeur.
*/

//prototype fputs
int fputs(const char* chaine, FILE* pointeur_sur_fichier);
/*
même retour que fputc. la constante siginifie que la chiane ne pourra pas faire l'objet de modifications.
*/

//prototype fgetc
int fgetc(FILE* pointeur_sur_fichier);
/*
retourne un int. EOF si échec de la lecture, la valeur du caractère si réussi.
fgetc change de position à chaque appel, c-à-d elle lit le premier caractère puis le deuxième ainsi de suite. on peut
donc boucler pour rechercher un caractère donné ou afficher le contenu lu.
*/

//prototype fgets
char* fgets(char* chaine, int nb_caractere_a_lire, FILE* pointeur_sur_fichier);
/*
elle lit au maximum une ligne. faire une boucle pour plusieurs lignes. préciser le nombre de caractères à lire peut
éviter un dépassement de mémoire.
la fonction retourne NULL en cas d'échec de lecture.
code pour lire plus d'une ligne avec fgets.
    while (fgets(chaine, TALLE_MAX, fichier) != NULL);
        {
            printf("%s", chaine);
        }
*/

//prototype ftell
long ftell(FILE* pointeur_sur_fichier);
//renvoie la position sous forme de long. le nombre renvoyé correspond donc à la position

//prototype fseek
int fseek(FILE* pointeur_sur_fichier, long deplacement, int origine);
/*
permet de déplacer le curseur d'un certain nombre de cractère (deplacement) à partir de la position d'"origine"
deplacement : peut être un nombre positif(en avant), nul (= 0) ou négatif (en arrière)
origine : prend généralement l'une des trois constantes (des define)
    SEEK_SET : indique le début du fichier
    SEEK_CUR : indique la position actuelle du curseur
    SEEK_END : indique la fin du fichier

    exemple
        fseek(fichier, 2, SEEK_SET); //ce code place le curseur deux caractères après le début
        fseek(fichier, 0, SEEK_END); //place le curseur à la fin du fichier
*/

//prototype rewind
void rewind(FILE* pointeur_sur_fichier);
/*
remet le curseur à la position zéro 0
*/

//prototype rename
int rename(const char* ancien_nom, const char* nouveau_nom);
/*
elle renvoie 0 si elle a réussi à renommer, sinon elle renvoie une valeur différente.
*/

//prototype remove
int remove(const char* fichier_a_supprimer);
/*
elle supprime sans démander de confirmation. le fichier est supprimé du disque dur (pas dans le Trash)
*/

int main (int argc, char *argv[])
{
    FILE* fichier = NULL;
    char chaine[TAILLE_MAX];

    fichier = fopen("text.txt", "r");

//on vérifie à chaque fois si l'ouverture est réussie ou pas.
    if (fichier != NULL)
    {
    // On peut écrire dans le fichier
/* 
        fputc('A', fichier);
        fputs("Salut chef !\nAlors comment se déroule ton apprentissage ?", fichier);
        fprintf(fichier,"J'ai %d ans.", age);
*/

    // On peut lire dans le fichier
/*
        do {
            caractere_lu = fgetc(fichier);
            printf("%c", caractere_lu);
        } while (caractere_lu != EOF);
*/
    fgets(chaine, TAILLE_MAX, fichier);
    printf("%s", chaine);


        fclose(fichier); //fermeture du fichier
    }
    else
    {
        // On affiche un message d'erreur si on veut
        printf("Impossible d'ouvrir le fichier text.txt");
    }

    //rename("text.txt", "test.txt");

    //remove("test.txt");


    return 0;
}
