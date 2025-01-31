# Zipperlab — Container Image
# ===========================

FROM alpine:3.20


# Configurable Arguments
# ----------------------
#
# - `user_id` defaults to 500 but you can override this if needed.

ARG user_id=500


# Environment Variables
# ---------------------
#
# This doesn't need to be overridden

ENV PYTHONUNBUFFERED=1


# Layers (like Ogres)
# -------------------
#
# Build up the content of the image.
#
#
# Base Packages
# ~~~~~~~~~~~~~

RUN : &&\
    : Add system -S group for zipperlab, group ID -g &&\
    /usr/sbin/addgroup -S -g $user_id zipperlab &&\
    : Add system -S user for zipperlab with no password -D, group zipperlab -g, user ID -u, gecos info -g, home dir -h &&\
    /usr/sbin/adduser -S -D -h /zipperlab -G zipperlab -u $user_id -g 'Zipperlab user' zipperlab &&\
    : Separate installations into a separate "virtual" package for easy removal at the end &&\
    build_deps="automake bzip2-dev cyrus-sasl-dev git g++ gcc libffi-dev libjpeg-turbo-dev libwebp-dev libxml2-dev libxslt-dev make musl-dev openjpeg-dev openldap-dev openssl-dev pcre-dev python3-dev postgresql-dev su-exec tiff-dev zlib-dev py3-pip" &&\
    run_deps="curl krb5-libs libgcc libjpeg-turbo libldap libpq libsasl libstdc++ libwebp libxml2 libxslt netcat-openbsd openjpeg python3 rsync tiff tidyhtml" &&\
    /sbin/apk update --quiet &&\
    /sbin/apk add --no-progress --quiet --virtual build $build_deps &&\
    /sbin/apk add --no-progress --quiet $run_deps &&\
    : See https://github.com/python-ldap/python-ldap/issues/432 for workaround to Python LDAP vs OpenLDAP 2.5 issue &&\
    echo 'INPUT ( libldap.so )' > /usr/lib/libldap_r.so &&\
    :


# Spot Check
# ~~~~~~~~~~
#
# Over on GitHub Actions, we need to fail fast and not hit the six hour run limit, so make sure we got it right

RUN [ `/usr/bin/python3 --version | sed -E 's/[^0-9]*([0-9]+\.[0-9]+)\.[0-9]+/\1/'` = "3.12" ]


# Application Specifics and Clean Up
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# This is handy for development:

RUN : &&\
    echo 'TLS_REQCERT never' >> /etc/openldap/ldap.conf &&\
    :

# The real app setup follows:

RUN : &&\
    /usr/bin/python3 -m venv /app &&\
    /usr/bin/install -o zipperlab -g zipperlab -d /app/media /app/static /app/wheels &&\
    /app/bin/python3 -m ensurepip --upgrade &&\
    /app/bin/pip3 install --quiet --progress-bar off --upgrade pip setuptools wheel &&\
    /app/bin/pip3 install gunicorn==23.0.0 &&\
    :

COPY --chown=zipperlab:zipperlab ./dist/*.whl /app/wheels/
RUN /app/bin/pip3 install --progress-bar off /app/wheels/*.whl

RUN : &&\
    : Get the static files ready &&\
    cd /app &&\
    /sbin/su-exec zipperlab /usr/bin/env SIGNING_KEY=unused /app/bin/django-admin collectstatic --settings jpl.labcas.zipper.policy.settings.ops --no-input --clear --link &&\
    : Clean up clean up everybody everywhere &&\
    /app/bin/pip3 uninstall --yes --quiet pip &&\
    /sbin/apk del --quiet build &&\
    /bin/rm -rf /app/wheels &&\
    /bin/rm -rf /var/cache/apk/* &&\
    /bin/chown -R zipperlab:zipperlab /app/lib/python3.*/site-packages &&\
    :

COPY --chown=zipperlab:zipperlab docker/*.py /app/


# Image Morphology
# ----------------

# Define external shape and other miscellaneous details of the image.

EXPOSE      8000
VOLUME      ["/app/media"]
USER        zipperlab
WORKDIR     /app
ENTRYPOINT  ["/app/bin/gunicorn"]
HEALTHCHECK --interval=5m --timeout=2m --start-period=10m CMD /usr/bin/curl --fail --retry 6 --max-time 5 --retry-delay 10 --retry-max-time 60 http://127.0.0.1:8000/ || /bin/sh -c 'killall5 -TERM && (/bin/sleep 10; killall5 -KILL)'


# Metadata
# --------
#
# Note that ``org.label-schema`` is deprecated, but it's a heck of a lot easier to understand. Still, why not just
# use the Dublin Core?

LABEL "org.label-schema.name"="zipperlab"
LABEL "org.label-schema.version"="0.0.0"
