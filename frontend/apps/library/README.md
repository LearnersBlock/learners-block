# Learner's Block Library

This code and repository provides for https://library.learnersblock.org as well as the source code for Library access on the [Learner's Block](https://github.com/LearnersBlock/learners-block).

Contributions are welcome, please see the open issues and Good First Issues tag for guidance. 

Resources stored on this database are not managed through this repository, they are maintained through a seperate backend. Resources submissions can be made through our [contact page](https://learnersblock.org/contact) until a submissions page is added. 

# Development

## Backend

The backend for this site is served by [Strapi](https://strapi.io). Please see the [template repository](https://github.com/LearnersBlock/library-backend-template) for details on building a development backend. 

## Install the dependencies
`yarn install`

### Start the app in development mode.
The code will build for use on the Learner's Block when the `ONDEVICE=TRUE` variable exists in the build environment. If the variable is missing, it will start in web mode for library.learnersblock.org.

`quasar dev`

### Lint the files
yarn run lint

### Build the app for production
The code will build for use on the Learner's Block when the `ONDEVICE=TRUE` variable exists in the build environment. If the variable is missing, it will start in web mode for library.learnersblock.org.

`quasar build`

### Customize the configuration
See [configuring quasar.conf.js](https://quasar.dev/quasar-cli/quasar-conf-js).

## Add Languages
To add languages for i18n, go src/layouts/MainLayout, add the language to const languages and name it. Then go to src/i18n and mimic all the files and content from en-US folder. Then go to src/i18n/index.ts and add the import to the file created there.

## Bug reports

For bug reports, please search existing issues before posting a ticket. 

## Translation of the interface

We encourage translations and adjustments to current translations on all our components. These can be contributed via [Weblate](https://translate.learnersblock.org).  

## Donations

As with all community projects, we do incur costs. You can see everything we have spent, everything we have been donated and you can donate through our [funding page](https://docs.learnersblock.org/about-us#how-we-are-funded). 

## License

Learner’s Block is released under the [GPL-3.0 License](https://github.com/LearnersBlock/learners-block/blob/master/LICENSE)
