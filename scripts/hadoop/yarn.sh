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

HOSTNAME=$(hostname -f)
ROLE=$1

function yarnUsage() {
  echo "Usage: yarn.sh [resourcemanager|nodemanager|jobhistory] [logs|mkdir|format|start|stop|restart|mkhdfsdirs]"
}

# yarn.sh resourcemanager start | stop | restart
# yarn.sh resourcemanager logs log | out
# yarn.sh nodemanager start | stop | restart
# yarn.sh nodemanager logs log | out
# yarn.sh jobhistory start | stop | restart
# yarn.sh jobhistory logs out
# yarn.sh nodemanager mkdir $dirs(comma seperated)
# yarn.sh nodemanager mklogdir $dirs(comma seperated)

function yarnOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  echo "Initializing YARN"
      # Create the yarn directory
      # yarn.sh nodemanager mkdir $dirs(comma seperated)
      # yarn.sh jobhistory mkdir $dir
      # yarn.sh nodemanager mklogdir $dirs(comma seperated)
  TMP=$3
  DIRS=${TMP//,/ }
  if [ $1 = "nodemanager" ]; then
    if [ $2 = "mkdir" ]; then
      echo "Initializing NodeManager"
      for DIR in $DIRS
      do
        echo "Creating $DIR"
        sudo mkdir -p $DIR
        sudo chown -R yarn:hadoop $DIR
      done
    elif [ $2 = 'enable' ]; then
      echo 'enable hadoop-yarn-nodemanager service'
      sudo systemctl enable hadoop-yarn-nodemanager
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hadoop-yarn-nodemanager service'
      sudo systemctl disable hadoop-yarn-nodemanager
      exit $?
    elif [ $2 = "start" ]; then
      echo "Starting NodeManager"
      sudo systemctl start hadoop-yarn-nodemanager
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping NodeManager"
      sudo systemctl stop hadoop-yarn-nodemanager
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting NodeManager"
      sudo systemctl restart hadoop-yarn-nodemanager
      exit $?
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing NodeManager log"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-nodemanager-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Tailing NodeManager out"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-nodemanager-$HOSTNAME.out
      else
        echo "Invalid command"
        exit 1
      fi
    elif [ $2 = "mklogdir" ]; then
      echo "Initializing NodeManager log directory"
      for DIR in $DIRS
      do
        echo "Creating $DIR"
        sudo mkdir -p $DIR
        sudo chown -R yarn:hadoop $DIR
      done
    else
      echo "Invalid command"
      exit 1
    fi
  elif [ $1 = "resourcemanager" ]; then
    if [ $2 = "start" ]; then
      echo "Starting ResourceManager"
      sudo systemctl start hadoop-yarn-resourcemanager
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping ResourceManager"
      sudo systemctl stop hadoop-yarn-resourcemanager
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting ResourceManager"
      sudo systemctl restart hadoop-yarn-resourcemanager
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable hadoop-yarn-resourcemanager service'
      sudo systemctl enable hadoop-yarn-resourcemanager
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hadoop-yarn-resourcemanager service'
      sudo systemctl disable hadoop-yarn-resourcemanager
      exit $?
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing ResourceManager log"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-resourcemanager-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        echo "Tailing ResourceManager out"
        sudo -u yarn tail -n 200 /var/log/hadoop-yarn/yarn-yarn-resourcemanager-$HOSTNAME.out
      else
        echo "Invalid command"
        exit 1
      fi
    else
      echo "Invalid command"
      exit 1
    fi
  elif [ $1 = "jobhistory" ]; then
    if [ $2 = "start" ]; then
      sudo systemctl start hadoop-mapreduce-historyserver
      exit $?
    elif [ $2 = "stop" ]; then
      sudo systemctl stop hadoop-mapreduce-historyserver
      exit $?
    elif [ $2 = "restart" ]; then
      sudo systemctl restart hadoop-mapreduce-historyserver
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable hadoop-mapreduce-historyserver service'
      sudo systemctl enable hadoop-mapreduce-historyserver
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hadoop-mapreduce-historyserver service'
      sudo systemctl disable hadoop-mapreduce-historyserver
      exit $?
    elif [ $2 = 'mkdir' ]; then
      echo "Initializing JobHistory"
      sudo -u hdfs hdfs dfs -mkdir -p $3
      sudo -u hdfs hdfs dfs -chmod -R 1777 $3
    elif [ $2 = "logs" ]; then
      if [ $3 = "out" ]; then
        echo "Tailing JobHistory out"
        sudo -u mapred tail -n 200 /var/log/hadoop-mapreduce/mapred-mapred-historyserver-$HOSTNAME.out
      else
        echo "Invalid command"
        exit 1
      fi
    else
      echo "Invalid command"
      exit 1
    fi
  else
    echo "Invalid command"
    exit 1
  fi
}

if [ -z $1 ]; then
  yarnUsage
  exit 1
else
  yarnOperation $1 $2 $3
fi

