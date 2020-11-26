#!/bin/bash
  
# ID chat Telegram
USERID="897604004"

# API Token of bot
TOKEN="992709882:AAFxMGufKO5g4BcoAHqaQ-wGL-Je-I33RxM"

TIMEOUT="10"

# URL sent message of bot
URL="https://api.telegram.org/bot$TOKEN/sendMessage"

# System's date
DATE_EXEC="$(date "+%d %b %Y %H:%M")"

# File temp
TMPFILE='/tmp/ipinfo.txt'

if [ -n "$SSH_CLIENT" ]; then
    IP=$(echo $SSH_CLIENT | awk '{print $1}')
    PORT=$(echo $SSH_CLIENT | awk '{print $3}')
    HOSTNAME=$(hostname -f)
    IPADDR=$(echo $SSH_CONNECTION | awk '{print $3}')

    # Get user's access info from ipinfo.io
    curl http://ipinfo.io/$IP -s -o $TMPFILE
    CITY=$(cat $TMPFILE | jq '.city' | sed 's/"//g')
    REGION=$(cat $TMPFILE | jq '.region' | sed 's/"//g')
    COUNTRY=$(cat $TMPFILE | jq '.country' | sed 's/"//g')
    ORG=$(cat $TMPFILE | jq '.org' | sed 's/"//g')

    # Content Alert
    TEXT=$(echo -e "SSH => Alert\nDate $DATE_EXEC\nUser: ${USER} \nLogged in to STAGING"_"$HOSTNAME"_"$IPADDR \nFrom $IP - $ORG - $CITY, $REGION, $COUNTRY on port $PORT")

    # Send Alert
    curl -s -X POST --max-time $TIMEOUT $URL -d "chat_id=$USERID" -d text="$TEXT" > /dev/null

    # Delete $TMPFILE after script done
    rm $TMPFILE
fi