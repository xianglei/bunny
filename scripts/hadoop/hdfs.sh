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

# hdfs.sh namenode logs log
# hdfs.sh namenode logs out
# hdfs.sh namenode mkdir $dirs(comma seperated)
# hdfs.sh namenode format
# hdfs.sh namenode enable
# hdfs.sh namenode disable
# hdfs.sh namenode start
# hdfs.sh namenode stop
# hdfs.sh namenode restart
# hdfs.sh namenode mkhdfsdirs
# hdfs.sh datanode logs log
# hdfs.sh datanode logs out
# hdfs.sh datanode mkdir $dirs(comma seperated)
# hdfs.sh datanode enable
# hdfs.sh datanode disable
# hdfs.sh datanode start
# hdfs.sh datanode stop
# hdfs.sh datanode restart
# hdfs.sh journalnode logs log
# hdfs.sh journalnode logs out
# hdfs.sh journalnode mkdir $dirs(comma seperated)
# hdfs.sh journalnode enable
# hdfs.sh journalnode disable
# hdfs.sh journalnode start
# hdfs.sh journalnode stop
# hdfs.sh journalnode restart
# hdfs.sh zkfc logs log
# hdfs.sh zkfc logs out
# hdfs.sh zkfc enable
# hdfs.sh zkfc disable
# hdfs.sh zkfc start
# hdfs.sh zkfc stop
# hdfs.sh zkfc restart
# hdfs.sh initha shareedits
# hdfs.sh initha bootstrap
# hdfs.sh initha formatZK


function hdfsUsage() {
  echo "Usage: hdfs.sh [namenode|datanode|journalnode|zkfc|httpfs|balancer|initHA] [logs|mkdir|format|start|stop|restart|mkhdfsdirs]"
}

