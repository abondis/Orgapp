#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct task {
  char description[200];
  char *project;
  char *context;
  struct task *next;
};

void appendLine (FILE *fp, char *buffer);
void prepareFile (FILE *fp); 
void populateTasks (FILE *fp, struct task *tasks);
void viewTasks (struct task *tasks);
void dumpTasks();
/* generate a string from tasks in memory to save to file*/
void addTask();
/* add a task and save it in the file */
void moveTask();
/* moves a task from one position to another one and save to file*/
void getTasksByKeyword();
/* t get @home +project1
or t get +projet1 +projet2
or t get blah
*/
/* parse a line for task, +project and @context and returns a task */
struct task *parseLine(char *line);


int main() {
  FILE *fp;
  char *buffer;
  struct task *tachesHead;
  struct task *tachesCur;
  tachesHead = malloc( sizeof(struct task));
  tachesHead->next = 0;
  tachesCur = tachesHead;
  fp = fopen("blah.txt", "a");
  close(fp);
  fp = fopen("blah.txt", "r+");
  /*prepareFile(fp);*/
  populateTasks(fp, tachesCur);
  tachesCur = tachesHead;
  viewTasks(tachesCur);
  printf("dump tasks\n");
  tachesCur = tachesHead;
  dumpTasks(fp, tachesCur);
  fclose(fp);
}

void appendLine(FILE *fp, char *buffer) {
  size_t str_length;
  str_length = strlen(buffer);
  fwrite(buffer, str_length, 1, fp);
}

/*void prepareFile(FILE *fp) {
  fputs("premiere ligne\n", fp);
  fputs("deuxieme ligne\n", fp);
  fputs("troisieme ligne\n", fp);
  fputs("4eme ligne\n", fp);
  fputs("5eme ligne 9utnar  yaun uan \n", fp);
  fflush(fp);
}*/



void viewTasks (struct task *tasks){
  int cpt = 1;
  while ( tasks->next != NULL ) {
    printf("Tache no %d: %s", cpt, tasks->description);
    tasks = tasks->next;
    cpt++;
  }
} 

/* generate a string from tasks in memory to save to file
can be used for later functions like moving when we can get started from the cursor's position
*/
void dumpTasks(FILE *fp, struct task *tasks){
  while ( tasks->next != NULL ) {
    if ( (tasks->project == NULL) || (tasks->project == "")){
       tasks->project = malloc(sizeof(char *));
       tasks->project = "";
    }
    else {
      strcat(tasks->project, " ");
    }
    if ( (tasks->context == NULL)|| (tasks->context == "")){
       tasks->context = malloc(sizeof(char *));
       tasks->context = "";
    }
    else {
      strcat(tasks->context, " ");
    }
    printf("%s%s%s", tasks->context, tasks->project, tasks->description);
    tasks = tasks->next;
  }
}

/* parse a line for task, +project and @context and returns a task */
struct task *parseLine(char *line){
  struct task *tmpT = malloc(sizeof(struct task));
  int soc = sizeof(char *);
  char *proj, *cont, *tok;
  char desc[200];
  strcpy(desc, "");
  proj = malloc(soc);
  cont = malloc(soc);
  tmpT->context = malloc(soc);
  tmpT->project = malloc(soc);
  /* cf test/parsetask.c */
  tok = strtok( line, " ");
  while (tok != NULL){ 
    if ( strstr(tok, "@") != NULL) {
      strcpy(tmpT->context, tok );
    }
    else if ( strstr(tok, "+") != NULL) {
      strcpy(tmpT->project, tok );
    }
    else {
      strcat(desc, tok);
    }
    tok = strtok( NULL, " ");
  }
  strcpy(tmpT->description, desc);
  /* ?? comment faire le pare de la description ?
  free(proj);
  free(cont);
  free(tmpT);*/
  return(tmpT);
}

void populateTasks (FILE *fp, struct task *tasks){
  char tmpTask[200];
  struct task *parsed = malloc(sizeof(struct task *));
  rewind(fp);
  while (fgets(tmpTask, 4096, fp) != NULL) {
    printf("populating task %s", tmpTask);
    parsed = parseLine(tmpTask);
    memcpy(tasks, parsed, sizeof(*parsed));
    tasks->next = malloc( sizeof(struct task) );
    tasks = tasks->next;
    tasks->next = 0;
  } 
}

/* loads all the line in description
void populateTasks (FILE *fp, struct task *tasks){
  char tmpTask[200];
  rewind(fp);
  while (fgets(tmpTask, 4096, fp) != NULL) {
    strcpy(tasks->description, tmpTask);
    tasks->next = malloc( sizeof(struct task) );
    tasks = tasks->next;
    tasks->next = 0;
  } 
}
*/
