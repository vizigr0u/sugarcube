#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 2 compatibility
from __future__ import division
from builtins import int, str

class Element(object):
    """ Food or other element with certain properties
    """
    def __init__(self, name, **properties):
        """properties are set as attributes for easier access

        >>> Element('flour', color='#ffffff', density=0.7).density
        0.7
        """
        self.name = name
        for prop in properties:
            setattr(self, prop, properties[prop])
    def __repr__(self):
        return self.name

class Ingredient(object):
    """ An amount of a certain element

    >>> Ingredient(3 * Volume.teaspoon, Element('sugar'))
    3 tsp. sugar

    shorter syntax using multiplication:
    >>> 30 * Volume.milliliter * Element('cyanide')
    30 ml cyanide
    """
    def __init__(self, amount, element):
        self.amount = amount
        self.element = element
    def to(self, unit):
        """ Convert to a different unit, or measure depending on the properties of its element

        >>> (2 * Volume.cup * Element('water')).to(Volume.milliliter)
        480 ml water
        >>> (1 * Volume.cup * Flour).to(Mass.gram).amount
        168 g
        """
        if isinstance(unit, Measure):
            unit = unit.refUnit
        if unit.measure == self.amount.unit.measure:
            return Ingredient(self.amount.to(unit), self.element)
        return self._transform(unit)
    def __repr__(self):
        return "%s %s" % (self.amount, self.element)
    def _transform(self, unit):
        newAmount =  self.amount.unit.measure.transformTo(unit.measure)(self.amount, self.element)
        return Ingredient(newAmount.to(unit), self.element)

class Amount(object):
    """ Amount/quantity of a Unit

    >>> Amount(5, Mass.decigram)
    5 dg
    >>> 3 * Volume.hectoliter
    3 hl
    """
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
    def to(self, unit, properties=None):
        """ convert to another unit of the same measure

        >>> (2 * Volume.liter).to(Volume.centiliter)
        200 cl
        >>> (0 * Temperature.kelvin).to(Temperature.celsius)
        -273.15 °C
        """
        if not isinstance(unit, Unit):
            raise TypeError('Expected Unit type but unit is type ' + type(unit).__name__)
        if self.unit == unit:
            return self
        if unit.measure != self.unit.measure:
            raise TypeError("Can't implicitely convert from " + self.unit.measure.name + " to " + unit.measure.name)
        refAmount = self
        if self.unit != self.unit.measure.refUnit:
            refAmount = self.toRefUnit()
        if unit == refAmount.unit:
            return refAmount
        newAmount = Amount(unit.converter.fromRef(refAmount.value), unit)
        return newAmount
    def toRefUnit(self):
        """ convert to the reference unit of a unit measure
        """
        return self.unit.converter.toRef(self.value) * self.unit.measure.refUnit
    
    def __mul__(self, other):
        if isinstance(other, Element):
            return Ingredient(self, other)
        if isinstance(other, (int, float)):
            return Amount(self.value * other, self.unit)
        raise TypeError("Unable to multiply " + self.unit.measure + " and " + type(other).__name__)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Amount(self.value / other, self.unit)
        raise TypeError("Unable to divide " + self.unit.measure + " by " + type(other).__name__)
    def __repr__(self):
        valuestr = "%g" % self.value
        return "%s %s" % ((self.unit.abrev, valuestr) if self.unit.preFix else (valuestr, self.unit.abrev))

class Measure(object):
    def __init__(self, name, refUnit):
        self.name = name
        self.units = {}
        self.addUnit(refUnit)
        self.refUnit = refUnit
        self.transform_functions = {}
    def addUnit(self, unit):
            if not isinstance(unit, Unit):
                raise TypeError('Expected a type Unit, but got type ' + type(unit).__name__)
            if unit.name in self.units:
                raise ValueError("%s already contains a unit named %s" % (self.name, unit.name))
            unit.measure = self
            self.units[unit.name] = unit
            setattr(self, unit.name, unit)
    def addUnits(self, units):
        for unit in units:
            self.addUnit(unit)
    def transformTo(self, measure):
        if measure not in self.transform_functions:
            raise ValueError("No transformation known bewteen " + self.name + " and " + measure.name)
        return self.transform_functions[measure]
    def addTransform(self, toMeasure, function):
        if toMeasure not in self.transform_functions:
            self.transform_functions[toMeasure] = function

