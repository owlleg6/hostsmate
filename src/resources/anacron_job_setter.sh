#! /bin/bash

FREQUENCY=$1
HOSTSMATE_APP=$2
ETC_ANACRON_PATH="/etc/anacrontab"

function remove_hostsmate_job_from_anacrontab {
    job_line=$(grep -n "$HOSTSMATE_APP" "$ETC_ANACRON_PATH" | cut -d : -f 1)
    if [[ $job_line ]]; then
        sed -i "${job_line}d" "$ETC_ANACRON_PATH"
    fi
}

function add_hostsmate_job_to_anacron {

    case $FREQUENCY in
        1)
        echo "1       7       cron.daily      $HOSTSMATE_APP" >> $ETC_ANACRON_PATH ;;
        2)
        echo "7       12       cron.weekly      $HOSTSMATE_APP" >> $ETC_ANACRON_PATH ;;
        3)
        echo "@monthly        15       cron.monthly      $HOSTSMATE_APP" >> $ETC_ANACRON_PATH
    esac
}

remove_hostsmate_job_from_anacrontab
add_hostsmate_job_to_anacron
