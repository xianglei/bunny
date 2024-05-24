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

function kylinUsage() {
    echo "Usage: $0 {start|stop|status|restart|init}"
    exit 1
}

function kylinOperation() {
  CONNECTOR_JAR_STATUS=$(rpm -qa | grep mysql-connector-j > /dev/null; echo $?)
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = 'init' ]; then
    echo "init kylin"
    sudo -u hdfs hadoop fs -mkdir -p /user/kylin/cube
    sudo -u hdfs hadoop fs -mkdir -p /user/kylin/spark-history
    sudo -u hdfs hadoop fs -chown -R kylin:kylin /user/kylin
    if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
      sudo yum -y install mysql-connector-j mysql --verbose
    fi
    echo "Link mysql jdbc driver to /usr/lib/kylin/lib/mysql-connector-java.jar"
    if [ -L /usr/lib/kylin/lib/mysql-connector-java.jar ]; then
      sudo rm -f /usr/lib/kylin/lib/mysql-connector-java.jar
    fi
    sudo ln -sf /usr/share/java/mysql-connector-j.jar /usr/lib/kylin/lib/mysql-connector-java.jar
    echo "Link spark jdbc driver to /usr/lib/kylin/"
    if [ -L /usr/lib/kylin/spark ]; then
      sudo rm -f /usr/lib/kylin/spark
    fi
    sudo ln -sf /usr/lib/spark /usr/lib/kylin
  elif [ $1 = 'start' ]; then
    sudo systemctl start kylin
    exit $?
  elif [ $1 = 'stop' ]; then
    sudo systemctl stop kylin
    exit $?
  elif [ $1 = 'status' ]; then
    sudo systemctl status kylin
    exit $?
  elif [ $1 = 'restart' ]; then
    sudo systemctl restart kylin
    exit $?
  elif [ $1 = 'enable' ]; then
    sudo systemctl enable kylin
    exit $?
  elif [ $1 = 'disable' ]; then
    sudo systemctl disable kylin
    exit $?
  else
    kylinUsage
  fi
}

if [ -z $1 ]; then
  kylinUsage
  exit 1
else
  kylinOperation $1
fi
