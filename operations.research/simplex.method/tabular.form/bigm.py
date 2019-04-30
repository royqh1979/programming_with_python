from fractions import Fraction

class FractionWithM:
    """
    class for
    """
    def __init__(self,value, M=0):
        super().__setattr__('M',Fraction(M))
        super().__setattr__('fraction',Fraction(value))

    def __add__(self,y):
        if isinstance(y,FractionWithM):
            return FractionWithM(self.fraction+y.fraction,self.M+y.M)
        else:
            return FractionWithM(self.fraction+y,self.M)

    def __sub__(self,y):
        if isinstance(y,FractionWithM):
            return FractionWithM(self.fraction-y.fraction,self.M-y.M)
        else:
            return FractionWithM(self.fraction-y,self.M)

    def __mul__(self,y):
        if y.M!=0 and self.M!=0:
            return NotImplemented("Cant multiply 2 FractionWithM objects!")
        if y.M!=0:
            return FractionWithM(self.fraction*y.fraction,self.fracation * y.M)
        else:
            return FractionWithM(self.fraction*y.fraction,self.M * y.fraction)

    def __truediv__(self, y):
        if y.M!=0:
            return NotImplemented("Cant divide 2 FractionWithM objects!")
        return FractionWithM(self.fraction/y.fraction,self.M/y.fraction)


    def __gt__(self, y):
        if not isinstance(y,FractionWithM):
            if self.M>0:
                return True
            elif self.M<0:
                return False
            else:
                return self.fraction > y
        if self.M>y.M:
            return True
        elif self.M < y.M:
            return False
        return self.fraction > y.fraction

    def __eq__(self,y):
        if not isinstance(y,FractionWithM):
            if self.M!=0:
                return False
            else:
                return self.fraction == y

        return self.M == y.M and self.fraction == y.fraction

    def __lt__(self, y):
        if not isinstance(y,FractionWithM):
            if self.M<0:
                return True
            elif self.M>0:
                return False
            else:
                return self.fraction < y
        if self.M<y.M:
            return True
        elif self.M > y.M:
            return False
        return self.fraction < y.fraction


    def __ge__(self,y):
        if not isinstance(y,FractionWithM):
            if self.M>0:
                return True
            elif self.M<0:
                return False
            else:
                return self.fraction >= y
        if self.M>y.M:
            return True
        elif self.M < y.M:
            return False
        return self.fraction >= y.fraction

    def __le__(self, y):
        if not isinstance(y,FractionWithM):
            if self.M<0:
                return True
            elif self.M>0:
                return False
            else:
                return self.fraction <= y
        if self.M<y.M:
            return True
        elif self.M > y.M:
            return False
        return self.fraction <= y.fraction

    def __setattr__(self, key, value):
        raise AttributeError(f"Can't set a FractionWithM object's {key} attribute!")

    def __str__(self):
        str = ''
        if self.M != 0:
            if self.M.denominator == 1:
                str += f'{self.M.numerator}*M'
            else:
                str += f'{self.M.numerator}/{self.M.denominator}*M'
            if self.fraction > 0:
                str += '+'
        if self.fraction != 0:
            if self.fraction.denominator == 1:
                str += f'{self.fraction.numerator}'
            else:
                str += f'{self.fraction.numerator}/{self.fraction.denominator}'
        else:
            if self.M == 0:
                str = '0'
        return str
