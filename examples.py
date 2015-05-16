#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sugarcube import Mass, Volume, Temperature, Flour, Butter

if __name__  == "__main__":
    def printConversion(base, unit):
        print("%s = %s" % (base, base.to(unit)))

    printConversion(1 * Volume.cup,             Volume.milliliter)
    printConversion(250 * Mass.gram * Flour,    Volume.cup)
    printConversion(1 * Volume.cup * Flour,     Mass.gram)
    printConversion(175 * Mass.gram * Flour,    Volume.tablespoon)
    printConversion(1 * Volume.stick * Butter,  Mass.gram)
    printConversion(125 * Mass.gram * Butter,  Volume.stick)
    printConversion(0 * Temperature.kelvin,     Temperature.celsius)
    printConversion(37.7 * Temperature.celsius, Temperature.fahrenheit)
    printConversion(Temperature.thermostat * 6, Temperature.celsius)
    printConversion(Temperature.thermostat * 6, Temperature.fahrenheit)
