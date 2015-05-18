# sugarcube

sugarcube is a single-file python API to convert cooking ingredients to various measurements.
It is compatible with python 2.7 and python 3.4

## Installation
```bash
git clone https://github.com/vizigr0u/sugarcube.git
cd sugarcube
python setup.py install
```
## Usage

Converting grams of flour into cups:
```python
from sugarcube import Mass, Volume, Flour

ingredient = 250 * Mass.gram * Flour
print("%s = %s" % (ingredient, ingredient.to(Volume.cup)))
# prints: 250 g Flour = 1.4881 cup Flour
```

`help(sugarcube)` contains several usage examples

## Unit measures

Non-metric units are based on modern US standards :
- 1 cup = 240ml (FDA/*'US legal'* definition)
- 1 gallon = 231 * (2.54^3)
- 1 pound = 453.59237 grams
