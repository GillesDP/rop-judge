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

void attack() {
  size_t buffer[1];

  printf("BEFORE:\n");
  print_stack((size_t*) &buffer, 20);

  printf("<do_something> address: %p\n", &do_something);
  printf("<attack> return address: %p\n", __builtin_return_address(0));

  buffer[4] = (size_t) &do_something;

  printf("AFTER:\n");
  print_stack((size_t*) &buffer, 20);
}

int main(int argc, char *argv[]) {
  attack();
  return 0;
}
