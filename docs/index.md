# Apollo Microservice v1.0 Alpha

This project implements a REST API to select data from Apache Cassandra taking advantage of the power of Apache Spark. Spark cluster computes commands requested by HTTP clients through Apollo API endpoints.

I've written these [notes](https://jasset75.github.io/Spark-Cassandra-Notes/Environment.html) with which to follow a recipe to build a development environment. Besides, there you can find some examples and scripts which loads the data sources used in those and these examples.

> API Blueprint format. [See in Apiario.io](https://apollo20.docs.apiary.io)

# Apollo REST API

Spark-Cassandra Rest API

Apollo is a Microservice which allows data computing with Apache Spark from Apache Cassandra database.

Apache Cassandra is a highly scalable platform, it is ready to store a huge volume 
of data but it is not able to do join between data tables, 
so in order to make this kind of algebraic operations we need a tool like Apache Spark, powerful and highly scalable as well.

This API implements an interface between an app client and Spark-Cassandra environment. Furthermore, using Sparl SQL module we access to join, union... relational algebra operations in general.

## API Enpoints

+ [/about](./apidoc/about.md)
+ [/version](./apidoc/version.md)
+ [/create-table](./apidoc/create-table.md)
+ [/get-table](./apidoc/get-table.md)
+ [/join](./apidoc/join.md)
+ [/union](./apidoc/union.md)

>Updated Source at:
>[Apiary Documentation](https://apollo20.docs.apiary.io)

>NOTE: Examples and test are based on data and examples of this [repository](https://jasset75.github.io/Spark-Cassandra-Notes/).

## Internals

### _admix_

Python library which implements interface with Apache Cassandra.

+ [admix](./apidoc/admix.md) documentation.

### _quiver_

Python library which implements interface with Apache Spark.

+ [quiver](./apidoc/quiver.md) documentation.

## Useful tools

### Insomnia

Insomnia is that kind of applications that is highly recommended to develop a REST API. It has as prominent features:

- Usable GUI.
- Different Environment management.
- The whole range of HTTP verbs: GET, PUT, POST, DELETE, etc.
- Exportable environment file with JSON format for sharing.
- Response beautifier.

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

### Apiari.io

It is oriented to describe and test REST APIs. Supports Swagger and API Blueprint formats, as well as automation. Integrates with Dredd.

Apiary uses mainly two API description languages API Blueprint and Swagger.

I've used API Blueprint and Dredd for automatic test.

### Dredd

Is an language-agnostic test API Framework. It integrates with continuous integration environments. This validation software has a command-line tool which runs description document against API implementation. To do so, developers write specific test with format request-response that tool applies automatically each time is invoked from command-line or in a higher level platform.

Dredd requires Node Js and npm.

```sh
$ npm install -g dredd
```

Dredd supports several description languages such as API Blueprint or Swagger. In this case we are using API Blueprint. Command example to run test:

```sh
dredd apiary.apib http://localhost:5000
```

Results:
```sh
info: Beginning Dredd testing...
pass: GET (200) /about duration: 136ms
pass: GET (200) /version duration: 17ms
pass: POST (201) /create-table duration: 54ms
pass: POST (201) /create-table duration: 32ms
pass: POST (201) /create-table duration: 29ms
pass: POST (201) /create-table duration: 24ms
pass: POST (201) /create-table duration: 17ms
pass: POST (201) /create-table duration: 29ms
pass: POST (201) /create-table duration: 24ms
pass: POST (200) /get-table duration: 3690ms
pass: POST (200) /get-table duration: 3109ms
pass: POST (200) /get-table duration: 1852ms
pass: POST (200) /get-table duration: 2197ms
pass: POST (200) /get-table duration: 4484ms
pass: POST (200) /join duration: 3016ms
pass: POST (200) /join duration: 1435ms
pass: POST (200) /join duration: 17920ms
pass: POST (200) /union duration: 1007ms
pass: POST (200) /union duration: 1155ms
complete: 19 passing, 0 failing, 0 errors, 0 skipped, 19 total
complete: Tests took 40247ms
```
