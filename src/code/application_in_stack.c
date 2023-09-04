char *Gets(char *dest)
{
  ...
  if (!hexformat) {
    while ((c = getc(infile)) != EOF && c != '\n') {
      *sp++ = c;
      save_char(c);
    }
  } 
  ...
}
unsigned long long getbuf(){
  char buf[36];
  unsigned long long val = (unsigned long long)Gets(buf);
  variable_length = alloca((val % 40) < 36 ? 36 : val % 40);
  ...
  return val % 40;
}
void test(){
  unsigned long long val;
  ...
    val = getbuf();
  ...
}
static void launch(int nitro, int offset){
  int localbuf[16];
  int stable_tweak = 0;
  int *space;
  ...
  test();
  ...
}
int main(int argc, char *argv[]){
  ...
  launch(nitro, offsets[i]+cookie_tweak);
  ...
}
