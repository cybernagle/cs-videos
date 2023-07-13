#include <stdio.h>
#include <string.h>

void vulnerableFunction() {
  char buffer[5];
  printf("请输入内容：");
  gets(buffer);
  printf("你输入的是：%s\n", buffer);
}

int main() {
  vulnerableFunction();
  return 0;
}
