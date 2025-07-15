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
    
    def exp(self):

        return medida(math.exp(self._value), math.exp(self._value)*self._error)
    
    def ln(self):

        return medida(math.log(self._value), self._error/self._value)
    
    def __pow__(self, other):

        if isinstance(other, medida):

            a = ( other._value*(self._value.ln()) ).exp()
            b = other._error*(self._value.ln()) + other._value*self._error/self._value
            return medida(self._value**other._value, a*b)
        
        elif isinstance(other, float or int):

            return medida(self._value**other, other*self._value**(other-1)*self._error)
        
        else:

            raise TypeError("Should be medida, float or int")
        
    def log(self, other):
        
        "log de self na base other"

        if isinstance(other, medida):

            a = self._error/self._value*(math.log(other._value)) - other._error/other._value*(math.log(self._value))
            b = 2.0*math.log(other._value)
            return medida(self._value**other._value, a/b)
        
        elif isinstance(other, float or int):

            return self.ln()/math.log(other)
        
        else:

            raise TypeError("Should be medida, float or int")
