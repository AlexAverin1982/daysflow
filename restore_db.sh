#!/bin/sh
set PGPASSWORD=123456
pg_restore -F c -d habitz /backups/habitz.sql