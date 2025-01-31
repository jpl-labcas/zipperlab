# 🤐 Zipperlab

Zipperlab is the LabCAS ZIP archiver.


## 🤓 Development

Make the DB

    createdb zipperlab
    ./manage.sh makemigrations
    ./manage.sh migrate wagtailimages  # not sure why this needs to be done separately?
    ./manage.sh migrate

Launch it

    ./manage.sh runserver 6468  # or pick your favorite port


### Essential Environment Variables

TBD.


### Database

TBD.


### Software Installation

TBD.


## 🚢 Containerized Setup

TBD.


### 🎑 Image Building

First, build the wheels by running:

    support/build-wheels.sh

Then build the image:

    docker image build --file docker/Dockerfile --tag edrndocker/zipperlab .

You can do a spot check to see if the image is viable by running

    docker container run --rm --env SIGNING_KEY=key --env ALLOWED_HOSTS='*' --publish 8000:8000 \
        edrndocker/zipperlab:latest

and then visiting http://localhost:8000/. If you get "Server Error (500)", congratulations! It's working.

To launch the orchestrated services (Zipperlab application, PostgreSQL database, Redis cache/message queue, and Celery worker)—or in other words, to _start the composition_—run:

    docker compose --project-name zipperlab --file docker/docker-compose.yaml up --detach

Note the many environment variables that are needed. You'll want to put these into a `.env` file; see the "Environemnt Variables" section, below. Also, after the first launch only, the database is empty and needs to be structured and populated; see the next section.


### 📀 Containerized Database Setup

Create the `zipperlab` database in PostgreSQL:

    docker compose --project-name zipperlab --file docker/docker-compose.yaml \
        exec db createdb --username=postgres --encoding=UTF8 --owner=postgres zipperlab

Make sure the `POSTGRES_PASSWORD` environment variable has the same value when running this command as you did when you started the composition, above.

Next, run the Django database migrations to turn the empty `zipperlab` database into a Django-, Wagtail-, and Zipperlab-capable database:

    docker compose --project-name zipperlab --file docker/docker-compose.yaml \
        exec app /app/bin/django-admin migrate

Finally, populate the content with:

    docker compose --project-name zipperlab --file docker/docker-compose.yaml \
        exec app /app/bin/django-admin zipperlab_bloom



### 🪶 Front End Web Server

TBD.



#### 🏛 Database Structure

TBD.


#### 🥤 Initial Form and Content Population

TBD.


#### 🔻 Subpath Serving

TBD.


### 🍃 Container Environment Variables

TBD.


### 🍃 Environment Variable Reference

| Variable                         | Purpose                                                   | Default |
|:---------------------------------|:----------------------------------------------------------|:--------|
| `ALLOWED_HOSTS`                  | Valid `Host` HTTP headers; others rejected                | `.jpl.nasa.gov` |
| `BASE_URL`                       | Base URL for Wagtail admin interface for generated emails | `https://edrn-labcas.jpl.nasa.gov/zipperlab/` |
| `ZIPPERLAB_VERSION`              | Version of the Zipperlab image in Docker Composition      | `latest` |
| `CACHE_URL`                      | URL to the cache service                                  | `redis://` |
| `CERT_CN`                        | Common name of random TLS certificate                     | `edrn-docker.jpl.nasa.gov` |
| `CSRF_TRUSTED_ORIGINS`           | Comma-separated URLs that provide trusted resources       | `http://*.jpl.nasa.gov,https://*.jpl.nasa.gov` |
| `DATA_DIR`                       | Where Docker Composition can persist voumes               | `/usr/local/labcas/zipperlab/ops/dockerdata` |
| `EMAIL_HOST_PASSWORD`            | Password to log into SMTP server                          | (unset) |
| `EMAIL_HOST_USER`                | Username to log into SMTP server                          | (unset) |
| `EMAIL_HOST`                     | Host name of SMTP server                                  | `smtp.jpl.nasa.gov` |
| `EMAIL_PORT`                     | Port number of SMTP server                                | `587` |
| `EMAIL_USE_SSL`                  | `True` if to use SSL to access SMTP server                | `False` |
| `EMAIL_USE_TLS`                  | `True` if to use TLS to access SMTP server                | `True` |
| `FORCE_SCRIPT_NAME`              | Subpath if the app isn't at the root URL                  | (unset, except `/zipperlab/` in Docker Composition) |
| `HTTP_PORT`                      | `http` non-TLS port (see `PROXY_PORT` for TLS)            | 8080 |
| `IMAGE_RENDITIONS_CACHE_SIZE`    | How many various resolutions of images to cache           | 1000 |
| `IMAGE_RENDITIONS_CACHE_TIMEOUT` | How long to cache image renditions (seconds)              | 86400 |
| `LDAP_CACHE_TIMEOUT`             | Timeout in seconds to cache results from `LDAP_URI`       | 3600 |
| `LDAP_URI`                       | LDAP server for Wagtail administrator authentication      | `ldaps://ldap-202007.jpl.nasa.gov` |
| `MEDIA_ROOT`                     | Filesystem location of user media                         | `$CWD/media` |
| `MEDIA_URL`                      | URL to user media (images, documents)                     | `/media/` |
| `MQ_URL`                         | URL to message queue                                      | `redis://` |
| `POSTGRES_PASSWORD`              | Root password to Postgres DB in Docker Composition        | (unset) |
| `PROXY_PATH`                     | Subpath in TLS-termination of Zipperlab                   | `/zipperlab/` in Docker Composition |
| `HTTPS_PORT`                     | Host port to bind for TLS-based termination of Zipperlab  | `4235` |
| `RECAPTCHA_PRIVATE_KEY`          | Private key of reCAPTCHA service                          | (unset) |
| `RECAPTCHA_PUBLIC_KEY`           | Public key of reCAPTCHA service                           | (unset) |
| `SECURE_COOKIES`                 | `True` if to use secure (HTTPS) cookies only              | `True` |
| `SIGNING_KEY`                    | Opaque key used to sign secrets                           | (unset but required)
| `STATIC_ROOT`                    | Filesystem location of static files                       | `$CWD/static` |
| `STATIC_URL`                     | URL to static resources                                   | `/static/` |

## 👩‍💻 Software Environment

TBD.


### 👥 Contributing

You can start by looking at the [open issues](https://github.com/EDRN/zipperlab/issues), forking the project, and submitting a pull request. You can also [contact us by email](mailto:ic-portal@jpl.nasa.gov) with suggestions.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software. For versions available, see the [releases made](https://github.com/EDRN/zipperlab/releases) on this project.


## 👩‍🎨 Creators

The principal developer is:

- [Sean Kelly](https://github.com/nutjob4life)

The QA team consists of:

- [Heather Kincaid](https://github.com/hoodriverheather)

To contact the team as a whole, [email the Informatics Center](mailto:ic-portal@jpl.nasa.gov).

## 🏞️ Image Credits

TBD.


## 📃 License

The software is licensed under the [Apache version 2](LICENSE.md) license.
