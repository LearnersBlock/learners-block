[![learnersblock.org](https://learnersblock.org/images/lb-logo-full.svg)](https://learnersblock.org)

## Description

An open-source project that lets individuals and organisations provide their educational resources, websites and apps to users offline.

More info at: https://learnersblock.org

## Documentation

All of our documentation is available [here](https://docs.learnersblock.org). 

## Technical Details

This project is made possible by Balena OS, an operating system designed for IoT devices. On top of the OS goes the code provided in this repository. For more details on the technical structure of the operating system and this code, please see our [technical details page](https://docs.learnersblock.org/advanced-features/technical-details).

## Installation

### Development Notes

On the GitHub release page you will find a 'pre-release' tagged 'development' which contains all the latest commits from the 'main' branch. These images are linked to our servers for automatic updates but receive all updates as soon as they are pushed to the 'main' branch.

### Development Instructions

A Docker based development environment is available. If you require each component individually, see the README file in the component's folder.

#### Frontend

Start the development environment:

`docker-compose -f docker-compose-dev.yml up --build`

The development environment is accessible through:

`http://0.0.0.0:8081`

Note: Ensure Docker has access to sufficient 'CPUs' and memory via the Docker preferences page before running.

#### Library

Development of the Library interface takes place on a [separate repository](https://github.com/LearnersBlock/library), which is mirrored in this repository at `/frontend/apps/library`. By default, it points to the `main` branch. The Library is served as part of the Docker development environment with hot-reload enabled although pull requests should be made to the [Library repository](https://github.com/LearnersBlock/library). 

#### Using the environments

After the containers start, required Node modules will be installed and development services run. This may take some time on the first run, please be patient. 

Changing files in the folders on your system will trigger the reload on hot-reload components.

All development changes will require testing through the Balena OS and relevant hardware before being deployed to our public fleet of devices. We will do our best to help with this but encourage as thorough testing as possible before submitting Pull Requests. Follow the [Balena local deployment](https://www.balena.io/docs/learn/develop/local-mode/) documentation on how to deploy to a local device.

### Production 

#### Pre-built

Learner’s Block software is provided as a complete package ready to flash to an SD card, including an operating system with automatic updates. To benefit from these automatic updates download the image files from our [downloads page](https://downloads.learnersblock.org).

Alternatively, you can find these images from the GitHub releases page. 

Release names follow the following formats:

**Releases:**
```
# Image which runs production code from 'main' branch when submitted with a version tag.
Learners-Block-%%device-type%%-v%%version-number%%.tar.gz 
```
**Pre-releases:**
```
## Image which runs latest commits from the 'main' branch. 
Learners-Block-%%device-type%%-dev.zip 
```

#### Deploy locally

You may deploy the code to a device locally. This approach, however, will not benefit from automatic updates, and we cannot offer support for its use. Building all the required components on low-powered devices will also take a considerable time or may fail.

In order to prepare the code from this repository for deployment to a device:

2. Download the [OS for your device](https://www.balena.io/os/) and flash it to your memory card. 
1. Clone this repository.
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
We welcome contributions, they are what keep the Block alive! For pull requests we suggest discussing the changes through a ticket first. This is for your own sake in case there are already changes ongoing that will affect your contribution. 

If you are looking to contribute but do not have a specific feature or goal in mind, please check the list of [Good First Issues](https://github.com/LearnersBlock/learners-block/contribute) and our [voting platform](https://vote.learnersblock.org), which contains a list of features prioritised by the community.

### Bug reports

For bug reports, please search existing issues before posting a ticket. 

### Translation of the interface

We encourage translations and adjustments to current translations on all our components. These can be contributed via [Weblate](https://translate.learnersblock.org).  

### Donations

As with all community projects, we do incur costs. You can see everything we have spent, everything we have been donated and you can donate through our [funding page](https://docs.learnersblock.org/about-us/how-we-are-funded). 

## License

Learner’s Block is released under the [GPL-3.0 License](https://github.com/LearnersBlock/learners-block/blob/main/LICENSE)

## Attribution

Many great open-source projects provide the foundation to make this possible, and we would like to thank and recognise them all:

* [Balena](https://www.balena.io/)
* [IFM](https://github.com/misterunknown/ifm/)
* [GitBook](http://gitbook.com)
* [Weblate](https://weblate.org)
* [Feature UpVote](https://featureupvote.com/)
* [Strapi](https://strapi.io)
