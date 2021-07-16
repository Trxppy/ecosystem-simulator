
# Ecosystem Simulation

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Upcoming Features (v0.2.0 alpha)
[] Add organism behavior mechanism
-animal can try new behavior; If behavior results in more food, water, or offspring, then animal can "learn" behavior and try it again
-If behavior is learned, then it can be passed down (epigenetic mutation)
[] Add subspecies detection
-If species has more than 50 points of variation compared to its given species, create new subspecies of that species

## Future Update Ideas
[] Dead orgnanism utilization
-Dead organisms are not deleted and can be eaten by other organisms
-Dead plants can be used as shelter habitat for animals
[] Add pack behavior simulation
[] Add dynamic weather and seasons

## License
[MIT](https://choosealicense.com/licenses/mit/)
