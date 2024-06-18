#!/bin/sh
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# privoxy_config.sh - Lógica necesaria para configurar los servicios Privoxy


ETCBASE="/etc/privoxy"
LOGBASE="/var/log/privoxy"
SOCKSBASE=9050
LISTENBASE=3128 # Asignamos el 3128 del HAProxy, y se darán los valores sucesivos
N_INSTANCES=2
for INSTANCE in 1 2
do

    CONFDIR="$ETCBASE$INSTANCE"
    LOGDIR="$LOGBASE$INSTANCE"
    CONF="$CONFDIR/config"
    SOCKS_PORT=$((SOCKSBASE+INSTANCE))
    LISTEN_PORT=$((LISTENBASE+INSTANCE))
    echo "Configuring instance $INSTANCE with $SOCKS_PORT socks port listening on $LISTEN_PORT"
    SERVICE_FILE="/etc/systemd/system/privoxy$INSTANCE.service"
    mkdir -p $CONFDIR
    mkdir -p $LOGDIR
    chown privoxy $LOGDIR
    chgrp adm $LOGDIR
    chown privoxy $CONFDIR
    chgrp adm $CONFDIR
    # Privoxy utilizará el puerto $SOCKS_PORT del anfitrión local (localhost) como servidor socks versión 5 (Según la doc: Es decir, el servicio Tor en el anfitrión local)
    echo "forward-socks5t   /               127.0.0.1:$SOCKS_PORT ." > $CONF
    echo "logdir $LOGDIR" >> $CONF
    # Privoxy escuchará unicamente peticiones de anfitrión local (localhost), por los puertos $LISTEN_PORT
    echo "listen-address  127.0.0.1:$LISTEN_PORT" >> $CONF
    cat /home/vagrant/Desktop/tor-scraper-classifier/config/privoxy.config.default >> $CONF

cat << EOF > $SERVICE_FILE
[Unit]
Description=Privacy enhancing HTTP Proxy

[Service]
Environment=PIDFILE=/var/run/privoxy$INSTANCE.pid
Environment=OWNER=privoxy
Environment=CONFIGFILE=$CONF
Type=forking
PIDFile=/var/run/privoxy$INSTANCE.pid
ExecStart=/usr/sbin/privoxy --pidfile \$PIDFILE --user \$OWNER \$CONFIGFILE
ExecStopPost=/bin/rm -f \$PIDFILE
SuccessExitStatus=15

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl stop privoxy$INSTANCE.service
    systemctl start privoxy$INSTANCE.service
done

