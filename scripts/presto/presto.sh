#!/usr/bin/env bash

JAVA8_HOME_CANDIDATES=(
    '/usr/java/jdk1.8'
    '/usr/java/jre1.8'
    '/usr/lib/jvm/j2sdk1.8-oracle'
    '/usr/lib/jvm/j2sdk1.8-oracle/jre'
    '/usr/lib/jvm/java-8-oracle'
    '/usr/lib/jdk8-latest'
    '/usr/lib/jvm/java-1.8.0'
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


function prestoOperation(){
    echo "Presto operation"
    if [ -z "${JAVA_HOME}" ]; then
      echo "JAVA_HOME is not set, script will not work"
      exit 1
    fi
    if [ $1 = "master" ]; then
      if [ $2 = "start" ]; then
        echo "Starting Presto master"
        sudo systemctl start presto-master
        exit $?
      elif [ $2 = "stop" ]; then
        echo "Stopping Presto master"
        sudo systemctl stop presto-master
        exit $?
      elif [ $2 = "restart" ]; then
        echo "Restarting Presto master"
        sudo systemctl restart presto-master
        exit $?
      elif [ $2 = "status" ]; then
        echo "Checking Presto master status"
        sudo systemctl status presto-master
        exit $?
      elif [ $2 = "enable" ]; then
        echo "Enabling Presto master"
        sudo systemctl enable presto-master
        exit $?
      elif [ $2 = "disable" ]; then
        echo "Disabling Presto master"
        sudo systemctl disable presto-master
        exit $?
      else
        echo "Invalid operation"
      fi
    elif [ $1 = "worker" ]; then
      if [ $2 = "start" ]; then
        echo "Starting Presto worker"
        sudo systemctl start presto-worker
        exit $?
      elif [ $2 = "stop" ]; then
        echo "Stopping Presto worker"
        sudo systemctl stop presto-worker
        exit $?
      elif [ $2 = "restart" ]; then
        echo "Restarting Presto worker"
        sudo systemctl restart presto-worker
        exit $?
      elif [ $2 = "status" ]; then
        echo "Checking Presto worker status"
        sudo systemctl status presto-worker
        exit $?
      elif [ $2 = "enable" ]; then
        echo "Enabling Presto worker"
        sudo systemctl enable presto-worker
        exit $?
      elif [ $2 = "disable" ]; then
        echo "Disabling Presto worker"
        sudo systemctl disable presto-worker
        exit $?
      else
        echo "Invalid operation"
      fi
    elif [ $1 = "mkdir" ]; then
      echo "Creating directory"
      sudo mkdir -p $2
      sudo chown -R presto:presto $2
      exit $?
    elif [ $1 = "rmdir" ]; then
      echo "Removing directory"
      sudo rm -rf $2
      exit $?
    else
        echo "Invalid operation"
    fi
}


prestoOperation $1 $2


