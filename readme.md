
# Ecosystem Simulation

This is a lightweight console application that simulates natural ecosystems and allows the user to observe and log the effects of long-term processes like evolution, habitat loss, and climate change.

## Installation
Installation documentation coming soon!

## Usage
Usage documentation coming soon!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Upcoming Features (v0.3.0)
- [ ] Dead orgnanism utilization
- Dead organisms are not deleted and can be eaten by other organisms
- Dead plants can be used as shelter habitat for animals
- [ ] Allow user to reset and re-enter organisms in the environment
- [ ] Add rename function in application console
- Renames all organisms with given species name and updates parent species information
- [X] Convert plant and animal output to __dict__ objects

## Future Update Ideas
- [ ] Add pack behavior simulation
- [ ] Add dynamic weather and seasons
- Split daily simulation into four sections: dawn, day, dusk, night
- [ ] Add organism behavior mechanism
- Animal can try new behavior; If behavior results in more food, water, or offspring, then animal can "learn" behavior and try it again
- If behavior is learned, then it can be passed down (epigenetic mutation)
- [ ] Add save feature to simulation
- Any new species created during simulation are stored in output
- Also tracks extinct species
- [ ] Add transfer saved organisms feature to environment
- Transfers new organisms from output to the user list of organism
- [ ] Calculate species fitness based on what percent did not die due to natural causes
- [ ] Add sleep variable for animals and preferred shelter location
- If animal sleep is below default, then searching distance for food/water/mates is diminished and all movement is reduced
- Sleep can be replenished by finding a suitable shelther location
- If no shelter location found and sleep is insufficient for movement, sleep wherever organism is

## License
[MIT](https://choosealicense.com/licenses/mit/)
