/*Ce sont des lignes dans le code débutant avec un dièse #. Le préprocesseur va parcourir tous les fichiers à la recherche de directives avant la compilation pour réaliser certaines modifications.

#include = inclure un fichier dans un autre
#define = associer une valeur à un mot. c'est la définition d'une constante de préprocesseur (ne prend pas de place en mémoire et s'applique à toutes les occurrences dans le code).

il existe des constantes prédéfinies par le processeur
_LINE_ : donne le numéro de la ligne
_FILE_ : donne le nom du fichier actuel
_DATE_ : donne la date de la compilation
_TIME_ : donne l'heure de la compilation
ces constantes peuvent être utiles pour gérer des erreurs

on peut réaliser des conditions en langage préprocesseur. l'intérêt est de faire des compilations conditionnelles.

à noter, il n'y a pas d'accolades en préprocesseur.

#ifdef : si la constante est définie (cas d'une constante préprocesseur définie sans valeur)
#ifndef : si la constante n'est pas définie
    permet aussi d'éviter les inclusions infinies

*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAILLE_MAX_TABLEAU 1000 //tous les tableaux seront initialisés à 1000
#define LARGEUR_FENETRE 800
#define HAUTEUR_FENETRE 600
#define NOMBRE_PIXELS (LARGEUR_FENETRE * HAUTEUR_FENETRE) //calcul simple

//création d'une macro simple, sans paramètres
#define SALUT() printf("Salut !\n"); \
                printf("Je suis MOI\n");\
                printf("Etudiant.\n");

//macro avec paramètre
#define MAJEUR(age, nom) if (age >= 18) \
                    printf("Vous avez %d ans et êtes majeur(e) %s !\n", age, nom); \
                    else \
                    printf("Vous avez %d ans et êtes mineur(e) %s !\n", age, nom);

//un peu le principe de certains programmes multi-plateformes pour s'adpater à l'OS.
#define WINDOWS

#ifdef WINDOWS
    /* Code source pour Windows */
#endif

#ifdef LINUX
    /* Code source pour Linux */
#endif

#ifdef MAC
    /* Code source pour Mac */
#endif


//modèle de tous les fichiers .h (par sécurité)
#ifndef DEF_NOM_DU_FICHIER // Si la constante n'a pas été définie le fichier n'a jamais été inclus
#define DEF_NOM_DU_FICHIER /* On définit la constante pour que la prochaine fois le fichier ne soit
plus inclus */

/* Contenu de votre fichier .h (autres include, prototypes, define...) */

#endif


int main (){
char chaine1[TAILLE_MAX_TABLEAU], chaine2[TAILLE_MAX_TABLEAU]; //taille 1000
int largeur = LARGEUR_FENETRE;

printf("%d\n", largeur);
printf("Il est %s lors de la compilation\n\n", __TIME__);

SALUT(); //appel de la macro, peut ou ne pas avoir de point-virgule

MAJEUR(19, "Inconnu"); //macro avec paramètre

return 0;
}