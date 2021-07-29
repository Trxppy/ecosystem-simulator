
# Ecosystem Simulation

This is a lightweight console application that simulates natural ecosystems and allows the user to observe and log the effects of long-term processes like evolution, habitat loss, and climate change.

## Installation
Installation documentation coming soon!

## Usage
Usage documentation coming soon!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Upcoming Features (v0.4.0)
- [ ] Calculate species fitness based on what percent did not die due to natural causes
- [ ] Add sleep variable for animals and preferred shelter location
- If animal sleep is below default, then searching distance for food/water/mates is diminished and all movement is reduced
- Sleep can be replenished by finding a suitable shelther location
- If no shelter location found and sleep is insufficient for movement, sleep wherever organism is
- Dead plants with sufficient size can be used as shelter habitat for animals


## Future Update Ideas
- [ ] Add dynamic weather and seasons (coming in v0.6.0)
- Split daily simulation into four periods: dawn, day, dusk, night
- Each time will have different temperature variation based on the user-defined baseline for the environment
- Add blood temperature variable to animal objects; If rainfall occurs and the temperature is below freezing, accumulate snowfall on terrain blocks
- Add snow accumulation variable to block 
- Snowfall will reduce animal movement by 50%
- Freezing temperature reduces animal movement by 40% min_food by 45% (If cold-blooded, reduce movement by 80% and food by 90%)
- Add is_frozen variable to water blocks; After eight consecutive periods of below freezing, set all blocks to frozen
- Block can unfreeze after eight consecutive periods of above freezing temmps
- For water organisms, frozen blocks reduce movement by 50%, min_food by 70% (90% and 95% for cold-blooded organisms)
- User can define up to four seasons, along with their own temperature variation and rainfall frequency
- [ ] Add organism behavior mechanism (coming in v0.5.0)
- Animal can try new behavior; If behavior results in more food, water, or offspring, then animal can "learn" behavior and try it again
- If behavior is learned, then it can be passed down (epigenetic mutation)
- [ ] Add pack behavior simulation

## License
[MIT](https://choosealicense.com/licenses/mit/)