function hdfsOperation()
{
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
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
        exit 126
      else
        sudo touch /var/lib/hadoop-hdfs/formatted
        sudo -u hdfs hdfs namenode -format
        exit  $? # exit with the same status as the format command
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
    elif [ $2 = 'enable' ]; then
      echo 'enable service'
      sudo systemctl enable hadoop-hdfs-namenode
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable service'
      sudo systemctl disable hadoop-hdfs-namenode
      exit $?
    # Start namenode
    elif [ $2 = "start" ]; then
      echo "Starting Namenode"
      # Start Namenode
      sudo systemctl start hadoop-hdfs-namenode
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Namenode"
      # Stop Namenode
      sudo systemctl stop hadoop-hdfs-namenode
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Namenode"
      # Restart Namenode
      sudo systemctl restart hadoop-hdfs-namenode
      exit $?
    # mkdir hdfs dirs
    elif [ $2 = "mkhdfsdirs" ]; then
      echo "Making HDFS directories"
      # Make HDFS directories
      tmp=/tmp
      echo "Init dir /tmp"
      if sudo -u hdfs hdfs dfs -test -d /tmp; then
        echo "Directory /tmp already exists"
      else
        echo "Creating HDFS directory /tmp"
        sudo -u hdfs hdfs dfs -mkdir -p $tmp
        sudo -u hdfs hdfs dfs -mkdir -p /tmp/hadoop-yarn/staging/history/done_intermediate
        sudo -u hdfs hdfs dfs -chown -R hdfs:hadoop $tmp
        sudo -u hdfs hdfs dfs -chown -R mapred:mapred /tmp/hadoop-yarn/staging
        sudo -u hdfs hdfs dfs -chmod -R 1777 $tmp
        echo "HDFS Directory /tmp created"
      fi
      echo "Init /var"
      if sudo -u hdfs hdfs dfs -test -d /var; then
        echo "HDFS Directory /var already exists"
      else
        echo "Creating HDFS directory /var"
        sudo -u hdfs hdfs dfs -mkdir -p /var/log/hadoop-yarn
        sudo -u hdfs hdfs dfs -chown yarn:mapred /var/log/hadoop-yarn
        echo "HDFS Directory /var created"
      fi
      if sudo -u hdfs hdfs dfs -test -d /user; then
        echo "HDFS Directory /user already exists"
      else
        echo "Init /user"
        sudo -u hdfs hdfs dfs -mkdir -p /user/history
        sudo -u hdfs hdfs dfs -chmod -R 1777 /user/history
        echo "Init /user/hdfs"
        sudo -u hdfs hdfs dfs -mkdir -p /user/hdfs
        sudo -u hdfs hdfs dfs -chown -R hdfs:hadoop /user/hdfs
        echo "Init /user/mapred"
        sudo -u hdfs hdfs dfs -mkdir -p /user/mapred
        sudo -u hdfs hdfs dfs -chown -R mapred:hadoop /user/mapred
        echo "Init /user/yarn"
        sudo -u hdfs hdfs dfs -mkdir -p /user/yarn
        sudo -u hdfs hdfs dfs -chown -R yarn:hadoop /user/yarn
        sudo -u hdfs hdfs dfs -chmod 777 /user
        echo "HDFS Directory /user created"
      fi
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
    elif [ $2 = 'enable' ]; then
      echo 'enable service'
      sudo systemctl enable hadoop-hdfs-datanode
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable service'
      sudo systemctl disable hadoop-hdfs-datanode
      exit $?
    elif [ $2 = "start" ]; then
      # hdfs.sh datanode start
      echo "Starting Datanode"
      # Start Datanode
      sudo systemctl start hadoop-hdfs-datanode
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Datanode"
      # Stop Datanode
      sudo systemctl stop hadoop-hdfs-datanode
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Datanode"
      # Restart Datanode
      sudo systemctl restart hadoop-hdfs-datanode
      exit $?
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
      # hdfs.sh journalnode mkdir /dfs1/jn,/dfs2/jn
      TMP=$3
      DIRS=${TMP//,/ }
      for DIR in $DIRS; do
        sudo mkdir -p $DIR
        sudo chown -R hdfs:hadoop $DIR
        sudo chmod -R 755 $DIR
      done
    elif [ $2 = 'enable' ]; then
      echo 'enable service'
      sudo systemctl enable hadoop-hdfs-journalnode
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable service'
      sudo systemctl disable hadoop-hdfs-journalnode
      exit $?
    elif [ $2 = "start" ]; then
      # hdfs.sh journalnode start
      echo "Starting Journalnode"
      # Start Journalnode
      sudo systemctl start hadoop-hdfs-journalnode
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Journalnode"
      # Stop Journalnode
      sudo systemctl stop hadoop-hdfs-journalnode
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Journalnode"
      # Restart Journalnode
      sudo systemctl restart hadoop-hdfs-journalnode
      exit $?
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
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping ZKFC"
      # Stop ZKFC
      sudo systemctl stop hadoop-hdfs-zkfc
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting ZKFC"
      # Restart ZKFC
      sudo systemctl restart hadoop-hdfs-zkfc
      exit $?
    elif [ $2 = "logs" ]; then
      echo "Tailing ZKFC logs"
      # Tail ZKFC logs
      sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
    elif [ $2 = 'enable' ]; then
      echo 'enable service'
      sudo systemctl enable hadoop-hdfs-zkfc
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable service'
      sudo systemctl disable hadoop-hdfs-zkfc
      exit $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = "httpfs" ]; then
    if [ $2 = "start" ]; then
      echo "Starting Httpfs"
      # Start Httpfs
      sudo systemctl start hadoop-httpfs
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Httpfs"
      # Stop Httpfs
      sudo systemctl stop hadoop-httpfs
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Httpfs"
      # Restart Httpfs
      sudo systemctl restart hadoop-httpfs
      exit $?
    elif [ $2 = "logs" ]; then
      echo "Tailing Httpfs logs"
      # Tail Httpfs logs
      sudo -u hdfs tail -n 200 /var/log/hadoop-httpfs/hadoop-httpfs-httpfs-$HOSTNAME.log
    fi
  elif [ $1 = "balancer" ]; then
    if [ $2 = "start" ]; then
      echo "Starting Balancer"
      # Start Balancer
      sudo -u hdfs hdfs balancer
      exit $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = "initHA" ]; then
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
      exit $?
    elif [ $2 = "bootstrap" ]; then
      sudo -u hdfs hdfs namenode -bootstrapStandby
      exit $?
    elif [ $2 = "formatZK" ]; then
      sudo -u hdfs hdfs zkfc -formatZK
      exit $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = "secondarynamenode" ]; then
    if [ $2 = "start" ]; then
      # hdfs.sh secondarynamenode start
      echo "Starting Secondary Namenode"
      # Start Secondary Namenode
      sudo systemctl start hadoop-hdfs-secondarynamenode
      exit $?
    elif [ $2 = "stop" ]; then
      echo "Stopping Secondary Namenode"
      # Stop Secondary Namenode
      sudo systemctl stop hadoop-hdfs-secondarynamenode
      exit $?
    elif [ $2 = "restart" ]; then
      echo "Restarting Secondary Namenode"
      # Restart Secondary Namenode
      sudo systemctl restart hadoop-hdfs-secondarynamenode
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable service'
      sudo systemctl enable hadoop-hdfs-secondarynamenode
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable service'
      sudo systemctl disable hadoop-hdfs-secondarynamenode
      exit $?
    elif [ $2 = "logs" ]; then
      if [ $3 = "log" ]; then
        echo "Tailing Secondary Namenode logs"
        # Tail Secondary Namenode logs
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.log
      elif [ $3 = "out" ]; then
        sudo -u hdfs tail -n 200 /var/log/hadoop-hdfs/hadoop-hdfs-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = "mkdir" ]; then
    # hdfs.sh secondarynamenode mkdir $dirs(comma seperated)
          TMP=$3
          DIRS=${TMP//,/ }
          for DIR in $DIRS; do
            sudo mkdir -p $DIR
            sudo chown -R hdfs:hadoop $DIR
            sudo chmod -R 755 $DIR
          done
    else
      echo "Invalid command"
    fi
  else
    echo "Invalid command"
  fi
}

if [ -z $1 ]; then
  hdfsUsage
  exit 1
else
  hdfsOperation $1 $2 $3
fi
