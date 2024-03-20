#!/bin/bash

JAVA8_HOME_CANDIDATES=(
    '/usr/java/jdk1.8'
    '/usr/java/jre1.8'
    '/usr/lib/jvm/j2sdk1.8-oracle'
    '/usr/lib/jvm/j2sdk1.8-oracle/jre'
    '/usr/lib/jvm/java-8-oracle'
    '/usr/lib/jdk8-latest'
    '/usr/lib/jvm/java-1.8.0'
    '/usr/lib/jvm/java-1.8.0-oracle'
)

OPENJAVA8_HOME_CANDIDATES=(
    '/usr/lib/jvm/java-1.8.0-openjdk-amd64'
    '/usr/lib/jvm/java-1.8.0-openjdk-ppc64el'
    '/usr/lib/jvm/java-1.8.0-openjdk'
    '/usr/lib64/jvm/java-1.8.0-openjdk-1.8.0'
    '/usr/lib/jvm/adoptopenjdk-8-hotspot'
)

MISCJAVA_HOME_CANDIDATES=(
    '/Library/Java/Home'
    '/usr/java/default'
    '/usr/lib/jvm/java'
    '/usr/lib/jvm/jre'
    '/usr/lib/jvm/default-java'
    '/usr/lib/jvm/java-openjdk'
    '/usr/lib/jvm/jre-openjdk'
    '/usr/lib/jvm/java-oracle'
)

case ${BIGTOP_JAVA_MAJOR} in
  6|7) echo "Java ${BIGTOP_JAVA_MAJOR} is no longer supported. Please upgrade"
     exit 1
     ;;
  8) JAVA_HOME_CANDIDATES=(${JAVA8_HOME_CANDIDATES[@]} ${OPENJAVA8_HOME_CANDIDATES[@]})
     ;;
  *) JAVA_HOME_CANDIDATES=(${JAVA8_HOME_CANDIDATES[@]}
                           ${MISCJAVA_HOME_CANDIDATES[@]}
                           ${OPENJAVA8_HOME_CANDIDATES[@]})
     ;;
esac

# attempt to find java
if [ -z "${JAVA_HOME}" ]; then
  for candidate_regex in ${JAVA_HOME_CANDIDATES[@]} ; do
      for candidate in `ls -rvd ${candidate_regex}* 2>/dev/null`; do
        if [ -e ${candidate}/bin/java ]; then
          export JAVA_HOME=${candidate}
          break 2
        fi
      done
  done
fi

function tailZookeeper() {
  echo "Tailing Zookeeper"
  # Tail Zookeeper
  sudo -u zookeeper tail -n 200 /var/log/zookeeper/zookeeper.log
}

function initZookeeper() {
  echo "Initializing Zookeeper"
  # Create the data directory
  # zookeeper.sh init [1|2|3] [dataDir]
  sudo mkdir -p $2/data
  sudo chown -R zookeeper:zookeeper $2/data
  if [ -f $2/myid ]; then
    echo "Zookeeper already initialized"
    exit 1
  else
    sudo -u zookeeper zookeeper-server-initialize --myid=$1 --force
    exit 0
  fi
}

function startZookeeper() {
  echo "Starting Zookeeper"
  # Start Zookeeper
  sudo systemctl start zookeeper-server
}

function stopZookeeper() {
  echo "Stopping Zookeeper"
  # Stop Zookeeper
  sudo systemctl stop zookeeper-server
}

function restartZookeeper() {
  echo "Restarting Zookeeper"
  # Restart Zookeeper
  sudo systemctl restart zookeeper-server
}

function enableZookeeper() {
  echo 'enable zookeeper'
  sudo systemctl enable zookeeper-server
}

function disableZookeeper() {
  echo 'enable zookeeper'
  sudo systemctl disable zookeeper-server
}

#if [ -z $1 ]; then
  if [ $1 = "init" ]; then
    NUM=$2
    dataDir=$3
    initZookeeper ${NUM} ${dataDir}
  elif [ $1 = "start" ]; then
    startZookeeper
  elif [ $1 == "stop" ]; then
    stopZookeeper
  elif [ $1 == "restart" ]; then
    restartZookeeper
  elif [ $1 = 'enable' ]; then
    enableZookeeper
  elif [ $1 = 'disable' ]; then
    disableZookeeper
  else
    echo "Invalid command"
    exit 1
  fi
#else
#  echo "zookeeper.sh [init|start|stop|restart|enable|disable] [1|2|3] [dataDir(init only)]"
#fi
