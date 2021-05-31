# Learner's Block Interface
If choosing to develop locally, it is recommended to change:
```
const devAPI = 'http://0.0.0.0:9090'
```
to:
```
const devAPI = 'http://localhost:9090'
```

This will prevent errors about cookies being stored across domains when using the Quasar default load page of http://localhost:8081.

Alternatively, ensure you navigate to the development page via http://0.0.0.0:8081 and not http://localhost:8081.

## Install the dependencies
```bash
yarn
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
yarn dev
```

### Lint the files
```bash
yarn run lint
```

### Build the app for production
```bash
yarn build
```
