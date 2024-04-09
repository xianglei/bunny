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

function dolphinUsage() {
    echo "Usage: $0 {master|worker|api|alert|standalone} {start|stop|status|restart|initDatabase}"
    exit 1
}

function dolphinOperation() {
  if [ $1 = 'master' ];then
    if [ $2 = 'initDatabase' ]; then
      echo "init database"
      sudo ln -sf /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/lib/mysql-connector-java.jar
      sudo /usr/lib/dolphinscheduler/script/create-dolphinscheduler.sh
    elif [ $2 = 'start' ]; then
      sudo systemctl start dolphinscheduler-master
    elif [ $2 = 'stop' ]; then
      sudo systemctl stop dolphinscheduler-master
    elif [ $2 = 'status' ]; then
      sudo systemctl status dolphinscheduler-master
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart dolphinscheduler-master
    else
      dolphinUsage
    fi
  elif [ $1 = 'worker' ]; then
    if [ $2 = 'start' ]; then
      sudo systemctl start dolphinscheduler-worker
    elif [ $2 = 'stop' ]; then
      sudo systemctl stop dolphinscheduler-worker
    elif [ $2 = 'status' ]; then
      sudo systemctl status dolphinscheduler-worker
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart dolphinscheduler-worker
    else
      dolphinUsage
    fi
  elif [ $1 = 'api' ]; then
    if [ $2 = 'start' ]; then
      sudo systemctl start dolphinscheduler-api
    elif [ $2 = 'stop' ]; then
      sudo systemctl stop dolphinscheduler-api
    elif [ $2 = 'status' ]; then
      sudo systemctl status dolphinscheduler-api
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart dolphinscheduler-api
    else
      dolphinUsage
    fi
  elif [ $1 = 'alert' ]; then
    if [ $2 = 'start' ]; then
      sudo systemctl start dolphinscheduler-alert
    elif [ $2 = 'stop' ]; then
      sudo systemctl stop dolphinscheduler-alert
    elif [ $2 = 'status' ]; then
      sudo systemctl status dolphinscheduler-alert
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart dolphinscheduler-alert
    else
      dolphinUsage
    fi
  elif [ $1 = 'standalone' ]; then
    if [ $2 = 'start' ]; then
      sudo systemctl start dolphinscheduler-standalone
    elif [ $2 = 'stop' ]; then
      sudo systemctl stop dolphinscheduler-standalone
    elif [ $2 = 'status' ]; then
      sudo systemctl status dolphinscheduler-standalone
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart dolphinscheduler-standalone
    else
      dolphinUsage
    fi
  else
    dolphinUsage
  fi
}
