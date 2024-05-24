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

function in_array()
{
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

ACTION=("start" "stop" "restart" "logs" "initHBaseHDFSDir")

ROLES=("master" "regionserver" "thrift" "thrift2" "rest")
# valid $2 in [master, regionserver, thrift, thrift2]
# valid $3 is an hdfs path
# hbase.sh initHBaseHDFSDir
# hbase.sh master [start|stop|restart|logs] [log|out]
# hbase.sh regionserver [start|stop|restart|logs] [log|out]
# hbase.sh thrift [start|stop|restart|logs] [log|out]
# hbase.sh thrift2 [start|stop|restart|logs] [log|out]
# hbase.sh rest [start|stop|restart|logs] [log|out]
function hbaseOperation()
{
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = 'initHBaseHDFSDir' ]; then
        echo "Make /hbase on hdfs"
        sudo -u hdfs hdfs dfs -mkdir -p /user/hbase/
        echo "Chown /hbase on hdfs to hbase:hbase"
        sudo -u hdfs hdfs dfs -chown hbase:hbase /user/hbase/
        echo $?
  elif [ $1 = 'master' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase master'
      sudo systemctl start hbase-master
      echo $?
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-master service'
      sudo systemctl enable hbase-master
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-master service'
      sudo systemctl disable hbase-master
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-$1-$HOSTNAME.log
      elif [ $3 = 'out' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase master'
      sudo systemctl stop hbase-master
      echo $?
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase master'
      sudo systemctl restart hbase-master
      echo $?
    elif [ $2 = 'status' ]; then
      sudo systemctl status hbase-master
      echo $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'regionserver' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase regionserver'
      sudo systemctl start hbase-regionserver
      echo $?
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-regionserver service'
      sudo systemctl enable hbase-regionserver
      echo $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-regionserver service'
      sudo systemctl disable hbase-regionserver
      echo $?
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-$1-$HOSTNAME.log
      elif [ $3 = 'out' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-$1-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase regionserver'
      sudo systemctl stop hbase-regionserver
      echo $?
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase regionserver'
      sudo systemctl restart hbase-regionserver
      echo $?
    elif [ $2 = 'status' ]; then
      sudo systemctl status hbase-regionserver
      echo $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'thrift' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase thrift'
      sudo systemctl start hbase-thrift
      echo $?
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase thrift'
      sudo systemctl stop hbase-thrift
      echo $?
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase thrift'
      sudo systemctl restart hbase-thrift
      echo $?
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-thrift-$HOSTNAME.log
      elif [ $3 = 'out' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-thrift-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-thrift service'
      sudo systemctl enable hbase-thrift
      echo $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-thrift service'
      sudo systemctl disable hbase-thrift
      echo $?
    elif [ $2 = 'status' ]; then
      sudo systemctl status hbase-thrift
      echo $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'thrift2' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase thrift2'
      sudo systemctl start hbase-thrift2
      echo $?
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase thrift2'
      sudo systemctl stop hbase-thrift2
      echo $?
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase thrift'
      sudo systemctl restart hbase-thrift2
      echo $?
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-thrift2-$HOSTNAME.log
      elif [ $3 = 'out' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-thrift2-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-thrift2 service'
      sudo systemctl enable hbase-thrift2
      echo $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-thrift2 service'
      sudo systemctl disable hbase-thrift2
      echo $?
    elif [ $2 = 'status' ]; then
      sudo systemctl status hbase-thrift2
      echo $?
    else
      echo "Invalid command"
    fi
  elif [ $1 = 'rest' ]; then
    if [ $2 = 'start' ]; then
      echo 'start hbase rest'
      sudo systemctl start hbase-rest
      echo $?
    elif [ $2 = 'stop' ]; then
      echo 'stop hbase rest'
      sudo systemctl stop hbase-rest
      echo $?
    elif [ $2 = 'restart' ]; then
      echo 'restart hbase rest'
      sudo systemctl restart hbase-rest
      echo $?
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-rest-$HOSTNAME.log
      elif [ $3 = 'out' ]; then
        sudo -u hbase tail -n 200 /var/log/hbase/hbase-hbase-rest-$HOSTNAME.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = 'enable' ]; then
      echo 'enable hbase-rest service'
      sudo systemctl enable hbase-rest
      echo $?
    elif [ $2 = 'disable' ]; then
      echo 'disable hbase-rest service'
      sudo systemctl disable hbase-rest
      echo $?
    elif [ $2 = 'status' ]; then
      sudo systemctl status hbase-rest
      echo $?
    else
      echo "Invalid command"
    fi
  else
    echo "Invalid command"
  fi
}

function hbaseUsage() {
  echo "Usage: hbase.sh [master|regionserver|thrift|thrift2|rest] [initHBaseHDFSDir|start|stop|restart|enable|disable]"
}

if [ -z $1 ]; then
  hbaseUsage
  exit 1
else
  hbaseOperation $1 $2 $3
fi