class Converter(object):
    def __init__(self, toRefFunction, fromRefFunction):
        self.toRef = toRefFunction
        self.fromRef = fromRefFunction
    @property
    def reverse(self):
        return Converter(self.fromRef, self.toRef)
    @classmethod
    def Linear(cls, factor, constant=0):
        return cls(lambda n: n * factor + constant, lambda n: (n - constant) / factor)
    @classmethod
    def Constant(cls, constant):
        return cls.Linear(1, constant)
    def __repr__(self):
        return "1 u. ~= %g ref." % self.toRef(1)
Converter.Neutral = Converter.Linear(1)

class Unit(object):
    """Unit of a measure, i.e. gram (mass), liter (volume) etc.
    """
    def __init__(self, name='Unknown unit', abrev='?unit', preFix=False, converter=Converter.Neutral):
        self.name = name
        self.abrev = abrev
        self.preFix = preFix
        self.converter = converter
        self.measure = None # set by Measures when they add a unit
    def __mul__(self, other):
        return self.__rmul__(other)
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Amount(other, self)
    def __repr__(self):
        return self.name

def SIUnitsFromUnit(unit):
    """list the most common SI units based of a reference unit

    SIUnitsFromUnit(Unit('liter', 'l')) -> [ Unit('milliliter', 'ml' (0.001 liter)), (...) ]
    prefixes: milli, centi, deci, deca, hecto, kilo
    """
    if not isinstance(unit, Unit):
        raise TypeError('Expected type Unit, but unit is type ' + type(unit).__name__)
    return map(
        lambda t:
            Unit(t[0] + unit.name,
                t[1] + unit.abrev,
                converter=Converter.Linear(t[2]),
                preFix=unit.preFix),
        [
            ('milli',   'm',    0.001),
            ('centi',   'c',    0.01),
            ('deci',    'd',    0.1),
            ('deca',    'da',   10),
            ('hecto',   'h',    100),
            ('kilo',    'k',    1000)
        ]
    )

# Common cooking measures

Mass = Measure('Mass', Unit('gram', 'g'))
Mass.addUnits(SIUnitsFromUnit(Mass.gram))

Volume = Measure('Volume', Unit('liter', 'l'))
Volume.addUnits(SIUnitsFromUnit(Volume.liter))

Temperature = Measure('Temperature', Unit('celsius', '°C'))
Temperature.addUnits([
    Unit('kelvin',      '°K',           converter=Converter.Constant(-273.15)),
    Unit('fahrenheit',  '°F',           converter=Converter.Linear(1.8, 32).reverse),
    Unit('thermostat',  'thermostat',   converter=Converter.Linear(30), preFix=True)
])

# other measures

Length = Measure('Length', Unit('meter', 'm'))
Length.addUnits(SIUnitsFromUnit(Length.meter))

Time = Measure('Time', Unit('second', 's'))
Time.addUnits([
    Unit('minute', 'min', converter=Converter.Linear(60)),
    Unit('hour', 'h', converter=Converter.Linear(3600))
])

# measure conversion

milliliter = Volume.milliliter
gram = Mass.gram

Volume.addTransform(Mass, lambda volume, element: (element.density * volume.to(milliliter)).value * gram)
Mass.addTransform(Volume, lambda mass, element: ((mass.to(gram)).value / element.density) * milliliter)

# US cooking units

Volume.addUnits([
    Unit('pinch',           'pinch',    converter=Converter.Linear(0.000625)),
    Unit('teaspoon',        'tsp.',     converter=Converter.Linear(0.005)),
    Unit('tablespoon',      'tbsp.',    converter=Converter.Linear(0.015)),
    Unit('FluidOunce',      'oz',       converter=Converter.Linear(0.03)),
    Unit('stick',           'stick',    converter=Converter.Linear(0.126)),
    Unit('cup',             'cup',      converter=Converter.Linear(0.240)),
    Unit('pint',            'pt.',      converter=Converter.Linear(0.47318)),
    Unit('quart',           'qt',       converter=Converter.Linear(0.94635)),
    Unit('gallon',          'gal.',     converter=Converter.Linear(3.78541))
])

Mass.addUnits([
    Unit(name='Ounce',  abrev='oz', converter=Converter.Linear(28.349523125)),
    Unit(name='Pound',  abrev='lb', converter=Converter.Linear(453.59237))
])

# Common Ingredients

Flour  = Element('Flour',  density=0.7)
Sugar  = Element('Sugar',  density=1.2)
Salt   = Element('Salt',   density=1.2)
Butter = Element('Butter', density=0.9)

# run the module to make it test itself
if __name__ == "__main__":
    import doctest
    doctest.testmod()
