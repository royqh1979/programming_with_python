from scanf import scanf


# scanf supports the following formats:
#   %c        One character
#   %5c       5 characters
#   %d, %i    int value
#   %7d, %7i  int value with length 7
#   %f        float value
#   %o        octal value
#   %X, %x    hex value
#   %s        string terminated by whitespace


a,b=scanf("%d %d","35 47")
print(a,b)

a,b,c = scanf("%d,%d,%d","35,45,68")
print(a,b,c)

