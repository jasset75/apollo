# Apollo Microservice v0.1

This project implements a REST API to select data from Apache Cassandra through Apache Spark. The Spark cluster computes commands requested by HTTP client through Apollo API endpoints.

I wrote this [notes](https://jasset75.github.io/Spark-Cassandra-Notes/Environment.html) in order to follow a recipe to mount a development environment. Besides, there are some examples and scripts which loads the data sources used in those and these examples.

## Apollo REST API

## Useful tools

### Apiari.io

It is oriented to describe and test REST APIs. Supports Swagger and API Blueprint formats, as well as automation. Integrates with Dredd, which is a framework for validating API description document against backend implementation of the API.

### Insomnia

Insomnia is of kind of applications that is highly recommended to develop a REST API. It has as prominent features:

- Usable GUI
- Different Environment management
- The whole range of HTTP verbs: GET, PUT, POST, DELETE, etc.
- Exportable environment file with JSON format for sharing
- Response beautifier
...

```sh
# Add to sources
echo "deb https://dl.bintray.com/getinsomnia/Insomnia /" \
    | sudo tee -a /etc/apt/sources.list.d/insomnia.list

# Add public key used to verify code signature
wget --quiet -O - https://insomnia.rest/keys/debian-public.key.asc \
    | sudo apt-key add -

# Refresh repository sources and install Insomnia
sudo apt-get update
sudo apt-get install insomnia
```
