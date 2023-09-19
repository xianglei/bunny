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

# hdfs.sh namenode logs log tail
# hdfs.sh namenode mkdir $dirs(comma seperated)
# hdfs.sh namenode format
# hdfs.sh namenode start
# hdfs.sh namenode stop
# hdfs.sh namenode restart
# hdfs.sh namenode mkhdfsdirs
# hdfs.sh datanode logs log tail
# hdfs.sh datanode mkdir $dirs(comma seperated)
# hdfs.sh datanode start
# hdfs.sh datanode stop
# hdfs.sh datanode restart
# hdfs.sh journalnode logs log tail
# hdfs.sh journalnode mkdir $dirs(comma seperated)
# hdfs.sh journalnode start
# hdfs.sh journalnode stop
# hdfs.sh journalnode restart
# hdfs.sh zkfc logs log tail
# hdfs.sh zkfc start
# hdfs.sh zkfc stop
# hdfs.sh zkfc restart
# hdfs.sh initha shareedits
# hdfs.sh initha bootstrap
# hdfs.sh initha formatZK


function hdfsUsage() {
  echo "Usage: hdfs.sh [namenode|datanode|journalnode|zkfc] [logs|mkdir|format|start|stop|restart|mkhdfsdirs]"
}

function hdfsOperation()
{
  if [ $1 = "namenode" ]; then
    # mkdir namenode metadata dirs
    if [ $2 = "mkdir" ]; then
      # hdfs.sh namenode mkdir $dirs(comma seperated)
      TMP=$3
      DIRS=${TMP//,/ }
      for DIR in $DIRS; do
        sudo mkdir -p $DIR
        sudo chown -R hdfs:hadoop $DIR
        sudo chmod -R 755 $DIR
      done
    # format namenode
    elif [ $2 = "format" ]; then
      # hdfs.sh namenode format
      echo "Formatting the namenode"
      # formatted
      if [ -f /var/lib/hadoop-hdfs/formatted ]; then
        echo "Namenode already formatted"
      else
        sudo -u hdfs hdfs namenode -format
        sudo touch /var/lib/hadoop-hdfs/formatted
      fi
    # Tail namenode logs
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing Namenode logs"
        # Tail Namenode logs
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    # Start namenode
    elif [ $2 = "start" ]; then
      echo "Starting Namenode"
      # Start Namenode
      sudo systemctl start hadoop-hdfs-namenode
    elif [ $2 = "stop" ]; then
      echo "Stopping Namenode"
      # Stop Namenode
      sudo systemctl stop hadoop-hdfs-namenode
    elif [ $2 = "restart" ]; then
      echo "Restarting Namenode"
      # Restart Namenode
      sudo systemctl restart hadoop-hdfs-namenode
    # mkdir hdfs dirs
    elif [ $2 = "mkhdfsdirs" ]; then
      echo "Making HDFS directories"
      # Make HDFS directories
      tmp=/tmp
      echo "Init dir /tmp"
      sudo -u hdfs hdfs dfs -mkdir -p $tmp
      sudo -u hdfs hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging/history/done_intermediate
      sudo -u hdfs hdfs dfs -chown -R hdfs:hadoop $tmp
      sudo -u hdfs hdfs dfs -chown -R mapred:mapred /tmp/hadoop-yarn/staging
      sudo -u hdfs hdfs dfs -chmod -R 1777 $tmp
      echo "Init /var"
      sudo -u hdfs hdfs dfs -mkdir -p /var/log/hadoop-yarn
      sudo -u hdfs hdfs dfs -chown yarn:mapred /var/log/hadoop-yarn
      echo "Init /user"
      sudo -u hdfs hdfs dfs -mkdir -p /user/history
      sudo -u hdfs hdfs dfs -chmod -R 1777 /user/history
      sudo -u hdfs hdfs dfs -mkdir -p /user/hdfs
      sudo -u hdfs hdfs dfs -chown -R hdfs:hadoop /user/hdfs
      sudo -u hdfs hdfs dfs -mkdir -p /user/mapred
      sudo -u hdfs hdfs dfs -chown -R mapred:hadoop /user/mapred
      sudo -u hdfs hdfs dfs -mkdir -p /user/yarn
      sudo -u hdfs hdfs dfs -chown -R yarn:hadoop /user/yarn
    else
      echo "Invalid command"
    fi
  elif [ $1 = "datanode" ]; then
    if [ $2 = "mkdir" ]; then
      # hdfs.sh datanode mkdir $dirs(comma seperated)
      TMP=$3
      DIRS=${TMP//,/ }
      for DIR in $DIRS; do
        sudo mkdir -p $DIR
        sudo chown -R hdfs:hadoop $DIR
        sudo chmod -R 755 $DIR
      done
    elif [ $2 = "start" ]; then
      # hdfs.sh datanode start
      echo "Starting Datanode"
      # Start Datanode
      sudo systemctl start hadoop-hdfs-datanode
    elif [ $2 = "stop" ]; then
      echo "Stopping Datanode"
      # Stop Datanode
      sudo systemctl stop hadoop-hdfs-datanode
    elif [ $2 = "restart" ]; then
      echo "Restarting Datanode"
      # Restart Datanode
      sudo systemctl restart hadoop-hdfs-datanode
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing Datanode logs"
        # Tail Datanode logs
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid command"
    fi
  elif [ $1 = "journalnode" ]; then
    if [ $2 = "mkdir" ]; then
      # hdfs.sh journalnode mkdir $dirs(comma seperated)
      TMP=$3
      DIRS=${TMP//,/ }
      for DIR in $DIRS; do
        sudo mkdir -p $DIR
        sudo chown -R hdfs:hadoop $DIR
        sudo chmod -R 755 $DIR
      done
    elif [ $2 = "start" ]; then
      # hdfs.sh journalnode start
      echo "Starting Journalnode"
      # Start Journalnode
      sudo systemctl start hadoop-hdfs-journalnode
    elif [ $2 = "stop" ]; then
      echo "Stopping Journalnode"
      # Stop Journalnode
      sudo systemctl stop hadoop-hdfs-journalnode
    elif [ $2 = "restart" ]; then
      echo "Restarting Journalnode"
      # Restart Journalnode
      sudo systemctl restart hadoop-hdfs-journalnode
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing Journalnode logs"
        # Tail Journalnode logs
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid command"
    fi
  elif [ $1 = "zkfc" ]; then
    if [ $2 = "start" ]; then
      # hdfs.sh zkfc start
      echo "Starting ZKFC"
      # Start ZKFC
      sudo systemctl start hadoop-hdfs-zkfc
    elif [ $2 = "stop" ]; then
      echo "Stopping ZKFC"
      # Stop ZKFC
      sudo systemctl stop hadoop-hdfs-zkfc
    elif [ $2 = "restart" ]; then
      echo "Restarting ZKFC"
      # Restart ZKFC
      sudo systemctl restart hadoop-hdfs-zkfc
    elif [ $2 = "logs" ]; then
      echo "Tailing ZKFC logs"
      # Tail ZKFC logs
      sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
    else
      echo "Invalid command"
    fi
  elif [ $1 = "initha" ]; then
    echo "Initializing High Availability"
    # Initialize High Availability
    : '
    1. stop secondary namenode
    2. stop namenode
    3. stop datanodes
    4. deploy configurations
    5. install journalnode and local storage mkdirs
    6. start journalnode
    7. initializeSharedEdits
    8. start the pre-active namenode
    9. install pre-standby namenode
    10 bootstrapStandby on pre-standby namenode
    11. pre-standby namenode start
    12. install zkfc
    13. format zkfc
    14. start zkfc on both namenode
    15. start datanodes
    16. start other services
    '
    if [ $2 = "shareedits" ]; then
      sudo -u hdfs hdfs namenode -initializeSharedEdits
    elif [ $2 = "bootstrap" ]; then
      sudo -u hdfs hdfs namenode -bootstrapStandby
    elif [ $2 = "formatZK" ]; then
      sudo -u hdfs hdfs zkfc -formatZK
    else
      echo "Invalid command"
    fi
  fi
}


:<<!
function initHdfsDirs() {
  echo "Initializing HDFS"
  # Create the data directory
  # hdfs.sh namenode mkdir $dirs(comma seperated)
  # hdfs.sh datanode mkdir $dirs(comma seperated)
  # hdfs.sh journalnode mkdir $dirs(comma seperated)
  TMP=$3
  DIRS=${TMP//,/ }
  if [ $1 = "namenode" ]; then
    for DIR in $DIRS; do
      sudo mkdir -p $DIR
      sudo chown -R hdfs:hadoop $DIR
      sudo chmod -R 755 $DIR
    done
  elif [ $1 == "datanode" ]; then
    for DIR in $DIRS; do
          sudo mkdir -p $DIR
          sudo chown -R hdfs:hadoop $DIR
          sudo chmod -R 755 $DIR
        done
  else
    echo "Invalid command"
  fi
}

function formatHdfs() {
  # hdfs.sh namenode format
  echo "Formatting the namenode"
  # format the namenode
  if [ -f /var/lib/hadoop-hdfs/formatted ]; then
    echo "Namenode already formatted"
  else
    sudo -u hdfs hdfs namenode -format
    sudo touch /var/lib/hadoop-hdfs/formatted
  fi
}

function startHdfs() {
  # hdfs.sh namenode start
  # hdfs.sh datanode start
  # hdfs.sh journalnode start
  # hdfs.sh zkfc start
  ROLE=$1
  if [ 'namenode' = $ROLE ]; then
    echo "Starting Namenode"
    # Start Namenode
    sudo systemctl start hadoop-hdfs-namenode
  elif [ 'datanode' = $ROLE ]; then
    echo "Starting Datanode"
    # Start Datanode
    sudo systemctl start hadoop-hdfs-datanode
  elif [ 'journalnode' = $ROLE ]; then
    echo "Starting Journalnode"
    # Start Journalnode
    sudo systemctl start hadoop-hdfs-journalnode
  elif [ 'zkfc' = $ROLE ]; then
    echo "Starting ZKFC"
    # Start ZKFC
    sudo systemctl start hadoop-hdfs-zkfc
  else
    echo "Invalid command"
  fi
}

function stopHdfs() {
  # hdfs.sh namenode stop
  # hdfs.sh datanode stop
  # hdfs.sh journalnode stop
  # hdfs.sh zkfc stop
  ROLE=$1
  if [ 'namenode' = $ROLE ]; then
    echo "Stopping Namenode"
    # Stop Namenode
    sudo systemctl stop hadoop-hdfs-namenode
  elif [ 'datanode' = $ROLE ]; then
    echo "Stopping Datanode"
    # Stop Datanode
    sudo systemctl stop hadoop-hdfs-datanode
  elif [ 'journalnode' = $ROLE ]; then
    echo "Stopping Journalnode"
    # Stop Journalnode
    sudo systemctl stop hadoop-hdfs-journalnode
  elif [ 'zkfc' = $ROLE ]; then
    echo "Stopping ZKFC"
    # Stop ZKFC
    sudo systemctl stop hadoop-hdfs-zkfc
  else
    echo "Invalid command"
  fi
}

function restartHdfs() {
  # hdfs.sh namenode restart
  # hdfs.sh datanode restart
  # hdfs.sh journalnode restart
  # hdfs.sh zkfc restart
  if [ 'namenode' = $ROLE ]; then
    echo "Restarting Namenode"
    # Restart Namenode
    sudo systemctl restart hadoop-hdfs-namenode
  elif [ 'datanode' = $ROLE ]; then
    echo "Restarting Datanode"
    # Restart Datanode
    sudo systemctl restart hadoop-hdfs-datanode
  elif [ 'journalnode' = $ROLE ]; then
    echo "Restarting Journalnode"
    # Restart Journalnode
    sudo systemctl restart hadoop-hdfs-journalnode
  elif [ 'zkfc' = $ROLE ]; then
    echo "Restarting ZKFC"
    # Restart ZKFC
    sudo systemctl restart hadoop-hdfs-zkfc
  else
    echo "Invalid command"
  fi
}

if [ ! $1 ]; then
  echo "No command specified"
else
  if [ $1 = "namenode" ]; then
    if [ $2 = 'format' ]; then
      formatHdfs
    elif [ $2 = 'start' ]; then
      startHdfs $1
    elif [ $2 = 'stop' ]; then
      stopHdfs $1
    elif [ $2 = 'restart' ]; then
      restartHdfs $1
    elif [ $2 = 'logs' ]; then
      tailLogs $1 $2 $3
    elif [ $2 = 'mkdir' ]; then
      initHdfsDirs $1 $2 $3
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'datanode' ]; then
    if [ $2 = 'start' ]; then
      startHdfs $1
    elif [ $2 = 'stop' ]; then
      stopHdfs $1
    elif [ $2 = 'restart' ]; then
      restartHdfs $1
    elif [ $2 = 'logs' ]; then
      tailLogs $1 $2 $3
    elif [ $2 = 'mkdir' ]; then
      initHdfsDirs $1 $2 $3
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'journalnode' ]; then
    if [ $2 = 'start' ]; then
      startHdfs $1
    elif [ $2 = 'stop' ]; then
      stopHdfs $1
    elif [ $2 = 'restart' ]; then
      restartHdfs $1
    elif [ $2 = 'logs' ]; then
      tailLogs $1 $2 $3
    elif [ $2 = 'mkdir' ]; then
      initHdfsDirs $1 $2 $3
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'zkfc' ]; then
    if [ $2 = 'start' ]; then
      startHdfs $1
    elif [ $2 = 'stop' ]; then
      stopHdfs $1
    elif [ $2 = 'restart' ]; then
      restartHdfs $1
    elif [ $2 = 'logs' ]; then
      tailLogs $1 $2 $3
    elif [ $2 = 'mkdir' ]; then
      initHdfsDirs $1 $2 $3
    else
      echo "Invalid command"
    fi
  else
    echo "Invalid command"
  fi
fi
!
