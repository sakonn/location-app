#!/usr/bin/env bash
# Dump current database

SQL_SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../config/db-init" && pwd )"

echo "## cron tasks"
drush cron
echo "## clear and rebuild drupal cache"
drush cr
echo "## cleaning system events log"
drush watchdog-delete all -y
echo "## cleaning drupal cache"
drush sql-cli < "$SQL_SCRIPT_PATH/02_cache_truncate.sql"
echo "## database dump to file $SQL_SCRIPT_PATH/01_schema.sql"
drush sql-dump --ordered-dump > "$SQL_SCRIPT_PATH/01_schema.sql"
echo "## Successful"