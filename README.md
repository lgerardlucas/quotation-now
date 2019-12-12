[![Quotation-NOW](https://res.cloudinary.com/quotation-now/image/upload/v1576156892/Quotation-NOW/qnow_favico_linear_lonbyu.png)](https://quotation-now.herokuapp.com/)
# Quotation-NOW


Sobre o projeto
----------------
Quotation Now, ou como gostamos de chamar "Q-NOW", em tradução livre do inglês, significa: "Cotação Agora", é uma plataforma de cotação online para um nicho de mercado muito importante, neste caso Móveis Planejados. Temos a intenção de oferecer, um mecanismo de cotação, que unirá CLIENTES e MARCENARIAS em um só ambiente, dando a ambas as partes, uma experiência simples e eficaz, tanto para o CLIENTE que busca os melhores preços, prazos de entrega e condições de pagamento, como para MARCENEIROS, colocando-os em condições iguais neste mercado com tanta concorrência.





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
