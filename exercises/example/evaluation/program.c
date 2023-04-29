#include <signal.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

extern char __executable_start;

int attack() {
  printf("ATTACKED!\n");
  return 1;
}

void exploit(char* stack) {
  size_t buffer[1] = {0xFF};
  int i = 0;
  while (buffer[i] != (size_t) __builtin_return_address(0)) i++;
  char* token = strtok(stack, "|");
  while (token != NULL) {
    #ifdef __PIE__
      buffer[i] = (size_t) (strtol(token, NULL, 16) + &__executable_start);
    #else
      buffer[i] = (size_t) strtol(token, NULL, 16);
    #endif
    token = strtok(NULL, "|");
    i++;
  }
}

int main(int argc, char *argv[]) {
  if (argc != 2) exit(0);
  signal(SIGSEGV, exit);
  exploit(argv[1]);
  return 0;
}