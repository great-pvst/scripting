#ifndef MAIN_H_INCLUDED
#define MAIN_H_INCLUDED
 //strucutre
typedef struct Identite Identite;
struct Identite
{
    char nom[100];
    char prenom[100];
    char adresse[1000];
    int age;
};

typedef struct Coordonnees Coordonnees;
struct Coordonnees
{
    int x;
    int y;
    int z;

};

//énumération
typedef enum Mention Mention;
enum Mention
{
    NUL = 8, PASSABLE = 11, BIEN = 15, EXCELLENT = 20
};

#endif // MAIN_H_INCLUDED
