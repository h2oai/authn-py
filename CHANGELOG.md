# Changelog

## [2.0.0](https://github.com/h2oai/authn-py/compare/v1.1.1...v2.0.0) (2024-02-05)


### ⚠ BREAKING CHANGES

* Python 3.7 is no longer supported. The minimum supported version is now Python 3.8.

### Features

* 🧑‍💻 Implement `__str__` for `TokenEndpointError` to provide more info in tracebacks. ([#83](https://github.com/h2oai/authn-py/issues/83)) ([7317215](https://github.com/h2oai/authn-py/commit/7317215ba82e8b430207b1b936229f31b866b68b)), closes [#81](https://github.com/h2oai/authn-py/issues/81)


### Build System

* 💥 remove support for Python 3.7 ([6d1dfce](https://github.com/h2oai/authn-py/commit/6d1dfced40263e88ecb496f06842ecf1980c14fa))


### Continuous Integration

* 👷 extend testing matrix of the httpx dependency ([#80](https://github.com/h2oai/authn-py/issues/80)) ([bd11cbf](https://github.com/h2oai/authn-py/commit/bd11cbfc63fd41069de90ea610cd46d346e85ad0))

## [1.1.1](https://github.com/h2oai/authn-py/compare/v1.1.0...v1.1.1) (2023-12-05)


### Documentation

* 📝 Fix discovery example in the README ([#69](https://github.com/h2oai/authn-py/issues/69)) ([7657e6e](https://github.com/h2oai/authn-py/commit/7657e6ed7540113ca6310cb765af285a4944c82a))
* 📝 remove dropped `service` parameter from the discovery example in README ([#71](https://github.com/h2oai/authn-py/issues/71)) ([3e02562](https://github.com/h2oai/authn-py/commit/3e02562c6b5413af8519509c8901f6c7829ea119))

## [1.1.0](https://github.com/h2oai/authn-py/compare/v1.0.0...v1.1.0) (2023-09-18)


### Features

* ✨ allow to set timeout and ssl_context for the underlying http client. ([#61](https://github.com/h2oai/authn-py/issues/61)) ([a9b836b](https://github.com/h2oai/authn-py/commit/a9b836bd4398a7fd775b7e49d90cee64de99f270))
* ✨ optionally support creation of token providers from discovery objects ([#54](https://github.com/h2oai/authn-py/issues/54)) ([bb7608f](https://github.com/h2oai/authn-py/commit/bb7608f620f136fe6b1a2210e0f71d798f685a37))
* 🏷️ mark package as typed ([#53](https://github.com/h2oai/authn-py/issues/53)) ([b6fdd48](https://github.com/h2oai/authn-py/commit/b6fdd48b21f62225be0204fc8649f21c0666a09f))
