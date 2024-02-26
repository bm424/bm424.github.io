# Local Build

```shell
docker compose build && docker compose run main
```

# Deployment details

Push to `main` branch. .github/workflows/main defines the action taken,
using checkout and (peaceiris/actions-gh-pages)[https://github.com/peaceiris/actions-gh-pages/tree/main/src] to push build directory to `gh-pages` branch.
