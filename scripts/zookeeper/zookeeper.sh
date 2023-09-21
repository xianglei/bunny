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
  # zookeeper.sh init [1|2|3]
  sudo mkdir -p /var/lib/zookeeper/data
  sudo chown -R zookeeper:zookeeper /var/lib/zookeeper/data
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
