#!/bin/sh -e
#
# Rebuild for developement

# Secrets

. ${HOME}/.secrets/passwords.sh
DEFAULT_LDAP_SERVER_PASSWORD=$edrn_ldap_manager_password
export DEFAULT_LDAP_SERVER_PASSWORD

# Argument check

if [ $# -ne 0 ]; then
    echo "😩 This program takes no arguments; try again?" 1>&2
    exit 1
fi


# Sentinel files check

if [ ! -f "manage.sh" -o ! -f "local.py" ]; then
    echo "🚨 Run this from the checked out zipperlab repository; you should have" 1>&2
    echo "manage.sh and local.py files in the current directory. You may have to" 1>&2
    echo "create local.py, setting SECRET_KEY to anything and ALLOWED_HOSTS to a list of"
    echo "just the single character *. You can also disable CACHES and turn off the" 1>&2
    echo "SILENCED_SYSTEM_CHECKS for captcha.recaptcha_test_key_error while in" 1>&2
    echo "development." 1>&2
    exit 1
fi


# Normally we'd need to transfer an existing database, but we're starting off from scratch
# here.

# Warning

cat <<EOF
❗️ This program will wipe out your local "zipperlab" PostgreSQL database.

If you have any local changes to your content database or media blobs
you want to preserve, abort now!

⏱️ You have 5 seconds.
EOF


# Here we go

sleep 5
trap 'echo "😲 Interrupted" 1>&2; exit 1' SIGINT

echo "🏃‍♀️Here we go"
dropdb --force --if-exists "zipperlab"
createdb "zipperlab" 'Database for Zipperlab'


# Normally we'd need to transfer an existing database, but we're starting off from scratch
# here.

./manage.sh makemigrations
./manage.sh migrate
./manage.sh collectstatic --no-input --clear --link


# Add additional upgrade steps here:

./manage.sh zipperlab_bloom --hostname localhost --port 6468

# And make development a breeze

./manage.sh clear_cache --all

echo '🏁 Done! You can start it with:'
echo './manage.sh runserver 6468'

exit 0
