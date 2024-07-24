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

function flinkUsage(){
  echo "Usage: flink.sh <jobmanager|taskmanager|initFlinkDir|initLinks> <start|stop|restart|enable|disable|status|logs> [log|out]"
}

function flinkOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi

  FLINK_HOME=/usr/lib/flink
  HOSTNAME=$(hostname -f)

  if [ $1 = "jobmanager" ]; then
    if [ $2 = "start" ]; then
      echo "Starting Flink Job Manager"
      sudo systemctl start flink-jobmanager
      echo $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Flink Job Manager"
      sudo systemctl stop flink-jobmanager
      echo $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Flink Job Manager"
      sudo systemctl restart flink-jobmanager
      echo $?
    elif [ $2 = "enable" ]; then
      echo "Enabling Flink Job Manager"
      sudo systemctl enable flink-jobmanager
      echo $?
    elif [ $2 = "disable" ]; then
      echo "Disabling Flink Job Manager"
      sudo systemctl disable flink-jobmanager
      echo $?
    elif [ $2 = "status" ]; then
      echo "Checking Flink Job Manager status"
      sudo systemctl status flink-jobmanager
      echo $?
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Showing Flink Job Manager logs"
        sudo -u flink tail -n 200 /var/log/flink/flink-flink-standalonesession-0-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Showing Flink Job Manager output"
        sudo -u flink tail -n 200 /var/log/flink/flink-jobmanager.out
      else
        flinkUsage
      fi
    else
      flinkUsage
    fi
  elif [ $1 = "taskmanager" ]; then
    if [ $2 = "start" ]; then
      echo "Starting Flink Task Manager"
      sudo systemctl start flink-taskmanager
      echo $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Flink Task Manager"
      sudo systemctl stop flink-taskmanager
      echo $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Flink Task Manager"
      sudo systemctl restart flink-taskmanager
      echo $?
    elif [ $2 = "enable" ]; then
      echo "Enabling Flink Task Manager"
      sudo systemctl enable flink-taskmanager
      echo $?
    elif [ $2 = "disable" ]; then
      echo "Disabling Flink Task Manager"
      sudo systemctl disable flink-taskmanager
      echo $?
    elif [ $2 = "status" ]; then
      echo "Checking Flink Task Manager status"
      sudo systemctl status flink-taskmanager
      echo $?
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Showing Flink Task Manager logs"
        sudo -u flink tail -n 200 /var/log/flink/flink-flink-taskexecutor-0-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Showing Flink Task Manager output"
        sudo -u flink tail -n 200 /var/log/flink/flink-taskmanager.out
      else
        flinkUsage
      fi
    else
      flinkUsage
    fi
  elif [ $1 = "initFlinkDir" ]; then
    echo "Create flink HDFS dirs"
    sudo -u hdfs hdfs dfs -mkdir -p /user/flink/ha
    sudo -u hdfs hdfs dfs -chown -R flink:flink /user/flink
    sudo -u hdfs hdfs dfs -chmod -R 777 /user/flink/ha
  elif [ $1 = "initLinks" ]; then
    sudo ln -sf /usr/lib/hadoop/lib/* /usr/lib/flink/lib/
    sudo ln -sf /usr/lib/hadoop-hdfs/* /usr/lib/flink/lib/
    sudo ln -sf /usr/lib/hadoop-yarn/* /usr/lib/flink/lib/
    sudo ln -sf /usr/lib/hadoop-mapreduce/* /usr/lib/flink/lib/
    sudo ln -sf /usr/lib/hadoop-kms/* /usr/lib/flink/lib/
    sudo ln -sf /etc/hadoop/conf/* /etc/flink/conf/
  else
    flinkUsage
  fi
}



