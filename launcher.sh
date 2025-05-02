#!/bin/sh
echo "$(date) — autorun triggered for device: \"$1\"" >> /home/klsnkv/python_cron/log.txt
/usr/bin/python /home/klsnkv/python_cron/script.py "$@"
