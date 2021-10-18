# Learner's Block Interface
If choosing to develop outside of the Docker environment, ensure you navigate to the development page via http://0.0.0.0:8081 and not http://localhost:8081 to prevent errors around cookies being stored across domains (CORS).

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
