# [hancock.lighting](http://hancock.lighting)

Steady blue, clear view. Flashing blue, clouds due. Steady red, rain ahead. Flashing red, snow instead.

## Table of Contents

1. [Motivation](#motivation)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Motivation

It's almost a rite of passage for designers to build a flashy weather app of questionable utility. By looking down at your phone, this project replicates the experience of looking up in a [limited geographic area](https://goo.gl/maps/y3D9mBrG1YE2) to view the lights on the tip of a tower, in order to decipher a poem that gives you a general description of a city's current weather conditions.

When I was working at the Boston Globe, I tried my hardest to resurrect the [old Boston.com weather beacon feature](http://archive.boston.com/sports/baseball/redsox/articles/2004/10/29/hancockbeacon/). It captured a delightful little detail of the city's rich history, but unfortunately, the project was never made a priority.

This site makes good on that attempt, and is a little love letter to the city that's been my home for the past decade. It's also a chance to put a lot of CSS techniques into practice, including some new approaches and technologies I wanted a chance to try out. Fortunately, I was also able to browbeat [my friend Dan](https://github.com/danielsmc) into helping with the icky Python part.

## Installation

Provide code examples and explanations of how to get the project.

### Cheating

If you're impatient and would like to preview the different  states without waiting for the time and weather to change, you can append the following to the end of the URL: `/?beacon=raining&time=nighttime`

Where the `beacon` values are:

- `clear`
- `cloudy`
- `raining`
- `snowing`
- `sox-rainout`
- `sox-champs`

And the `time` values are:

- `daytime`
- `nighttime`

Note: `sox-champs` only works with `nighttime`.

## Contributing

Contributions are welcome! Please follow the [contributing guidelines](https://github.com/ericwbailey/hancock.lighting/CONTRIBUTING.md) for submitting Issues and Pull and Feature Requests.

If you'd just like to show a little love, contacting the [authors](https://github.com/ericwbailey/hancock.lighting/AUTHORS) on Twitter is probably your best bet:

- [@ericwbailey](https://twitter.com/ericwbailey)
- [@mclaughlin](http://twitter.com/mclaughlin)

## License

[MIT License](https://raw.githubusercontent.com/ericwbailey/hancock.lighting/master/LICENSE)
