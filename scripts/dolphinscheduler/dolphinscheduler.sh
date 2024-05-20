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
  CONNECTOR_JAR_STATUS=$(rpm -qa | grep mysql-connector-j; echo $?)
  if [ $1 = 'master' ];then
    if [ $2 = 'initDatabase' ]; then
      MYSQL_USER=$3
      MYSQL_PASSWORD=$4
      MYSQL_DB=dolphinscheduler
      echo "init database"
      echo "Install mysql client and jdbc driver"
      if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
        sudo yum -y install mysql-connector-j mysql --verbose
      fi
      echo "Link mysql jdbc driver to /usr/lib/dolphinscheduler/lib/mysql-connector-java.jar"
      if [ -L /usr/lib/dolphinscheduler/master-server/libs/mysql-connector-java.jar ]; then
        sudo rm -f /usr/lib/dolphinscheduler/master-server/libs/mysql-connector-java.jar
      fi
      sudo ln -sf /usr/share/java/mysql-connector-j.jar /usr/lib/dolphinscheduler/master-server/libs/mysql-connector-java.jar
      echo "Create database"
      sudo mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB"
      echo "Create user and grant privileges"
      sudo mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e "CREATE USER IF NOT EXISTS 'dolphinscheduler'@'%' IDENTIFIED BY 'dolphinscheduler';"
      sudo mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e "GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO 'dolphinscheduler'@'%';"
      sudo mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e "FLUSH PRIVILEGES;"
      sudo mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DB < /usr/lib/dolphinscheduler/tools/sql/sql/dolphinscheduler_mysql.sql
    elif [ $2 = 'start' ]; then
      sudo mkdir -p /dolphinscheduler
      OWNER=$(stat -c %U:%G /dolphinscheduler)
      if [ $OWNER != "dolphinscheduler:dolphinscheduler" ]; then
        chown -R dolphinscheduler:dolphinscheduler /dolphinscheduler
      fi
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
      sudo mkdir -p /dolphinscheduler
      if [ $OWNER != "dolphinscheduler:dolphinscheduler" ]; then
        chown -R dolphinscheduler:dolphinscheduler /dolphinscheduler
      fi
      sudo systemctl start dolphinscheduler-worker
    elif [ $2 = "jdbc" ]; then
      if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
        sudo yum -y install mysql-connector-j mysql --verbose
      fi
      if [ -L /usr/lib/dolphinscheduler/worker-server/libs/mysql-connector-java.jar ]; then
        sudo rm -f /usr/lib/dolphinscheduler/worker-server/libs/mysql-connector-java.jar
      fi
      sudo ln -sf /usr/share/java/mysql-connector-java.jar /usr/lib/dolphinscheduler/worker-server/libs/mysql-connector-java.jar
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
      sudo mkdir -p /dolphinscheduler
      if [ $OWNER != "dolphinscheduler:dolphinscheduler" ]; then
        chown -R dolphinscheduler:dolphinscheduler /dolphinscheduler
      fi
      sudo systemctl start dolphinscheduler-api
    elif [ $2 = "jdbc" ]; then
      if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
        sudo yum -y install mysql-connector-j mysql --verbose
      fi
      if [ -L /usr/lib/dolphinscheduler/api-server/libs/mysql-connector-java.jar ]; then
        sudo rm -f /usr/lib/dolphinscheduler/api-server/libs/mysql-connector-java.jar
      fi
      sudo ln -sf /usr/share/java/mysql-connector-java.jar /usr/lib/dolphinscheduler/api-server/libs/mysql-connector-java.jar
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
      mkdir -p /dolphinscheduler
      if [ $OWNER != "dolphinscheduler:dolphinscheduler" ]; then
        chown -R dolphinscheduler:dolphinscheduler /dolphinscheduler
      fi
      sudo systemctl start dolphinscheduler-alert
    elif [ $2 = "jdbc" ]; then
      if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
        sudo yum -y install mysql-connector-j mysql --verbose
      fi
      if [ -L /usr/lib/dolphinscheduler/alert-server/libs/mysql-connector-java.jar ]; then
        sudo rm -f /usr/lib/dolphinscheduler/alert-server/libs/mysql-connector-java.jar
      fi
      sudo ln -sf /usr/share/java/mysql-connector-java.jar /usr/lib/dolphinscheduler/alert-server/libs/mysql-connector-java.jar
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
      sudo mkdir -p /dolphinscheduler
      if [ $OWNER != "dolphinscheduler:dolphinscheduler" ]; then
        chown -R dolphinscheduler:dolphinscheduler /dolphinscheduler
      fi
      sudo systemctl start dolphinscheduler-standalone
    elif [ $2 = "jdbc" ]; then
      if [ $CONNECTOR_JAR_STATUS -ne 0 ]; then
        sudo yum -y install mysql-connector-j mysql --verbose
      fi
      if [ -L /usr/lib/dolphinscheduler/standalone-server/libs/mysql-connector-java.jar ]; then
        sudo rm -f /usr/lib/dolphinscheduler/standalone-server/libs/mysql-connector-java.jar
      fi
      sudo ln -sf /usr/share/java/mysql-connector-java.jar /usr/lib/dolphinscheduler/standalone-server/libs/mysql-connector-java.jar
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
