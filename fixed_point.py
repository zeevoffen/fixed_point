class FixedPoint:

    def check_value_range(self,value):
        if value > self.max_value or value < self.min_value:
            raise ValueError(f"Value {value} cannot be represented with precision {self.precision} max_val:{self.max_value} min_val:{self.min_value}")

    def recompute_value_according_to_precision(self,value):
        self.check_value_range(value)
        int_bits, frac_bits = self.precision
        scale = 2 ** frac_bits
        scaled_value = int(value * scale)
        rounded_value = round(scaled_value)
        return rounded_value / scale

    def __init__(self, value, precision,signed=True):
        sub1 = 1 if signed else 0
        self.max_value = (2**(precision[0]+precision[1] - sub1)-1) / 2**(precision[1])
        self.min_value = 0 if not signed else -self.max_value
        self.signed = signed
        self.precision = precision
        self.value = self.recompute_value_according_to_precision(value)
    
    def __str__(self):
        sign = "-" if self.value < 0 else ""
        signed = "SIGNED" if self.signed else "UNSIGNED"
        int_part = abs(int(self.value))
        frac_part = abs(self.value) - int_part
        int_str = bin(int_part)[2:].zfill(self.precision[0])
        frac_str = ""
        for _ in range(self.precision[1]):
            frac_part *= 2
            bit = int(frac_part)
            frac_str += str(bit)
            frac_part -= bit
        return f"signed {sign}{int_str}.{frac_str} value:{self.value} max_val:{self.max_value} min_val:{self.min_value}"

    def __repr__(self):
        return f'FixedPoint({self.value}, {self.precision}) {self.__str__()}'

    
    def __add__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError('unsupported operand type(s) for +: \'FixedPoint\' and \'' + type(other).__name__ + '\'')
        if self.precision != other.precision:
            raise ValueError('operands have different precision')
        return FixedPoint(self.value + other.value, self.precision)
    
    def __sub__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError('unsupported operand type(s) for -: \'FixedPoint\' and \'' + type(other).__name__ + '\'')
        if self.precision != other.precision:
            raise ValueError('operands have different precision')
        return FixedPoint(self.value - other.value, self.precision)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return FixedPoint(self.value * other, self.precision)
        elif isinstance(other, FixedPoint):
            return FixedPoint((self.value*other.value), (self.precision[0] + other.precision[0],self.precision[1] + other.precision[1]))
        else:
            raise TypeError('unsupported operand type(s) for *: \'FixedPoint\' and \'' + type(other).__name__ + '\'')
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return FixedPoint(self.value / other, self.precision)
        if isinstance(other, FixedPoint):
            return FixedPoint((self.value/other.value), (other.precision[0],self.precision[1] - other.precision[1]))
        else: 
            raise TypeError('unsupported operand type(s) for /: \'FixedPoint\' and \'' + type(other).__name__ + '\'')
    def __rmul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError('unsupported operand type(s) for *: \'' + type(other).__name__ + '\' and \'FixedPoint\'')
        return FixedPoint(self.value * other, self.precision)
    
    def __eq__(self, other):
        if not isinstance(other, FixedPoint):
            return False
        return self.value == other.value and self.precision == other.precision
    
    def __ne__(self, other):
        return not self.__eq__(other)
