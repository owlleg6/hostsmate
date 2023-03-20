#!/bin/bash

FREQUENCY=$1
KHOSTMAN_APP=$2
ETC_ANACRON_PATH="/etc/anacrontab"

function remove_khostman_job_from_anacrontab(){

    job_line=$(grep -n "$KHOSTMAN_APP" "$ETC_ANACRON_PATH" | cut -d : -f 1)
    if [[ $job_line ]]; then
        sed -i "${job_line}d" "$ETC_ANACRON_PATH"
    fi
}

function add_khostman_job_to_anacron(){

    case $FREQUENCY in
        1)
        echo "1       7       cron.daily      $KHOSTMAN_APP" >> $ETC_ANACRON_PATH ;;
        2)
        echo "7       12       cron.weekly      $KHOSTMAN_APP" >> $ETC_ANACRON_PATH ;;
        3)
        echo "@monthly        15       cron.monthly      $KHOSTMAN_APP" >> $ETC_ANACRON_PATH
    esac
}


remove_khostman_job_from_anacrontab
add_khostman_job_to_anacron
