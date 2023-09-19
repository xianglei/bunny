#!/bin/bash

if [ $JAVA_HOME ]; then
  echo "JAVA_HOME is set to $JAVA_HOME"
  if [ -z "$JAVA_HOME" ]; then
    echo "JAVA_HOME is null"
    export JAVA_HOME=/usr/java/default
  else
    echo "JAVA_HOME is set"
    export PATH=$PATH:$JAVA_HOME/bin
    export JAVA_HOME=$JAVA_HOME
    if [ -e "$JAVA_HOME/bin/java" ]; then
      echo "JAVA_HOME ok"
    else
      echo "JAVA_HOME not ok"
      exit 1
    fi
  fi
else
  echo "JAVA_HOME is not set"
  exit 1
fi

function tailZookeeper() {
  echo "Tailing Zookeeper"
  # Tail Zookeeper
  sudo -u zookeeper tail -n 200 /var/log/zookeeper/zookeeper.log
}

function initZookeeper() {
  echo "Initializing Zookeeper"
  # Create the data directory
  # zookeeper.sh init [1|2|3]
  mkdir -p /var/lib/zookeeper/data
  chown -R zookeeper:zookeeper /var/lib/zookeeper/data
  if [ -f /var/lib/zookeeper/myid ]; then
    echo "Zookeeper already initialized"
    exit 1
  else
    sudo -u zookeeper zookeeper-server-initialize --myid=$1 --force --verbose
    exit 0
  fi
}

function startZookeeper() {
  echo "Starting Zookeeper"
  # Start Zookeeper
  sudo -u systemctl start zookeeper
}

function stopZookeeper() {
  echo "Stopping Zookeeper"
  # Stop Zookeeper
  sudo -u systemctl stop zookeeper
}

function restartZookeeper() {
  echo "Restarting Zookeeper"
  # Restart Zookeeper
  sudo -u systemctl restart zookeeper
}

if [ $1 = "init" ]; then
  NUM=$2
  initZookeeper ${NUM}
elif [ $1 = "start" ]; then
  startZookeeper
elif [ $1 == "stop" ]; then
  stopZookeeper
elif [ $1 == "restart" ]; then
  restartZookeeper
else
  echo "Invalid command"
  exit 1
fi
