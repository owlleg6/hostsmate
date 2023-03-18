#!/bin/bash

khostman_app=$KHOSTMAN_APP
CRON_JOB_NAME="khostman.cron"
FREQUENCY=$1

DAILY_CRON_DIR="/etc/cron.daily"
WEEKLY_CRON_DIR="/etc/cron.weekly"
MONTHLY_CRON_DIR="/etc/cron.montly"


ETC_ANACRON_PATH="/etc/anacrontab"


# $FREQUENCY map:
#
# 1: daily
# 2: weekly
# 3: montly


# Return a path to a cron specific directory based on the requested frequency
function get_frequency_dir() {

    case $frequency in
        1) echo $DAILY_CRON_DIR ;;
        2) echo $WEEKLY_CRON_DIR ;;
        3) echo $MONTHLY_CRON_DIR
    esac
}




# Verify if the job is already set in frequency-specific directories
function remove_job_file_if_exists(){

    for directory in $DAILY_CRON_DIR $WEEKLY_CRON_DIR $MONTHLY_CRON_DIR;
    do
        if [ -f "$directory/$CRON_JOB_NAME" ]; then
            rm -f "$directory/$CRON_JOB_NAME"
        fi
    done
}

# Create and write to anacron job file
function create_job_file(){
    cron_job_dir=$(get_frequency_dir)

    case $frequency in
        1)
        echo "@daily /usr/sbin/anacron -s -t $ETC_ANACRON_PATH" > "$cron_job_dir/$CRON_JOB_NAME";;
        2)
        echo "@weekly /usr/sbin/anacron -s -t $ETC_ANACRON_PATH" > "$cron_job_dir/$CRON_JOB_NAME" ;;
        3)
        echo "@monthly /usr/sbin/anacron -s -t $ETC_ANACRON_PATH" > "$cron_job_dir/$CRON_JOB_NAME"
    esac
}

# Create /etc/anacrontab if not exists
function create_anacrontab_if_not_exists() {
    if [ ! -f $ETC_ANACRON_PATH ]; then
    touch $ETC_ANACRON_PATH
    fi
}

# Remove previous khosman job from the /etc/anacrontab file if exists
function remove_khostman_job_from_anacrontab(){
    job_line=$(grep $KHOSTMAN_APP $ETC_ANACRON_PATH)

    if [[ $job_line ]]; then
        sed -i "/$job_line/d" $ETC_ANACRON_PATH
    fi
}

function add_khostman_job_to_anacron(){
    case $frequency in
    1)
    echo "@daily $KHOSTMAN_APP" >> $ETC_ANACRON_PATH ;;
    2)
    echo "@weekly $KHOSTMAN_APP" >> $ETC_ANACRON_PATH ;;
    3)
    echo "@monthly $KHOSTMAN_APP" >> $ETC_ANACRON_PATH
    esac
}


get_frequency_dir
remove_job_file_if_exists
create_job_file
create_anacrontab_if_not_exists
add_khostman_job_to_anacron


