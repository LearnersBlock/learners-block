# Learner’s Block

Learner’s Block is still under development and not yet ready for stable production. Check back here for updates on progress or follow our [pre-deployment project list](https://github.com/LearnersBlock/learners-block/projects/3). 

## Description

An open-source project that lets individuals and organisations provide their educational resources, websites and apps to users offline.
https://learnersblock.org

## Documentation

All of our documentation is stored and maintained [here](https://docs.learnersblock.org). 

## Technical Details

This project is made possible by Balena OS, an operating system for Internet of Things devices. On top of the OS goes the code provided in this repository. For more details on the technical structure of the operating system and this code, please see our [technical details page](https://docs.learnersblock.org/advanced-features/technical-details).

## Installation

### Development

A development environment is provided in this repo. Docker-compose.yml on your local system will compile and launch an instance locally. 

All development changes however, will require testing through the Balena OS and relevant hardware before being deployed to the fleet of devices. Follow the [Balena local deployment](https://www.balena.io/docs/learn/develop/local-mode/) documentation to do so.

### Production 

#### Pre-built

Learner’s Block software is provided as an entire package, including an operating system with pre-defined keys that allow for automatic updates. To benefit from these, [download the image files](https://downloads.learnersblock.org).

#### Deploy locally

You may deploy the code to a device locally. We recommend the Balena documentation listed below to do so. This approach however will not benefit from automatic update, and we cannot offer support for its use. 

[Balena Local Deployments](https://www.balena.io/docs/learn/develop/local-mode/)

#### Deploy to your own server

As open-source software, you can deploy to your own [Balena](https://www.balena.io) instance and serve your own automatic updates. We cannot however support installation and use via this method. 

[Balena Server Based Deployments](https://www.balena.io/docs/learn/deploy/deployment/)

## Feature requests

We thrive to ensure the features developed are those most in line with the community needs. That is why all feature requests are made through our [voting platform](https://vote.learnersblock.org), where users can add ideas and vote for those they feel most important. Please utilise this voting platform rather than adding feature requests to this repository. 

## Contributing

### Development/pull requests
We welcome contributions, they are what keep the Block alive! For pull requests we suggest discussing the changes through a ticket first. This is for your own sake in case there are already changes ongoing that will affect your contribution. If you are looking to contribute without a specific feature or goal in mind, please check the list of [Good First Issues](https://github.com/LearnersBlock/learners-block/contribute) and our [voting platform](https://vote.learnersblock.org) which contains a list of features prioritised by the community.

### Bug reports

For bug reports, please search existing issues before posting a ticket. 

### Translation of the interface

We encourage translations and adjustments to current translations on all our components. These can be contributed via [Weblate](https://translate.learnersblock.org).  

### Donations

As with all community projects, we do incur costs. You can see everything we have spent, everything we have been donated and you can donate yourself through our [funding page](https://docs.learnersblock.org/about-us#how-we-are-funded). 

## License

Learner’s Block is released under the [GPL-3.0 License](https://github.com/LearnersBlock/learners-block/blob/master/LICENSE)

## Attribution

Many great open-source projects provide the foundation to make this possible, and we would like to thank and recognise them all:

* [Open Balena](https://www.balena.io/open/)
* [IFM](https://github.com/misterunknown/ifm/)
* [Book Stack](https://www.bookstackapp.com/)
* [GitBook](http://gitbook.com)
* [Weblate](https://weblate.org)
* [Feature UpVote](https://featureupvote.com/lp/powered_by_feature_upvote/?product=Learner%27s%20Block&utm_source=live_button&utm_medium=powered-link)
* [Strapi](https://strapi.io)
