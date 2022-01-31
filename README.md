# Is it up?

A simple website availability monitor based on [Apache Kafka][kafka] and [PostgreSQL][postgres].

[kafka]: https://kafka.apache.org/
[postgres]: https://www.postgresql.org/

-------------------------------------------------------------------------------

The project relies on YAML configuration files to run.
An example configuration file can be found in this repository under the name `config.dev.yml`.
Each line is required, except for the those under the `Certificates and keys` section (**NOTE**: this strictly for local development, use certificates and keys as needed for production).

To define which domains you want monitored you can either:
- define a line separated file and point to it from the configuration file,
- or define the domains as a list under the `domains` key in the configuration file.

## Requirements

Required:
- [`docker-compose`][docker-compose-docs]

Optional:
- [Virtualenv][virtualenv] (or similar)
    - For local development outside of Docker.
- [Make][make]
    - For convenince.

[docker-compose-docs]: https://docs.docker.com/compose/
[virtualenv]: https://docs.docker.com/compose/
[make]: https://www.gnu.org/software/make/

## Development

_TL;DR:_ `make run-dev` _and you have everything running locally._

### Local

Local development relies on `config.dev.yml` for configuartion.
`docker-compose.dev.yml` defines a local Kafka (with Zookeeper) and Postgres Docker container instance.

To run the project locally you can simply run:

    make run-dev

Or alternatively, if you prefer the command line:

    docker-compose --file docker-compose.dev.yml up

For local development you may not want to rebuild all Docker containers each time or restart all services.
Instead, run the following commands to only build the `producer` and `consumer` upon changes:

    make rebuild-dev

Or alternatively, if you prefer the command line:

	docker-compose --file docker-compose.dev.yml \
		up --detach --build \
		isitup-consumer-dev isitup-producer-dev

To validate that your Postgres database has been populated run:

    make peek-data

Or alternatively, if you prefer the command line:

    docker-compose --file docker-compose.dev.yml \
		build isitup-producer-dev isitup-consumer-dev

### Production

For production use a configuration file named `config.prod.yml` set in the project root.
In case you need SSL for Kafka define those as well.

The production version of this project relies on `docker-compose.prod.yml`.
The recipe assumes that you have Kafka and Postgres running somewhere else, and creates just the `producer` and `consumer` locally.

To run the production build execute:

    make run-prod

Or alternatively, if you prefer the command line:

    docker-compose --file docker-compose.prod.yml up

Modify `docker-compose.prod.yml` to your needs.

### Testing

Tests are based on [`pytest`][pytest].
To execute, run the following command in the root of the project:

    pytest

[pytest]: https://docs.pytest.org/en/6.2.x/

## Future improvements

- Make Dockerfiles more standalone.
    - Right now they only work in conjunction with a `docker-compose.yml` file.
    - They could also be merged, as they're near identical.

- Implement integration tests for both the `consumer` and `producer`.
    - Testing in general is lacking.
    - Test by hand have been performed extensively.

- Add timestamp of ping to the `producer`.

- Validation of data passed onto Kafka.

- Python typehints.
    - Generates more readable and self-explanatory code.

- A proper configuration library.
    - The current solution is a bit ad-hoc and could use a proper configuration library.

- Better project packaging.
    - Right now everything is simply based on Docker and ad-hoc commands.

## Known issues

The `producer` does not currently wait for Kafka to be up.
In local development this means that the Docker container crashes multiple times before starting normally.

The `table_name` of the database is inserted with an f-string.
This could pontetially lead to issues (even fatal) if the name is set incorrectly and the SQL statement fails completely.
This was left in due to time-constraints, but noted here for full transparency.

## Attributions

- Kafka Docker container: [github.com/wurstmeister/kafka-docker][gh-kafka-docker]
    - For figuring out connections to Kafka over Docker: [github.com/wurstmeister/kafka-docker/issues/385#issuecomment-645077059][gh-kafka-conn]

- Python parallelism: [docs.python.org/3/library/concurrent.futures.html][py-para-docs]

- [`psycopg2-binary` not `psycopg2`][so-psycopg2-binary]

- [Kafka python][pypi-kafka-python]

- [`pytest` and setting ENV variables][pytest-env]

- Friends and family.

[gh-kafka-docker]: https://github.com/wurstmeister/kafka-docker
[gh-kafka-conn]: https://github.com/wurstmeister/kafka-docker/issues/385#issuecomment-645077059
[py-para-docs]: https://docs.python.org/3/library/concurrent.futures.html
[so-psycopg2-binary]: https://stackoverflow.com/questions/30940167/psycopg2-attributeerror-module-object-has-no-attribute-extras/51193228#51193228
[pytest-env]: https://shay-palachy.medium.com/temp-environment-variables-for-pytest-7253230bd777
[pypi-kafka-python]: https://pypi.org/project/kafka-python/
