# [hancock.lighting](http://hancock.lighting)

Steady blue, clear view. Flashing blue, clouds due. Steady red, rain ahead. Flashing red, snow instead.

## Table of Contents

1. [Motivation](#motivation)
- [Technology](#technology)
- [Contributing](#contributing)
- [License](#license)

## Motivation

It's almost a rite of passage for designers to make a flashy weather app of questionable utility. By looking down at your screen, this project replicates the experience of looking up in a [limited geographic area](https://goo.gl/maps/y3D9mBrG1YE2) to view the manually-controlled lights on the tip of a tower. This gives you the information you need to decipher a poem that gives you a high-level description of your current area's current weather conditions.

When I was working at the Boston Globe, I tried my hardest to resurrect the [old Boston.com weather beacon feature](http://archive.boston.com/sports/baseball/redsox/articles/2004/10/29/hancockbeacon/). It captured a [delightful little detail](http://www.bizjournals.com/boston/blog/bottom_line/2012/11/berkley-weather-beacon-survives.html) of the city's rich history, but unfortunately, the project was never made a priority.

This site makes good on that attempt, and is a little love letter to the city that's been my home for the past decade. It's also a chance to put a lot of CSS techniques into practice, including some new approaches and technologies I wanted a chance to try out. Fortunately, I was also able to browbeat [my friend Dan](https://github.com/danielsmc) into helping with the icky Python part.

## Technology

### Browser Support

This site makes liberal use of evergreen browser features such as [flexbox](http://caniuse.com/#feat=flexbox), [SVG](http://caniuse.com/#feat=svg), [viewport units](http://caniuse.com/#feat=viewport-units), [CSS blend modes](http://caniuse.com/#feat=css-backgroundblendmode), etc. As such, it makes few concessions for IE support.

### Installation

Assuming you have [Node](https://nodejs.org/en/) and [Node Package Manager](https://www.npmjs.com/) installed, you can install a local copy by:

1. Cloning from `https://github.com/ericwbailey/hancock.lighting.git` 
- Running `npm install`
- Then running `gulp`

This should pull down this repo's code, install all required Node modules, then build the site and open it in your browser via [Browsersync](https://www.browsersync.io/).

### Cheating

If you're impatient and would like to preview the different  states without waiting for the time and weather to change, you can append the following to the end of the URL: `/?beacon=cloudy&time=nighttime`

Where the `beacon` values are:

- `clear`
- `cloudy`
- `raining`
- `snowing`
- `sox-rainout`
- `sox-champs` (only works with `nighttime`)

And the `time` values are:

- `daytime`
- `nighttime`

Note: Changing the site's time and weather states won't affect the outside world.

## Contributing

Please follow the [contributing guidelines](https://github.com/ericwbailey/hancock.lighting/CONTRIBUTING.md) for submitting Issues and Pull and Feature Requests.

If you'd just like to show a little love, contacting the [authors](https://github.com/ericwbailey/hancock.lighting/AUTHORS) on Twitter is probably your best bet:

- [@ericwbailey](https://twitter.com/ericwbailey)
- [@mclaughlin](http://twitter.com/mclaughlin)

## License

[MIT License](https://raw.githubusercontent.com/ericwbailey/hancock.lighting/master/LICENSE)
