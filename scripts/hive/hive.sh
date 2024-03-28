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

HOSTNAME=$(hostname -f)
ROLE=$1

# hive.sh initSchema mysql
# hive.sh metastore start
# hive.sh metastore stop
# hive.sh metastore status
# hive.sh server2 start
# hive.sh server2 stop
# hive.sh server2 status

function hiveUsage() {
  echo "Usage: hive.sh {metastore|server|server2|webhcat|hwi|initSchema} {start|stop|status|mysql}"
  exit 1
}

function hiveOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = "metastore" ]; then
    if [ $2 = "start" ]; then
      #sudo -u hive HADOOP_HOME=${HADOOP_HOME} JAVA_HOME=${JAVA_HOME} ${HIVE_HOME}/bin/hive --service metastore > /var/log/hive/hive-metastore.log 2>&1 &
      sudo systemctl start hive-metastore
    elif [ $2 = "stop" ]; then
      #sudo -u hive pkill -f org.apache.hadoop.hive.metastore.HiveMetaStore
      sudo systemctl stop hive-metastore
    elif [ $2 = "status" ]; then
      #sudo -u hive jps | grep HiveMetaStore
      sudo systemctl status hive-metastore
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart hive-metastore
    else
      hiveUsage
    fi
  elif [ $1 = "server2" ]; then
    if [ $2 = "start" ]; then
      #sudo -u hive HADOOP_HOME=${HADOOP_HOME} JAVA_HOME=${JAVA_HOME} ${HIVE_HOME}/bin/hive --service hiveserver2 > /var/log/hive/hive-server2.log 2>&1 &
      sudo systemctl start hive-server2
    elif [ $2 = "stop" ]; then
      #sudo -u hive pkill -f org.apache.hive.service.server.HiveServer2
      sudo systemctl stop hive-server2
    elif [ $2 = "status" ]; then
      #sudo -u hive jps | grep HiveServer2
      sudo systemctl status hive-server2
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart hive-server2
    else
      hiveUsage
    fi
  elif [ $1 = "webhcat-server" ]; then
    if [ $2 = "start" ]; then
      #sudo -u hive HADOOP_HOME=${HADOOP_HOME} JAVA_HOME=${JAVA_HOME} ${HIVE_HOME}/bin/hive --service webhcat > /var/log/hive/hive-webhcat.log 2>&1 &
      sudo systemctl start hive-webhcat-server
    elif [ $2 = "stop" ]; then
      #sudo -u hive pkill -f org.apache.hive.service.server.HiveServer2
      sudo systemctl stop hive-webhcat-server
    elif [ $2 = "status" ]; then
      #sudo -u hive jps | grep HiveServer2
      sudo systemctl status hive-webhcat-server
    elif [ $2 = 'restart' ]; then
      sudo systemctl restart hive-webhcat-server
    else
      hiveUsage
    fi
  elif [ $1 = "initSchema" ]; then
    sudo -u hdfs hdfs dfs -mkdir -p /user/hive/warehouse
    sudo -u hdfs hdfs dfs -chown -R hive:hive /user/hive
    sudo -u hdfs hdfs dfs -chmod -R 0777 /user/hive/warehouse
    if [ $2 = "mysql" ]; then
      #sudo -u hive HADOOP_HOME=${HADOOP_HOME} JAVA_HOME=${JAVA_HOME} ${HIVE_HOME}/bin/hive --service schematool -initSchema -dbType derby
      if [ -f /usr/share/java/mysql-connector-j.jar ]; then
        sudo ln -sf /usr/share/java/mysql-connector-j.jar /usr/lib/hive/lib/mysql-connector-java.jar
      else
        echo "mysql-connector-j.jar not found, install mysql-connector-java package first"
        exit 1
      fi
      sudo -u hive /usr/lib/hive/bin/schematool -initSchema -dbType mysql
    else
      hiveUsage
    fi
  else
    echo "Invalid role: $1"
    hiveUsage
  fi
}

if [ -z "$ROLE" ]; then
  hiveUsage
else
  hiveOperation $1 $2
fi
