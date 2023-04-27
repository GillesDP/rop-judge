#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
  
  printf("BEFORE:\n");
  print_stack((size_t*) &buffer, 10);

  int i = 0;
  while (buffer[i] != (size_t) __builtin_return_address(0)) i++;
  buffer[i] = (size_t) &do_something;
  i++;

  char* token = strtok(stack, "\n");
  while (token != NULL) {
    buffer[i] = (size_t) strtol(token, NULL, 16);
    token = strtok(NULL, "\n");
    i++;
  }

  printf("AFTER:\n");
  print_stack((size_t*) &buffer, 10);
}

int main(int argc, char *argv[]) {
  attack(argv[1]);
  return 0;
}
