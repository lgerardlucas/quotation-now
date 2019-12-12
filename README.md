[![Quotation-NOW](https://res.cloudinary.com/quotation-now/image/upload/v1576156892/Quotation-NOW/qnow_favico_linear_lonbyu.png)](https://quotation-now.herokuapp.com/)
# Quotation-NOW


See it in Action
----------------
Sobre-nós
Q-NOW(Quotation Now) É uma plataforma online de cotação de móveis planejados, ligando clientes as melhores empresa de móveis(Marcenarias).






A `requirements.txt` must be present at the root of your application's repository to deploy.

To specify your python version, you also need a `runtime.txt` file - unless you are using the default Python runtime version.

Current default Python Runtime: Python 3.6.7

Alternatively, you can provide a `setup.py` file, or a `Pipfile`. Using `Pipenv` will generate `runtime.txt` based on `python-version` at build time.

Specify a Buildpack Version
---------------------------

You can specify the latest production release of this buildpack for upcoming builds of an existing application:

    $ heroku buildpacks:set heroku/python


Specify a Python Runtime
------------------------

Supported runtime options include:

- `python-3.7.1`
- `python-3.6.7`
- `python-2.7.15`

## Tests

The buildpack tests use [Docker](https://www.docker.com/) to simulate
Heroku's [stack images.](https://devcenter.heroku.com/articles/stack)

To run the test suite:

```
make test
```

Or to test in a particular stack:

```
make test-heroku-18
make test-heroku-16
```

The tests are run via the vendored
[shunit2](https://github.com/kward/shunit2)
test framework.
