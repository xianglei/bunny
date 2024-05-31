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

function ozoneUsage() {
    echo "Usage: ozone.sh {scm|om|datanode} {start|stop|status}"
    exit 1
}

function ozoneOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = 'scm' ]; then
    if [ $2 = 'init' ]; then
      if [ -f /usr/lib/ozone/scm.init-ed ]; then
        echo "Ozone SCM is already init-ed, if want to re-init, remove the scm meta dir and /usr/lib/ozone/scm.init-ed file manually and re-run the script"
        exit 1
      else
        sudo -u ozone /usr/lib/ozone/bin/ozone scm --init
        sudo touch /usr/lib/ozone/scm.init-ed
        sudo chown ozone:ozone /usr/lib/ozone/scm.init-ed
      fi
    elif [ $2 = 'mkdir' ]; then
      # ozone.metadata.dirs
      TMP=$3
      DIRS=${TMP//,/ }
      echo "Creating $DIR"
      for dir in $DIRS; do
        sudo mkdir -p $dir
        # chown from parent's parent dir
        # ex meta dir is /var/lib/ozone/metadata, then chown from /var/lib/ozone
        sudo chown -R ozone:ozone $dir
      done
    elif [ $2 = 'start' ]; then
      echo "Starting Ozone SCM"
      #sudo systemctl start ozone-scm
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon start scm
      exit $?
    elif [ $2 = 'stop' ]; then
      echo "Stopping Ozone SCM"
      #sudo systemctl stop ozone-scm
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon stop scm
      exit $?
    elif [ $2 = 'status' ]; then
      echo "Checking Ozone SCM status"
      #sudo systemctl status ozone-scm
      PID=$(ps -ef | grep -v grep | grep "ozone" | grep 'proc_scm' | awk '{print $2}')
      if [ -z "$PID" ]; then
        echo "Ozone SCM is not running"
        exit 1
      else
        echo "Ozone SCM is running with PID: $PID"
        exit 0
      fi
    elif [ $2 = 'restart' ]; then
      echo "Restarting Ozone SCM"
      #sudo systemctl restart ozone-scm
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon restart scm
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable ozone-scm service'
      sudo systemctl enable ozone-scm
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable ozone-scm service'
      sudo systemctl disable ozone-scm
      exit $?
    else
      ozoneUsage
    fi
  elif [ $1 = 'om' ]; then
    if [ $2 = 'init' ]; then
      if [ -f /usr/lib/ozone/om.init-ed ]; then
        echo "Ozone OM is already init-ed, if want to re-init, remove the om meta dir and /usr/lib/ozone/om.init-ed file manually and re-run the script"
        exit 1
      else
        sudo -u ozone /usr/lib/ozone/bin/ozone om --init
        sudo touch /usr/lib/ozone/om.init-ed
        sudo chown ozone:ozone /usr/lib/ozone/om.init-ed
      fi
    elif [ $2 = 'mkdir' ]; then
      # ozone.om.db.dirs
      TMP=$3
      DIRS=${TMP//,/ }
      echo "Creating $DIR"
      for dir in $DIRS; do
        sudo mkdir -p $dir
        sudo chown -R ozone:ozone $dir
      done
    elif [ $2 = 'start' ]; then
      echo "Starting Ozone OM"
      #sudo systemctl start ozone-om
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon start om
      exit $?
    elif [ $2 = 'stop' ]; then
      echo "Stopping Ozone OM"
      #sudo systemctl stop ozone-om
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon stop om
      exit $?
    elif [ $2 = 'status' ]; then
      echo "Checking Ozone OM status"
      PID=$(ps -ef | grep -v grep | grep "ozone" | grep 'proc_om' | awk '{print $2}')
      if [ -z "$PID" ]; then
        echo "Ozone SCM is not running"
        exit 1
      else
        echo "Ozone SCM is running with PID: $PID"
        exit 0
      fi
    elif [ $2 = 'restart' ]; then
      echo "Restarting Ozone OM"
      #sudo systemctl restart ozone-om
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon restart om
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable ozone-om service'
      sudo systemctl enable ozone-om
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable ozone-om service'
      sudo systemctl disable ozone-om
      exit $?
    else
      ozoneUsage
    fi
  elif [ $1 = 'datanode' ]; then
    if [ $2 = 'start' ]; then
      echo "Starting Ozone Datanode"
      #sudo systemctl start ozone-datanode
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon start datanode
      exit $?
    elif [ $2 = 'stop' ]; then
      echo "Stopping Ozone Datanode"
      #sudo systemctl stop ozone-datanode
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon stop datanode
      exit $?
    elif [ $2 = 'status' ]; then
      echo "Checking Ozone Datanode status"
      PID=$(ps -ef | grep -v grep | grep "ozone" | grep 'proc_datanode' | awk '{print $2}')
      if [ -z "$PID" ]; then
        echo "Ozone SCM is not running"
        exit 1
      else
        echo "Ozone SCM is running with PID: $PID"
        exit 0
      fi
    elif [ $2 = 'restart' ]; then
      echo "Restarting Ozone Datanode"
      #sudo systemctl restart ozone-datanode
      sudo -u ozone /usr/lib/ozone/bin/ozone --daemon restart datanode
      exit $?
    elif [ $2 = 'enable' ]; then
      echo 'enable ozone-datanode service'
      sudo systemctl enable ozone-datanode
      exit $?
    elif [ $2 = 'disable' ]; then
      echo 'disable ozone-datanode service'
      sudo systemctl disable ozone-datanode
      exit $?
    elif [ $2 = 'mkdir' ]; then
      # hdds.datanode.dirs
      TMP=$3
      DIRS=${TMP//,/ }
      echo "Creating $DIR"
      for dir in $DIRS; do
        sudo mkdir -p $dir
        sudo chown -R ozone:ozone $dir
      done
    else
      ozoneUsage
    fi
  else
    ozoneUsage
  fi
}

if [ -z $1 ]; then
  ozoneUsage
  exit 1
else
  ozoneOperation $1 $2 $3
fi



