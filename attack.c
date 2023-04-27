#include <stdio.h>
#include <stdlib.h>

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
  printf("ATTACKED!");
  return 0;
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

int main(int argc, char *argv[]) {
  size_t marker = 0xFF;

  printf("BEFORE:\n");
  print_stack(&marker, 20);

  printf("<main> address: %p\n", &main);
  printf("<do_something> address: %p\n", &do_something);
  
  marker = strtol(argv[1], NULL, 16);

  printf("AFTER:\n");
  print_stack(&marker, 20);

  return 0;
}
