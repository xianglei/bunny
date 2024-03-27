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

# spark.sh initHistoryDir
# spark.sh historyserver start
# spark.sh historyserver stop
# spark.sh historyserver restart
# spark.sh historyserver enable
# spark.sh historyserver disable
# spark.sh historyserver logs log
# spark.sh historyserver logs out
# spark.sh yarnshuffle
# spark.sh master start
# spark.sh master stop
# spark.sh master restart
# spark.sh master enable
# spark.sh master disable
# spark.sh master logs log
# spark.sh master logs out
# spark.sh worker start
# spark.sh worker stop
# spark.sh worker restart
# spark.sh worker enable
# spark.sh worker disable
# spark.sh worker logs log
# spark.sh worker logs out
# spark.sh thriftserver start
# spark.sh thriftserver stop
# spark.sh thriftserver restart
# spark.sh thriftserver enable
# spark.sh thriftserver disable
# spark.sh thriftserver logs log
# spark.sh thriftserver logs out


function sparkOperation() {
  if [ -z "${JAVA_HOME}" ]; then
    echo "JAVA_HOME is not set, script will not work"
    exit 1
  fi
  if [ $1 = 'pyspark' ]; then
    # set PYSPARK_PYTHON to python3
    if grep -qwxF 'export PYSPARK_PYTHON=python3' /usr/bin/pyspark; then
      echo "PYSPARK_PYTHON is already set to python3"
    else
      sudo sed -i 's/export PYSPARK_PYTHON=python/export PYSPARK_PYTHON=python3/g' /usr/bin/pyspark
    fi
    sudo pip3 install py4j
    cd /usr/lib/spark/python; sudo /usr/bin/python3 setup.py install
  elif [ $1 = "initHistoryDir" ]; then
    # 初始化spark historyserver目录并为spark.yarn.archive配置项上传spark-libs.zip
    sudo -u hdfs hdfs dfs -mkdir -p /user/spark/history
    sudo -u hdfs hdfs dfs -mkdir -p /user/spark/archive
    sudo -u hdfs hdfs dfs -mkdir -p /user/spark/events
    sudo -u hdfs hdfs dfs -chmod -R 1777 /user/spark/history
    cd /usr/lib/spark/jars; sudo zip -rq spark-libs.zip *
    sudo -u hdfs hdfs dfs -put /usr/lib/spark/jars/spark-libs.zip /user/spark/archive
    sudo -u hdfs hdfs dfs -chmod -R 1777 /user/spark/archive
    sudo -u hdfs hdfs dfs -chmod -R 1777 /user/spark/events
    sudo -u hdfs hdfs dfs -chown -R spark:spark /user/spark
  elif [ $1 = "historyserver" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark History Server"
      sudo systemctl start spark-history-server
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark History Server"
      sudo systemctl stop spark-history-server
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark History Server"
      sudo systemctl restart spark-history-server
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-history-server
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-history-server
    elif [ $2 = 'status' ]; then
      sudo systemctl status spark-history-server
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-history-server.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-history-server.out
      else
        echo "Invalid command"
      fi
    elif [ $2 = "status" ]; then
      sudo -u spark /usr/lib/spark/sbin/spark-daemon.sh status org.apache.spark.deploy.history.HistoryServer 1
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "yarnshuffle" ]; then
    # 添加spark-yarn-shuffle.jar到hadoop-yarn lib目录
    # 需要重启yarn
    if [ -f /usr/lib/hadoop-yarn/lib/spark-yarn-shuffle.jar ]; then
      echo "Spark Yarn Shuffle jar already exists"
    else
      echo "Copying Spark Yarn Shuffle jar"
      sudo ln -sf /usr/lib/spark/yarn/lib/spark-yarn-shuffle.jar /usr/lib/hadoop-yarn/lib/
    fi
  elif [ $1 = "master" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark master"
      sudo systemctl start spark-master
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark master"
      sudo systemctl stop spark-master
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark master"
      sudo systemctl restart spark-master
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-master
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-master
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-master
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-master.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-master.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "worker" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark worker"
      sudo systemctl start spark-worker
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark worker"
      sudo systemctl stop spark-worker
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark worker"
      sudo systemctl restart spark-worker
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-worker
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-worker
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-worker
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-worker.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-worker.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  elif [ $1 = "thriftserver" ];then
    if [ $2 = "start" ]; then
      echo "Starting Spark thriftserver"
      sudo systemctl start spark-thriftserver
    elif [ $2 = "stop" ]; then
      echo "Stopping Spark thriftserver"
      sudo systemctl stop spark-thriftserver
    elif [ $2 = "restart" ]; then
      echo "Restarting Spark thriftserver"
      sudo systemctl restart spark-thriftserver
    elif [ $2 = "enable" ]; then
      sudo systemctl enable spark-thriftserver
    elif [ $2 = "disable" ]; then
      sudo systemctl disable spark-thriftserver
    elif [ $2 = "status" ]; then
      sudo systemctl status spark-thriftserver
    elif [ $2 = 'logs' ]; then
      if [ $3 = 'log' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-thriftserver.log
      elif [ $3 = 'out' ]; then
        sudo -u spark tail -n 200 /var/log/spark/spark-thriftserver.out
      else
        echo "Invalid command"
      fi
    else
      echo "Invalid operation"
    fi
  else
    echo "Invalid operation"
  fi
}

function sparkUsage() {
  echo "Usage: spark.sh [master|worker|thrift|historyserver|yarnshuffle] [start|stop|restart|enable|disable]"
}

if [ -z $1 ]; then
  sparkUsage
  exit 1
else
  sparkOperation $1 $2 $3
fi
