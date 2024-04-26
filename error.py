import math

class measure:

    def __init__(self,value,error):
        """
        Initializes a new instance of the class.

        Args:
            value (Any): The value to be assigned to the instance variable _value.
            error (Any): The value to be assigned to the instance variable _error.

        Returns:
            None
        """
        self._value = value
        self._error = abs(error)


    def __add__(self, other):
        """
        Adds two `measure` objects together or adds a `measure` object and a `float` or `int`.

        Args:
            other (measure or float or int): The object to be added to `self`.

        Returns:
            measure: A new `measure` object with the sum of the values and the sum of the errors.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            return measure(self._value+other._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return measure(self._value+other, self._error)
        
        else:

            raise TypeError("Should be measure, float or int")
                            
        
    def __radd__(self, other):
        """
        Adds a `measure` object and a `float` or `int` together or adds two `measure` objects together.
        
        Args:
            other (measure or float or int): The object to be added to `self`.
        
        Returns:
            measure: A new `measure` object with the sum of the values and the sum of the errors.
        
        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            return measure(self._value+other._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return measure(self._value+other, self._error)
        
        else:

            raise TypeError("Should be measure, float or int")

        
    def __sub__(self, other):
        """
        Subtracts two `measure` objects or a `measure` object and a `float` or `int` together.

        Parameters:
            other (measure or float or int): The object to be subtracted from `self`.

        Returns:
            measure: A new `measure` object with the difference of the values and the sum of the errors.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            return measure(self._value-other._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return measure(self._value-other, self._error)
        
        else:

            raise TypeError("Should be measure, float or int")
        
        
    def __rsub__(self, other):
        """
        Subtracts two `measure` objects or a `measure` object and a `float` or `int` together.

        Parameters:
            other (measure or float or int): The object to be subtracted from `self`.

        Returns:
            measure: A new `measure` object with the difference of the values and the sum of the errors.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            return measure(other._value-self._value, self._error+other._error)
        
        elif isinstance(other, float or int):

            return measure(other-self._value, self._error)
        
        else:

            raise TypeError("Should be measure, float or int")
            
    
    def __mul__(self, other):
        """
        Multiplies the current `measure` object with another `measure` object, a `float` or `int`, or a combination thereof.

        Parameters:
            other (measure or float or int): The object to be multiplied with the current `measure` object.

        Returns:
            measure: A new `measure` object with the product of the values and the sum of the products of the errors by the conjugate values.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            return measure(self._value*other._value, self._value*other._error+self._error+other._value)
        
        elif isinstance(other, float or int):
                
            return measure(self._value*other, self._error*other)
        
        else:

            raise TypeError("Should be measure, float or int")
            
        
    def __rmul__(self, other):
        """
        Multiplies the current `measure` object with another `measure` object, a `float` or `int`, or a combination thereof.

        Parameters:
            other (measure or float or int): The object to be multiplied with the current `measure` object.

        Returns:
            measure: A new `measure` object with the product of the values and the sum of the products of the errors by the conjugate values.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):
            
            return measure(self._value*other._value, self._value*other._error+self._error+other._value)

        elif isinstance(other, float or int):
                
            return measure(self._value*other, self._error*other)

        else:
                
            raise TypeError("Should be measure, float or int")

        
    def __truediv__(self, other):
        """
        Divides the current `measure` object by another `measure` object, a `float` or `int`, or a combination thereof.

        Parameters:
            other (measure or float or int): The object to divide the current `measure` object by.

        Returns:
            measure: A new `measure` object with the quotient of the values and subract of the products of the errors by the conjugate values dividing by the square of the divider.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            dividend = self._value*other._error-self._error+other._value
            divider = other._value*other._value
            return measure(self._value/other._value, dividend/divider)

        elif isinstance(other, float or int):
                
                return measure(self._value/other, self._error/other)
        
        else:
                
                raise TypeError("Should be measure, float or int")
                
            
    def __rtruediv__(self, other):
        """
        Divides the current `measure` object by another `measure` object, a `float` or `int`, or a combination thereof.

        Parameters:
            other (measure or float or int): The object to divide the current `measure` object by.

        Returns:
            measure: A new `measure` object with the quotient of the values and subract of the products of the errors by the conjugate values dividing by the square of the divider.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):
        
            dividend = self._error+other._value-self._value*other._error
            divisor = self._value*self._value
            return measure(other._value/self._value, dividend/divisor)
        
        elif isinstance(other, float or int):
                
            return measure(self._value/other, -other*self._error/self._value**2.0)
        
        else:
               
            raise TypeError("Should be measure, float or int")

        
    def __repr__(self):
        """
        Returns a string representation of the `measure` object.

        Returns:
            str: A string in the format "{value}±{error}" where `{value}` is the value of the `measure` object and `{error}` is the error of the `measure` object.
        """
        return f"{self._value}±{self._error}"
    
    def __eq__(self, equal):
        """
        Check if the current `measure` object is equal to another `measure` object.

        Parameters:
            equal (measure): The `measure` object to compare with the current `measure` object.

        Returns:
            bool: True if the two `measure` objects are equal, False otherwise.

        Raises:
            TypeError: If `equal` is not a `measure` object.
        """
        if isinstance(equal, measure):

            return equal._value-(self._error+equal._error)<self._value<equal._value+(self._error+equal._error)

        else:

            raise TypeError("Should be measure")
            
        
    def __neg__(self):
        """
        Returns a new `measure` object that represents the negation of the current `measure` object.

        Parameters:
            self (measure): The current `measure` object.

        Returns:
            measure: A new `measure` object with the negated value and the same error as the current `measure` object.
        """
        return measure(-self._value, self._error)
    
    
    def __pow__(self, other):
        """
        Calculates the exponentiation of the current `measure` object with another `measure` object, a `float` or `int`, or a combination thereof.

        Parameters:
            other (measure or float or int): The object to be exponentiated with the current `measure` object.

        Returns:
            measure: A new `measure` object with the exponentiation of the values
            and a complex expression that relates to the derivates of powers, where the derivative of each value is replaced by the respective error.

        Raises:
            TypeError: If `other` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(other, measure):

            exponential = ( other._value*(math.log(self._value)) ).exp()
            multiplier = other._error*(math.log(self._value)) + other._value*self._error/self._value
            return measure(self._value**other._value, exponential*multiplier)
        
        elif isinstance(other, float or int):

            return measure(self._value**other, other*self._value**(other-1)*self._error)
        
        else:

            raise TypeError("Should be measure, float or int")

       
#out-of-class methods
def exp(measure):
    """
    Calculates the exponential of a `measure` object.

    Parameters:
        measure (measure): The `measure` object to calculate the exponential of.

    Returns:
        measure: A new `measure` object with the exponential of the value and exponential of the value multplied by de error.
    """
    return measure(math.exp(measure._value), math.exp(measure._value)*measure._error)

def ln(measure):
    """
    Calculates the natural logarithm of a `measure` object.

    Parameters:
        measure (measure): The `measure` object to calculate the natural logarithm of.

    Returns:
        measure: A new `measure` object with the natural logarithm of the value and the divison of the error by the value.
    """
    return measure(math.log(measure._value), measure._error/measure._value)

def log(logarithim, base):
        """
        Calculates the logarithm of a `measure` object with respect to a base `measure` object or a base `float` or `int`.

        Parameters:
            logarithim (measure or float or int): The `measure` object or `float` or `int` to calculate the logarithm of.
            base (measure or float or int): The `measure` object or `float` or `int` to use as the base for the logarithm calculation.

        Returns:
            measure: A new `measure` object with the logarithm of the value
            and a complex expression that relates to the derivates of division by logarithms, where the derivative of each value is replaced by the respective error.

        Raises:
            TypeError: If `logarithim` or `base` is not a `measure` object, `float`, or `int`.
        """
        if isinstance(logarithim, measure) and isinstance(base, measure):#if both are a measures

            dividendo = logarithim._error/logarithim._value*(math.log(base._value)) - base._error/base._value*(math.log(logarithim._value))
            divisor = 2.0*math.log(base._value)
            return measure(logarithim._value**base._value, dividendo/divisor)
        
        elif isinstance(base, float or int):#if only logarithm is a measure

            return ln(logarithim)/math.log(base)
        
        elif isinstance(logarithim, float or int):#if only base is a measure

            return math.log(logarithim)/ln(base)
        
        else:#if none are a measure

            raise TypeError("Should be measure, float or int")
        
def sqrt(measure):
    """
    Calculates the square root of a `measure` object.

    Args:
        measure (measure): The `measure` object to calculate the square root of.

    Returns:
        measure: A new `measure` object with the square root of the value and the error divided by twice the square root of the value.
    """
    return measure(math.sqrt(measure._value), measure._error/(2.0*math.sqrt(measure)))