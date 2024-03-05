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

function sparkOperation() {
  if [ $1 = "historyserver" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark History Server"
      sudo systemctl start spark-history-server
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark History Server"
      sudo systemctl stop spark-history-server
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark History Server"
      sudo systemctl restart spark-history-server
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-history-server
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-history-server
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-history-server.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-history-server.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = "status" ]; then
      sudo -u spark /usr/lib/spark/sbin/spark-daemon.sh status org.apache.spark.deploy.history.HistoryServer 1
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "yarnshuffle" ]; then
    if [ -f /usr/lib/hadoop-yarn/lib/spark-yarn-shuffle.jar ]; then
      echo "Spark Yarn Shuffle jar already exists"
    else
      echo "Copying Spark Yarn Shuffle jar"
      sudo cp /usr/lib/spark/yarn/lib/spark-yarn-shuffle.jar /usr/lib/hadoop-yarn/lib/
    fi
  elif [ $1 = "master" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark master"
      sudo systemctl start spark-master
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark master"
      sudo systemctl stop spark-master
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark master"
      sudo systemctl restart spark-master
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-master
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-master
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-master
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-master.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-master.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "worker" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark worker"
      sudo systemctl start spark-worker
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark worker"
      sudo systemctl stop spark-worker
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark worker"
      sudo systemctl restart spark-worker
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-worker
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-worker
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-worker
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-worker.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-worker.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "thriftserver" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark thriftserver"
      sudo systemctl start spark-thriftserver
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark thriftserver"
      sudo systemctl stop spark-thriftserver
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark thriftserver"
      sudo systemctl restart spark-thriftserver
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-thriftserver
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-thriftserver
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-thriftserver
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-thriftserver.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-thriftserver.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  else
    echo "Invalid operation"
  fi
}

function sparkUsage() {
  echo "Usage: spark.sh [master|worker|thrift|historyserver|yarnshuffle] [start|stop|restart|enable|disable]"
}

if [ -z $1 ]; then
  sparkUsage
  exit 1
else
  sparkOperation $1 $2 $3
fi
