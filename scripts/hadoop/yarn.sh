#!/bin/bash

if [ $JAVA_HOME ]; then
  echo "JAVA_HOME is set to $JAVA_HOME"
  if [ -z "$JAVA_HOME" ]; then
    echo "JAVA_HOME is null"
    export JAVA_HOME=/usr/java/default
  else
    echo "JAVA_HOME is set"
    export PATH=$PATH:$JAVA_HOME/bin
    export JAVA_HOME=$JAVA_HOME
    if [ -e "$JAVA_HOME/bin/java" ]; then
      echo "JAVA_HOME ok"
    else
      echo "JAVA_HOME not ok"
      exit 1
    fi
  fi
else
  echo "JAVA_HOME is not set"
  exit 1
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
