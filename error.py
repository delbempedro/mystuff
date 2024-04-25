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

            raise TypeError("Should be medida, float or int")
                            
        
    def __radd__(self, other):

        if isinstance(other, medida):

            return medida(self._value+other._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return medida(self._value+other, self._error)
        
        else:

            raise TypeError("Should be medida, float or int")

        
    def __sub__(self, other):

        if isinstance(other, medida):

            return medida(self._value-other._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return medida(self._value-other, self._error)
        
        else:

            raise TypeError("Should be medida, float or int")
        
        
    def __rsub__(self, other):

        if isinstance(other, medida):

            return medida(other._value-self._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return medida(other-self._value, self._error)
        
        else:

            raise TypeError("Should be medida, float or int")
            
    
    def __mul__(self, other):

        if isinstance(other, medida):

            return medida(self._value*other._value, self._value*other._error+self._error+other._value)
        
        elif isinstance(other, float or int):
                
            return medida(self._value*other, self._error*other)
        
        else:

            raise TypeError("Should be medida, float or int")
            
        
    def __rmul__(self, other):

        if isinstance(other, medida):
            
            return medida(self._value*other._value, self._value*other._error+self._error+other._value)

        elif isinstance(other, float or int):
                
            return medida(self._value*other, self._error*other)

        else:
                
            raise TypeError("Should be medida, float or int")

        
    def __truediv__(self, other):

        if isinstance(other, medida):

            a = self._value*other._error-self._error+other._value
            b = other._value*other._value
            return medida(self._value/other._value, a/b)

        elif isinstance(other, float or int):
                
                return medida(self._value/other, self._error/other)
        
        else:
                
                raise TypeError("Should be medida, float or int")
                
            
    def __rtruediv__(self, other):

        if isinstance(other, medida):
        
            a = self._error+other._value-self._value*other._error
            b = self._value*self._value
            return medida(other._value/self._value, a/b)
        
        elif isinstance(other, float or int):
                
            return medida(self._value/other, -other*self._error/self._value**2.0)
        
        else:
               
            raise TypeError("Should be medida, float or int")

        
    def __repr__(self):

        return f"{self._value}±{self._error}"
    
    def __eq__(self, equal):

        if isinstance(equal, medida):

            return equal._value-(self._error+equal._error)<self._value<equal._value+(self._error+equal._error)

        else:

            raise TypeError("Should be medida")
            
        
    def __neg__(self):

        return medida(-self._value, self._error)
    
    
    def __pow__(self, other):

        if isinstance(other, medida):

            a = ( other._value*(math.log(self._value)) ).exp()
            b = other._error*(math.log(self._value)) + other._value*self._error/self._value
            return medida(self._value**other._value, a*b)
        
        elif isinstance(other, float or int):

            return medida(self._value**other, other*self._value**(other-1)*self._error)
        
        else:

            raise TypeError("Should be medida, float or int")

       
#out-of-class methods
def exp(a):

    return medida(math.exp(a._value), math.exp(a._value)*a._error)

def ln(a):

    return medida(math.log(a._value), a._error/a._value)

def log(a, b):
        
        "log de a na base b"

        if isinstance(a, medida) and isinstance(b, medida):#se ambos sao medidas

            dividendo = a._error/a._value*(math.log(b._value)) - b._error/b._value*(math.log(a._value))
            divisor = 2.0*math.log(b._value)
            return medida(a._value**b._value, dividendo/divisor)
        
        elif isinstance(b, float or int):#se apenas a e' medida

            return ln(a)/math.log(b)
        
        elif isinstance(a, float or int):#se apenas b e' medida

            return math.log(a)/ln(b)
        
        else:

            raise TypeError("Should be medida, float or int")