#!/bin/bash
echo $(date) - "$@" >> /tmp/octo-log
CONF_FILE=$HOME/.octo.conf
if [ ! -f "$CONF_FILE" ];
then
    echo OCTO_API_KEY=$(OctoPrint/venv/bin/octoprint config get api.key | tr -d "'") > $CONF_FILE
    echo OCTO_PORT=$(OctoPrint/venv/bin/octoprint config get server.port | tr -d "'") >> $CONF_FILE
    echo OCTO_HOST=$(OctoPrint/venv/bin/octoprint config get server.host | tr -d "'") >> $CONF_FILE
    echo 'Retrieved API key'
fi
source $CONF_FILE

function send_octo() {
        curl -H "X-Api-Key: $OCTO_API_KEY" -H 'Content-Type: application/json' --data "$1" http://$OCTO_HOST:$OCTO_PORT/api/printer/printhead
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
  nothing)
    echo "nothing $(date)" >> /tmp/prueba
          ;;
esac