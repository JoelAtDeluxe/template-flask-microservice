# Flask Microservice Example

This project represents one way of structuring a (python 3) flask application. Note that some of these decisions are subjective and may not fit your needs exactly. Regardless, this can be helpful as a starter project for people new to microservices, or new to flask, as it provides some "batteries included" approaches to solving basic problems.

## Overview

This project contains some of the features that a typical microservice might encounter. This service focsues on only a shell application, with minimal actual logic. Further logic will be added to flesh out a concept to provide a more natural experience.

Project Features:

* DevOps related items
  * Docker/Docker-compose
    * Docker to help the CI/CD component, while the docker-compose to help provide a consistent testing/production like environment.
  * Gitlab CI / image hosting
    * An example of how a CI solution _might_ look. This focuses only on the creating and storage of the docker image, and eschews deployment concerns
* Development Assistance
  * Pipenv
    * Similar to a package.json, this file set (Pipfile/Pipfile.lock) help manage dependencies
  * Makefile
    * A place to keep the many simple, but repetative tasks associated with building/testing this project
  * .env / .env_template
    * A place to store local configuration details. Works especially well with pipenv, which will auto-load the environment variables when entering the pipenv shell
* Code features
  * Simple flask routing, Including...
    * Versioned api starting point
    * Unversioned api features to aid in development/issue diagnosis
  * Swagger/OpenAPI docs
  * Structured Logging
  * Ability to turn of flask logging, if so desired (may be desirable if consistent logging is needed throughout an application)
  * Unit testing via pytest
    * Though actual unit tests are missing presently
  * docstring testing
    * Though actual docstrings are missing presently
  * Reading configuration via environment variables

## Development Overview

### Requirements

* `python 3.7+` (This can be switched to python 3.6 with the removal of dataclasses, which are used sparingly)
* `pip`
* `pipenv`
* `make`
* `docker` & `docker-compose`
* Some familiarity with Python and Flask

### Recommended Environment

* Linux
  * Though OSX should be equally fine
* Visual Studio Code with the python plugin
  * PyCharm / Intellij IDEA should be equally fine (maybe even better than vscode)

### First Run

To start, it may be easiest to run the `make setup` target, which will install a user pipenv version, install the pipenv dependencies for this project, and create a .env file. You will wnat to update the .env file with any additional private configurations necessary for your local testing.

To test out the server, you can run `make run`. A few alternatives exist:

1. Open the pipenv shell by running `pipenv shell` and then run `python src/main.py`
2. Run the main from pipenv without entering the shell via `pipenv run python src/main.py`

These 3 ways are roughly equivalent. The `make` version will build and launch a container (with hot-reloading of code), while the pipenv versions will start local development versions utilizing the .env file (which should also have hot reloading)

### Proect Layout

```bash
├── docker-compose.yml             # Dev version to start a local production-like environment
├── Dockerfile                     # Production version of the dockerfile
├── Dockerfile.dev                 # A dockerfile to enable hot reloading / reading from src directory instead of dist
├── .env                           # loaded environment variables specific to this project
├── .env_template                  # A base for the .env file
├── .gitignore                     # What to not commit to git
├── .gitlab-ci.yml                 # gitlab ci build configuration
├── makefile                       # Simple scripts to help build/run the project
├── Pipfile                        # Version/selection logic for grabbing dependencies
├── Pipfile.lock                   # Version/hash information for all dependencies
├── readme.md                      # This file!
├── dist                           # Where the "release" version of this project goes
└── src                            # All of the project source code
    ├── constants.py
    ├── main.py                    # Dev Entrypoint/logic for starting up the server
    ├── project_config.py          # environment variables configuration
    ├── routes                     # Location for all endpoints + their logic
    │   ├── compliance.py          # Unversioned / microservice-friendly routes
    │   ├── custom_exceptions.py   # Common exceptions for all routes
    │   └── v1.py                  # v1-versioned routes
    ├── state.py                   # Global state holder (use sparingly)
    ├── static                     # All of the files that need to be served statically (this includes swagger)
    ├── tests                      # Unit tests directory (mirrors the src directory)
    └── wsgi.py                    # Entry point when running with gunicorn
```

### Quick Primer on Pipenv

Pipenv is basically a wrapper around virtualenv. Pipenv works by basically setting up a new shell session. While you are in that shell session, all of the environment values from the .env file are available as actual environment variables, and the `python` command plus the dependencies are specific to this shell. Typical usage boils down to these commands:

* `pipenv --three` or `pipenv --two` create new projects with a python3 / python2 runtime, respectively. Alternative actions to do something similar also work
* `pipenv shell` enters the virtual environment
* `pipenv install` installs all of the dependencies needed for this project
* `pipenv install <x>` installs a new dependency for this project.
* `pipenv run <x>` runs an action as if the pipenv environment was active. Useful if you want to just do something quickly

Finally, while in the pipenv shell, you can exit via `exit`

You can find out more about pipenv [here](https://docs.pipenv.org/en/latest/)

### TODO List

There are a few things that need to be added to make this project more complete. In no particular order:

* Add some example logic for some service
* Incorporate authentication requirements (likely JWT)
* Remove some endpoints from non-dev builds (e.g. /config)
* Posisbly replace simplog with struct-logging
* Add in kubernetes deployment / helm files?
* Mypy type checking
* Implement some pytests
* Implement some doc tests
* Implement tracing in addition/in place of structured logging

### Project Decisions

#### Why Python / Why Flask

Python presents a particularly good starting point for a basic microservice, given that the sped of development is high -- python mostly gets out of your way. In addition, the feature support via 3rd party libraries is quite high. The primary downside is speed, and to a lesser degree (depending on your situation), the dynamic typing can be an issue. As performance needs increase, there are two "obvious" options:

1. Look to a different langauge, such as Go or Elixir
2. Try optimizing sections via c modules or Cython. A good talk on Cython's potential can be found [jere](https://www.youtube.com/watch?v=_1MSX7V28Po)

The choice to use Flask is a bit different. Flask advertises itself as a microframework, which means two things: an easy ramp up to basic functionality, and moving a number of features (such as an ORM) into supporitng libraries, allowing to use what they're familiar with. Flask is also quite popular, which makes finding solutions for common issues pretty easy. In short: It's just sort of a common starting point for many. Other alternatives exist which may or may not suit your use case better. Two to look into: [Django](https://www.djangoproject.com/) and [aiohttp](https://aiohttp.readthedocs.io/en/stable/). Django in particular will offer a more batteries-included approach, while aiohttp offers a more efficient async approach.

#### Why pipenv

Dependency management is an important concept in any project. Older python projects tend to go with a virutal environment, which ends up being a bit difficult to use day-to-day. Pipenv wraps virtual environments so that they're a bit more invisible and also manages specific versions of applications better, making setup a bit easier for newer project developers.

#### What's with the project structure

Other than a directory named `src`, this is apretty common structure. Python projects "like" to be pretty flat. However, some project structure -- in particular routing -- really benefit from some hierarchy / namespacing. The rest is merely preference. A more complex application might warrant a more complex structure. A smaller project might warant a cleaner/tighter structure with fewer files.

#### Why Make

Mainly because it works, and it's pretty straight forward. There are some gotchas, for sure, but it provides a simple way to organize all of the ancilary scripts that end up being run often enough to slimply alias.

## Credits

| Person            | Role              | Contact                  | Notes |
| ----------------- | ----------------- | ------------------------ | ----- |
| Joel Smith        | Primary Developer | joel.smith@originate.com |       |
| _Your Name Here!_ |                   |                          |       |
