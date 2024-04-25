import math

class medida:

    def __init__(self,value,error):

        self._value = value
        self._error = abs(error)

    def __add__(self, other):

        if isinstance(other, medida):
            return medida(self._value+other._value, self._error+other._error)
        elif isinstance(other, float or int):
            return medida(self._value+other, self._error)
        else:
            raise TypeError("Should be medida")
        
    def __radd__(self, other):

        if isinstance(other, medida):
            return medida(self._value+other._value, self._error+other._error)
        elif isinstance(other, float or int):
            return medida(self._value+other, self._error)
        else:
            raise TypeError("Should be medida")
        
    def __sub__(self, other):

        if isinstance(other, medida):
            return medida(self._value-other._value, self._error+other._error)
        elif isinstance(other, float or int):
            return medida(self._value-other, self._error)
        else:
            raise TypeError("Should be medida")
        
    def __rsub__(self, other):

        if isinstance(other, medida):
            return medida(other._value-self._value, self._error+other._error)
        elif isinstance(other, float or int):
            return medida(other-self._value, self._error)
        else:
            raise TypeError("Should be medida")
            
    
    def __mul__(self, other):

        if not isinstance(other, medida):
            if not isinstance(other, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value*other, self._error*other)
        else:
            return medida(self._value*other._value, self._value*other._error+self._error+other._value)
        
    def __rmul__(self, other):

        if not isinstance(other, medida):
            if not isinstance(other, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value*other, self._error*other)
        else:
            return medida(self._value*other._value, self._value*other._error+self._error+other._value)
        
    def __truediv__(self, other):

        if not isinstance(other, medida):
            if not isinstance(other, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value/other, self._error/other)
        else:
            a = self._value*other._error-self._error+other._value
            b = other._value*other._value
            return medida(self._value/other._value, a/b)
    
    def __rtruediv__(self, other):

        if not isinstance(other, medida):
            if not isinstance(other, float or int):
                raise TypeError("Should be medida")
            else:
                return medida(self._value/other, -other*self._error/self._value**2.0)
        else:
            a = self._error+other._value-self._value*other._error
            b = self._value*self._value
            return medida(other._value/self._value, a/b)
        
    def __repr__(self):

        return f"{self._value}±{self._error}"
    
    def __eq__(self, equal):

        if not isinstance(equal, medida):
            raise TypeError("Should be medida")
        else:
            return equal._value-(self._error+equal._error)<self._value<equal._value+(self._error+equal._error)
        
    def __neg__(self):

        return medida(-self._value, self._error)
    
    def exp(self):

        return medida(math.exp(self._value), math.exp(self._value)*self._error)
    
    def ln(self):

        return medida(math.log(self._value), self._error/self._value)
    
    def __pow__(self, other):

        if isinstance(other, medida):
            return medida(self._value**other, other*self._value**(other-1)*self._error)
        elif isinstance(other, float or int):
            return medida(self._value**other, other*self._value**(other-1)*self._error)
        else:
            raise TypeError("Should be a medida")
            

a = medida(20,1)
b = medida(19,1)
print(a==b)