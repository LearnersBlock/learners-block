# Learner’s Block

Learner’s Block is still under development and not yet ready for stable production. Check back here for updates on progress, or follow our ‘Pre-Deployment’ project list. 

https://learnersblock.org

## Documentation

All of our documentation is stored and maintained [here](https://docs.learnersblock.org). 

## Description

An open source project that lets individuals and organisations provide their educational resources, websites and apps to users offline.

## Installation

### Development

A development environment is provide in this repo. Docker-compose.yml on your local system will compile and launch an instance locally. 

All development changes however, will require testing through the Balena OS and relevant hardware before being deployed to the fleet of devices. Follow the [Balena local deployment](https://www.balena.io/docs/learn/develop/local-mode/) documentation to do so.

### Production 

#### Pre-built

Learner’s Block software is provided as an entire package, including an operating system with pre-defined keys that allow for automatic updates. To benefit from these, [download the image files](https://downloads.learnersblock.org).

#### Deploy locally

You may deploy the code to a device locally. We recommend the Balena documentation listed below to do so. This approach however will not benefit from automatic update, and we cannot offer support for its use. 

[Balena Local Deployments](https://www.balena.io/docs/learn/develop/local-mode/)

#### Deploy to your own server

As open source software, you can deploy to your own [Balena](https://www.balena.io) instance and serve your own automatic updates. We cannot however support installation and use via this method. 

[Balena Server Based Deployments](https://www.balena.io/docs/learn/deploy/deployment/). 

## Translation of the interface

We encourage translations and adjustments to current translations on all our components. These can be contributed via [Weblate](https://hosted.weblate.org/projects/learners-block/).  

## License

Learner’s Block is released under the [GPL-3.0 License](https://github.com/LearnersBlock/learners-block/blob/master/LICENSE)

## Contributing

We welcome contributions, they are what keep the Block alive! For pull requests we suggest discussing the changes through a ticket first, for your own sake in case there are already changes ongoing that will affect your contribution. 

## Bug report or pull request

For bug reports, please search existing issues before posting a ticket. 

## Attribution

Many great open source projects provide the foundation to make this possible, and we would like to thank and recognise them all:

* [Open Balena](https://www.balena.io/open/)
* [Book Stack](https://www.bookstackapp.com/)
* [GitBook](http://gitbook.com)
* [Weblate](https://weblate.org)
