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

function yarnUsage() {
  echo "Usage: yarn.sh [resourcemanager|nodemanager|jobhistory] [logs|mkdir|format|start|stop|restart|mkhdfsdirs]"
}

:<<!
# yarn.sh resourcemanager start | stop | restart
# yarn.sh resourcemanager logs log | out
# yarn.sh nodemanager start | stop | restart
# yarn.sh nodemanager logs log | out
# yarn.sh jobhistory start | stop | restart
# yarn.sh jobhistory logs out
!

function yarnOperation() {
  echo "Initializing YARN"
      # Create the yarn directory
      # yarn.sh nodemanager mkdir $dirs(comma seperated)
      # yarn.sh jobhistory mkdir $dirs(comma seperated)
  TMP=$3
  DIRS=${TMP//,/ }
  if [ $1 = "nodemanager" ]; then
    if [ $2 = "mkdirs" ]; then
      echo "Initializing NodeManager"
      for DIR in $DIRS
      do
        echo "Creating $DIR"
        mkdir -p $DIR
        chown -R yarn:yarn $DIR
      done
    elif [ $2 = "start" ]; then
      echo "Starting NodeManager"
      sudo systemctl start hadoop-yarn-nodemanager
    elif [ $2 = "stop" ]; then
      echo "Stopping NodeManager"
      sudo systemctl stop hadoop-yarn-nodemanager
    elif [ $2 = "restart" ]; then
      echo "Restarting NodeManager"
      sudo systemctl restart hadoop-yarn-nodemanager
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing NodeManager log"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-nodemanager-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Tailing NodeManager out"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-nodemanager-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid command"
    fi
  elif [ $1 = "resourcemanager" ]; then
    if [ $2 = "start" ]; then
      echo "Starting ResourceManager"
      sudo systemctl start hadoop-yarn-resourcemanager
    elif [ $2 = "stop" ]; then
      echo "Stopping ResourceManager"
      sudo systemctl stop hadoop-yarn-resourcemanager
    elif [ $2 = "restart" ]; then
      echo "Restarting ResourceManager"
      sudo systemctl restart hadoop-yarn-resourcemanager
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing ResourceManager log"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-resourcemanager-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Tailing ResourceManager out"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-resourcemanager-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid command"
    fi
  elif [ $1 = "jobhistory" ]; then
    if [ $2 = "start" ]; then
      sudo systemctl start hadoop-mapreduce-historyserver
    elif [ $2 = "stop" ]; then
      sudo systemctl stop hadoop-mapreduce-historyserver
    elif [ $2 = "restart" ]; then
      sudo systemctl restart hadoop-mapreduce-historyserver
    elif [ $2 = "logs" ]; then
      if [ $3 = "out" ]; then
        echo "Tailing JobHistory out"
        sudo -u mapred tail -n 200 /var/log/hadoop-mapreduce/mapred-mapred-historyserver-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid command"
    fi
  else
    echo "Invalid command"
  fi
}

yarnOperation $1 $2 $3
