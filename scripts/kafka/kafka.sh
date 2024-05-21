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
    '/usr/lib/jvm/java-1.8.0-oracle'
    '/usr/lib/jvm/jdk-1.8-oracle-aarch64'
    '/usr/lib/jvm/jdk-1.8-oracle-x64'
    '/usr/lib/jvm/jdk-1.8-oracle-x86'
    '/usr/lib/jvm/jdk-1.8-oracle'
    '/usr/java/latest'
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

function kafkaUsage() {
    echo "Usage: kafka.sh {mkdir|server} dirs(comma seperated) {start|stop|status}"
    exit 1
}

function kafkaOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = "mkdir" ];then
    TMP=$2
    DIRS=${TMP//,/ }
    echo "Creating Kafka data directory"
    for DIR in $DIRS
    do
      sudo echo "Creating directory $DIR"
      sudo mkdir -p $DIR
      sudo chown -R kafka:kafka $DIR
    done
    echo "Create kafka hdfs directory"
    sudo -u hdfs hadoop fs -mkdir -p /user/kafka
    sudo -u hdfs hadoop fs -chown -R kafka:kafka /user/kafka
    exit $?
  elif [ $1 = "server" ];then
    if [ $2 = "start" ]; then
        echo "Starting Kafka"
        sudo systemctl start kafka-server
    elif [ $2 = "stop" ]; then
        echo "Stopping Kafka"
        sudo systemctl stop kafka-server
    elif [ $2 = "status" ]; then
        echo "Status of Kafka"
        sudo systemctl status kafka-server
    elif [ $2 = 'restart' ]; then
        echo "Restarting Kafka"
        sudo systemctl restart kafka-server
    else
        kafkaUsage
    fi
  else
    kafkaUsage
  fi
}

if [ -z $1 ]; then
  kafkaUsage
else
  kafkaOperation $1 $2
fi
