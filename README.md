[![learnersblock.org](https://raw.githubusercontent.com/LearnersBlock/learners-block/master/frontend/apps/interface/src/assets/logos/lb-logo-full.svg)](https://learnersblock.org)

Learner’s Block is still under development and not yet ready for stable production. Check back here for updates on progress or follow our [pre-deployment project list](https://github.com/LearnersBlock/learners-block/projects/3). 

## Description

An open-source project that lets individuals and organisations provide their educational resources, websites and apps to users offline.

More info at: https://learnersblock.org

## Documentation

All of our documentation is available [here](https://docs.learnersblock.org). 

## Technical Details

This project is made possible by Balena OS, an operating system designed for IoT devices. On top of the OS goes the code provided in this repository. For more details on the technical structure of the operating system and this code, please see our [technical details page](https://docs.learnersblock.org/advanced-features/technical-details).

## Installation

### Development

We provide and recommend using our Docker based development environment. The environment is built towards Mac OS AMD64. If you are running on another system, you may need to alter the image names in each of the Dockerfiles, replacing `amd64` with your operating system. A list of available images can be found [here]( https://www.balena.io/docs/reference/base-images/base-images/).  

To start the development environment, clone the repository and run:

`docker-compose -f docker-compose-dev.yml up --build`

 Enabling the Docker BuildKit will speed up build times considerably. 

After the containers start, required Node modules will be installed and development services run. This may take some time on the first run, please be patient. 

Once all the build processes have completed, the components will be available on the following ports:

```
Frontend interface: 8082
Controller: 9090
WiFi-Connect: 8080
```

Each component is started in development mode, with hot-reload. Changing files in the folders on your system will trigger the reload.

You can also see a production build (no hot-reload) on port `8081` if you build the interface first using: `docker-compose -f docker-compose-build.yml up --build`

All development changes will require testing through the Balena OS and relevant hardware before being deployed to the fleet of devices. We will do our best to help with this but encourage as thorough testing as possible before submitting Pull Requests. Follow the [Balena local deployment](https://www.balena.io/docs/learn/develop/local-mode/) documentation on how to deploy to a local device.

### Production 

#### Pre-built

Learner’s Block software is provided as a complete package ready to flash to an SD card, including an operating system with pre-defined keys that allow for automatic updates. To benefit from these automatic updates [download the image files](https://downloads.learnersblock.org).

#### Deploy locally

You may deploy the code to a device locally. This approach, however, will not benefit from automatic updates, and we cannot offer support for its use. 

In order to prepare the code from this repository for deployment to a device:

2. Download the [OS for your device](https://www.balena.io/os/) and flash it to your memory card. 
1. Clone this repository.
2. Execute `docker-compose -f docker-compose-build.yml up --build` to build the required components.
3. After installing the [Balena CLI](https://github.com/balena-io/balena-cli), run `balena push hostname-of-your-device.local` to deploy. 

More information on local deployments is available from Balena:

[Balena Local Deployments](https://www.balena.io/docs/learn/develop/local-mode/)

#### Deploy to your own server

As open-source software, you can deploy to your own [Balena](https://www.balena.io) instance and serve your own updates. We cannot however support installation and use via this method. 

[Balena Server Based Deployments](https://www.balena.io/docs/learn/deploy/deployment/)

## Feature requests

We thrive to ensure the features developed are those most in line with the community's needs. That is why all feature requests are made through our [voting platform](https://vote.learnersblock.org), where users can add ideas and vote for those they feel most important. Please utilise this voting platform rather than adding feature requests to this repository. 

## Contributing

### Pull requests
We welcome contributions, they are what keep the Block alive! For pull requests we suggest discussing the changes through a ticket first. This is for your own sake in case there are already changes ongoing that will affect your contribution. If you are looking to contribute but do not have a specific feature or goal in mind, please check the list of [Good First Issues](https://github.com/LearnersBlock/learners-block/contribute) and our [voting platform](https://vote.learnersblock.org), which contains a list of features prioritised by the community.

### Bug reports

For bug reports, please search existing issues before posting a ticket. 

### Translation of the interface

We encourage translations and adjustments to current translations on all our components. These can be contributed via [Weblate](https://translate.learnersblock.org).  

### Donations

As with all community projects, we do incur costs. You can see everything we have spent, everything we have been donated and you can donate through our [funding page](https://docs.learnersblock.org/about-us#how-we-are-funded). 

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
