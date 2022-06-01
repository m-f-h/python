""" Properties in Python.
  Written & (c) May 2022 by M.F.Hasler

A property is a kind of "computed attribute" of a Python object: 
It can be accessed as if it was a simple attribute, but it is actually computed on demand when accessed
(as well, and independently, for read and write access, i.e.: get and set).

This is implemented through Python's language "protocol" which consists in 
checking whether a given attibute has either of the methods __get__, __set__ or __delete__, 
in which case these are called to get, set or delete the (value of the) attribute.

The @property decorator can be used to create a property in a simpler way than using property( ... ).
"""
class temperature():
  """This class provides the attributes K, C and F for reading and setting
     the temperature in Kelvin, degrees Celcius or degrees Farenheit.
     Internally the temperature is stored in Kelvin (which shouldn't be negative)."""
  @property
  def C(self): return self.K - 273.15
  @C.setter
  def C(self, value): self.K = value + 273.15
  @property
  def F(self): return self.K*9/5 - 459.67
  @F.setter
  def F(self, value): self.K = (value + 459.67)*5/9

  def __repr__(self):
    "Return a string representation of this temperature instance."
    return type(self).__name__ + "(%g)" % self.K

  def __str__(self):
    "Return a string for nicely displaying the temperature."
    return "%g K = %g °C = %g °F" % (self.K, self.C, self.F)
  
  def __init__(self, value = 0, C = None, F = None):
    """Initialize the temperature with a string that may contain
    any of 'C', 'F' or 'K' and whitespace and '°' signs which are ignored,
    or with a floating point value that can be given as named argument 
    C = ... or F = ... to specify a scale different from Kelvin."""
    if isinstance(value, str):
      if 'C' in value:   C = value.strip(' °C')
      elif 'F' in value: F = value.strip(' °F')
      else:    value = float(value.strip(' °K'))
    if C is not None:   self.C = float(C)
    elif F is not None: self.F = float(F)
    else: self.K = value

if __name__ == '__main__':
  print("(Hit Ctrl-C to exit the loop.)")
  while True:
    T = temperature(input("Please enter a temperature: "))
    print(f"The temperature is {T}.")

# eof
