from error import *

a = measure(3.5, 0.1)
b = measure(2, 0.5)
print(a/b-a+b*exp(b)*ln(a)*a**b+sqrt(a)**log(a,b))