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

function hbaseOperation()
{
  if [ $1 = 'master' ]; then
    if [ $2 = 'initHBaseHDFSDir' ]; then
      echo "Make /hbase on hdfs"
      sudo -u hdfs hdfs dfs -mkdir /hbase
      echo "Chown /hbase on hdfs to hbase:hbase"
      sudo -u hdfs hdfs dfs -chown hbase:hbase /hbase
    elif [ $2 = 'start' ]; then
      echo 'start hbase master'
      systemctl start hbase-master
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-master service'
      systemctl enable hbase-master
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-master service'
      systemctl disable hbase-master
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase master'
      systemctl stop hbase-master
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase master'
      systemctl restart hbase-master
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'regionserver' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase regionserver'
      systemctl start hbase-regionserver
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-regionserver service'
      systemctl enable hbase-regionserver
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-regionserver service'
      systemctl disable hbase-regionserver
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase regionserver'
      systemctl stop hbase-regionserver
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase regionserver'
      systemctl restart hbase-regionserver
    else
      echo "Invalid command"
    fi
  else
    echo "Invalid command"
  fi
}
