# Changelog

## [3.0.0](https://github.com/h2oai/authn-py/compare/v2.0.1...v3.0.0) (2024-07-12)


### ⚠ BREAKING CHANGES

* Python 3.7 is no longer supported. The minimum supported version is now Python 3.8.
* Python 3.7 is no longer supported. The minimum supported version is now Python 3.8.

### Features

* ✨ allow to set timeout and ssl_context for the underlying http client. ([#61](https://github.com/h2oai/authn-py/issues/61)) ([a9b836b](https://github.com/h2oai/authn-py/commit/a9b836bd4398a7fd775b7e49d90cee64de99f270))
* ✨ optionally support creation of token providers from discovery objects ([#54](https://github.com/h2oai/authn-py/issues/54)) ([bb7608f](https://github.com/h2oai/authn-py/commit/bb7608f620f136fe6b1a2210e0f71d798f685a37))
* 🏷️ mark package as typed ([#53](https://github.com/h2oai/authn-py/issues/53)) ([b6fdd48](https://github.com/h2oai/authn-py/commit/b6fdd48b21f62225be0204fc8649f21c0666a09f))
* 🧑‍💻 Implement `__str__` for `TokenEndpointError` to provide more info in tracebacks. ([#83](https://github.com/h2oai/authn-py/issues/83)) ([7317215](https://github.com/h2oai/authn-py/commit/7317215ba82e8b430207b1b936229f31b866b68b)), closes [#81](https://github.com/h2oai/authn-py/issues/81)


### Bug Fixes

* :arrow_up: bump httpx from 0.23.3 to 0.24.1 ([#47](https://github.com/h2oai/authn-py/issues/47)) ([1fbed27](https://github.com/h2oai/authn-py/commit/1fbed277c6f53ee9b320ddb62f422e3b11841328))
* :arrow_up: bump mypy from 0.942 to 1.4.1 ([#50](https://github.com/h2oai/authn-py/issues/50)) ([50ba452](https://github.com/h2oai/authn-py/commit/50ba452c4f18ff7b1797fd2444bbf39cd7bf9c06))
* :arrow_up: bump nox-poetry from 0.9.0 to 1.0.3 ([#51](https://github.com/h2oai/authn-py/issues/51)) ([889a1ce](https://github.com/h2oai/authn-py/commit/889a1ce90cd70e0a75788873665db23e6ab99813))
* :arrow_up: bump pytest-asyncio from 0.16.0 to 0.21.1 ([#48](https://github.com/h2oai/authn-py/issues/48)) ([a7069f1](https://github.com/h2oai/authn-py/commit/a7069f1d60dca479be1c100de61e8dd8c9954f68))
* :arrow_up: bump time-machine from 2.9.0 to 2.10.0 ([#49](https://github.com/h2oai/authn-py/issues/49)) ([42e5f2b](https://github.com/h2oai/authn-py/commit/42e5f2beab0c323071257cd0cb7cafd1bdccb8c3))
* :arrow_up: update h2o-cloud-discovery requirement ([#84](https://github.com/h2oai/authn-py/issues/84)) ([2506159](https://github.com/h2oai/authn-py/commit/250615916f00df44c147920774e65577fdeaf0f2))


### Documentation

* ✏️ remove parametr that was removed from the readme. ([#68](https://github.com/h2oai/authn-py/issues/68)) ([3732449](https://github.com/h2oai/authn-py/commit/3732449b1468314db64a3fd179e7c573a8a3fc87))
* 📝 Fix discovery example in the README ([#69](https://github.com/h2oai/authn-py/issues/69)) ([7657e6e](https://github.com/h2oai/authn-py/commit/7657e6ed7540113ca6310cb765af285a4944c82a))
* 📝 remove dropped `service` parameter from the discovery example in README ([#71](https://github.com/h2oai/authn-py/issues/71)) ([3e02562](https://github.com/h2oai/authn-py/commit/3e02562c6b5413af8519509c8901f6c7829ea119))


### Build System

* 💥 remove support for Python 3.7 ([6d1dfce](https://github.com/h2oai/authn-py/commit/6d1dfced40263e88ecb496f06842ecf1980c14fa))


### Continuous Integration

* 👷 extend testing matrix of the httpx dependency ([#80](https://github.com/h2oai/authn-py/issues/80)) ([bd11cbf](https://github.com/h2oai/authn-py/commit/bd11cbfc63fd41069de90ea610cd46d346e85ad0))

## [2.0.1](https://github.com/h2oai/authn-py/compare/v2.0.0...v2.0.1) (2024-07-12)


### Bug Fixes

* :arrow_up: update h2o-cloud-discovery requirement ([#84](https://github.com/h2oai/authn-py/issues/84)) ([2506159](https://github.com/h2oai/authn-py/commit/250615916f00df44c147920774e65577fdeaf0f2))

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
