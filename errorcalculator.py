import math

class medida:

    def __init__(self,value,error):

        self._value = value
        self._error = abs(error)

    def __add__(self, plus):

        if not isinstance(plus, medida):
            if not isinstance(plus, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value+plus, self._error)
        else:
            return medida(self._value+plus._value, self._error+plus._error)
        
    def __radd__(self, plus):

        if not isinstance(plus, medida):
            if not isinstance(plus, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value+plus, self._error)
        else:
            return medida(self._value+plus._value, self._error+plus._error)
        
    def __sub__(self, subtract):

        if not isinstance(subtract, medida):
            if not isinstance(subtract, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value-subtract, self._error)
        else:
            return medida(self._value-subtract._value, self._error+subtract._error)
        
    def __rsub__(self, subtract):

        if not isinstance(subtract, medida):
            if not isinstance(subtract, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value-subtract, self._error)
        else:
            return medida(subtract._value-self._value, self._error+subtract._error)
    
    def __mul__(self, mult):

        if not isinstance(mult, medida):
            if not isinstance(mult, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value*mult, self._error*mult)
        else:
            return medida(self._value*mult._value, self._value*mult._error+self._error+mult._value)
        
    def __rmul__(self, mult):

        if not isinstance(mult, medida):
            if not isinstance(mult, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value*mult, self._error*mult)
        else:
            return medida(self._value*mult._value, self._value*mult._error+self._error+mult._value)
        
    def __truediv__(self, divi):

        if not isinstance(divi, medida):
            if not isinstance(divi, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value/divi, self._error/divi)
        else:
            a = self._value*divi._error-self._error+divi._value
            b = divi._value*divi._value
            return medida(self._value/divi._value, a/b)
    
    def __rtruediv__(self, divi):

        if not isinstance(divi, medida):
            if not isinstance(divi, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value/divi, -divi*self._error/self._value**2.0)
        else:
            a = self._error+divi._value-self._value*divi._error
            b = self._value*self._value
            return medida(divi._value/self._value, a/b)
        
    def __repr__(self):

        return f"{self._value}±{self._error}"
    
    def __eq__(self, equal):

        if not isinstance(equal, medida):
            raise TypeError("Should be medida")
        else:
            return equal._value-(self._error+equal._error)<self._value<equal._value+(self._error+equal._error)

    def __pow__(self, num):

        if not isinstance(num, float or int):
            raise TypeError("Should be a number")
        else:
            return medida(self._value**num, num*self._value**(num-1)*self._error)
        
    def __neg__(self):

        return medida(-self._value, self._error)
    
    def exp(self):

        return medida(math.exp(self._value), math.exp(self._value)*self._error)
    
    def ln(self):

        return medida(math.log(self._value), self._error/self._value)

a = medida(20,1)
b = medida(19,1)
print((a+b)/(a-b)*b**2.0)