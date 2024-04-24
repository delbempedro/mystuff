class medida:

    def __init__(self,value,error):
        self._value = value
        self._error = error

    def __add__(self, plus):
        if not isinstance(medida, plus):
            raise TypeError("Should be medida")
        else:
            return medida(self._value+plus.value,self._error+plus.error)
        
    def __radd__(self, plus):
        if not isinstance(medida, plus):
            raise TypeError("Should be medida")
        else:
            return medida(self._value+plus.value,self._error+plus.error)
        
    def __sub__(self, subtract):
        if not isinstance(medida, subtract):
            raise TypeError("Should be medida")
        else:
            return medida(self._value-subtract.value,self._error+subtract.error)
        
    def __rsub__(self, subtract):
        if not isinstance(medida, subtract):
            raise TypeError("Should be medida")
        else:
            return medida(subtract.value-self._value,self._error+subtract.error)
    
    def __mul__(self,mult):
        if not isinstance(medida, mult):
            raise TypeError("Should be medida")
        else:
            return medida(self._value*mult.value,self._value*mult.error+self._error+mult.value)
        
    def __rmul__(self,mult):
        if not isinstance(medida, mult):
            raise TypeError("Should be medida")
        else:
            return medida(self._value*mult.value,self._value*mult.error+self._error+mult.value)
        
    def __div__(self,divi):
        if not isinstance(medida, divi):
            raise TypeError("Should be medida")
        else:
            a = self._value*divi.error-self._error+divi.value
            b = divi.value*divi.value
            return medida(self._value/divi.value,a/b)
    
    def __rdiv__(self,divi):
        if not isinstance(medida, divi):
            raise TypeError("Should be medida")
        else:
            a = self._error+divi.value-self._value*divi.error
            b = self._value*self._value
            return medida(self._value/divi.value,a/b)

    