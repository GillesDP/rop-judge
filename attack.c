#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern char __executable_start;

unsigned int telephone(unsigned int n) {
  unsigned int result = 0;

  if (n < 2)
    result = 1;
  else
  {
    unsigned int n_minus_one = telephone(n-1);
    unsigned int n_minus_two = telephone(n-2);

    result = n_minus_one + (n - 1) * n_minus_two;
  }

  return result;
}

int do_something() {
  printf("ATTACKED!\n");
  return 1;
}

void print_stack(size_t* base_address, int view) {
  for (int i = -view; i<=view; i++) {
    if (i == 0) {
      printf("-> ");
    } else {
      printf("   ");
    }
    printf("%p: %p\n", base_address+i, (void*) *(base_address+i));
  }
}

void segfault_handler(int signal) {
  // Catch segmentation faults, don't print error!
  exit(1);
}

void attack(char* stack) {
  signal(SIGSEGV, segfault_handler);

  size_t buffer[1] = {0xFF};

  int i = 0;
  while (buffer[i] != (size_t) __builtin_return_address(0)) i++;
  char* token = strtok(stack, "|");
  printf("ROP CHAIN:\n");
  while (token != NULL) {
    buffer[i] = (size_t) (strtol(token, NULL, 16) + &__executable_start);
    printf("%p: %p\n", buffer+i, (void*) buffer[i]);
    token = strtok(NULL, "|");
    i++;
  }
  printf("\n");
}

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("Syntax: ./a.out <slot1>|<slot2>|<slot3>|... where each slot is a hexidecimal value.\n");
    exit(0);
  }
  attack(argv[1]);
  return 0;
}
