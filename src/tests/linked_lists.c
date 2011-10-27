#include <stdio.h>
#include <stdlib.h>

typedef char * string;
struct task {
  char *description;
  struct task *next;
  string *project;
};

void setListeDeTaches (struct task *lsTasks);

int main() {
  struct task *listeDeTaches;
  struct task *tacheCourante;
  int cpt = 1;
  listeDeTaches = malloc( sizeof(struct task) ); 
  listeDeTaches->next = 0;
  tacheCourante = listeDeTaches;
  setListeDeTaches(tacheCourante);
  tacheCourante = listeDeTaches;
  while ( tacheCourante->next != NULL ) {
    printf("Tache no %d: %s\n", cpt, tacheCourante->description);
    tacheCourante = tacheCourante->next; 
    cpt++;
  }
}

void setListeDeTaches(struct task *lsTasks) {
  int i = 0;
  string desc[6] = {"desc 1","aaaa", "desc 2", "desc 2.5", "desc 3", "desc 4"};
  printf("size of desc: %d\n", sizeof(desc)/sizeof(string));
  while ( i < sizeof desc / 4) {
    lsTasks->description = desc[i];
    lsTasks->next = malloc( sizeof(struct task) );
    lsTasks = lsTasks->next;
    lsTasks->next = 0;
    i++;
  }
}
