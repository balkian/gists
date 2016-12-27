#!/bin/bash
# Starting Octoprint's CLI takes **very long**.
# So long that it's useless for LIRC (remote) control.
# This script uses the CLI only once, to retrieve the API.
# It's a bit hacky, but it works for LIRC (infrared remote)
KEY_FILE=$HOME/.octokey
if [ ! -f "$KEY_FILE" ];
then
    OctoPrint/venv/bin/octoprint config get api.key | tr -d "'" > $KEY_FILE
    echo 'Retrieved API key'
fi
OCTO_API_KEY=$(cat $KEY_FILE)

function send_octo() {
        curl -H "X-Api-Key: $OCTO_API_KEY" -H 'Content-Type: application/json' --data "$1" http://localhost:5000/api/printer/printhead
}

case $1 in
  move)
    shift
    x=$1
    y=$2
    z=$3
    echo $1 $2 $3
    send_octo '{"command": "jog","x": '$x',"y": '$y',"z": '$z'}' http://localhost:5000/api/printer/printhead
    sleep 2
            ;;
  home)
    send_octo '{ "command": "home", "axes": ["x", "y", "z"] }'
;;
esac