#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main ()
{
  char str[] = "+blah blah a abc @truc blah\n";
  char *str2;
  str2 = malloc(sizeof(char *));
  strcpy(str2, str);
  printf("proj %s\n", strtok(strstr( str, "+"), " "));
  strcpy(str, str2);
  printf("cont %s\n", strtok(strstr( str2, "@"), " "));
  return 0;
}
