# hdfs.sh
  - hdfs.sh namenode logs log
  - hdfs.sh namenode logs out
  - hdfs.sh namenode mkdir $dirs(逗号分割)
  - hdfs.sh namenode format
  - hdfs.sh namenode enable
  - hdfs.sh namenode disable
  - hdfs.sh namenode start
  - hdfs.sh namenode stop
  - hdfs.sh namenode restart
  - hdfs.sh namenode mkhdfsdirs
  - hdfs.sh datanode logs log
  - hdfs.sh datanode logs out
  - hdfs.sh datanode mkdir $dirs(逗号分割)
  - hdfs.sh datanode enable
  - hdfs.sh datanode disable
  - hdfs.sh datanode start
  - hdfs.sh datanode stop
  - hdfs.sh datanode restart
  - hdfs.sh journalnode logs log
  - hdfs.sh journalnode logs out
  - hdfs.sh journalnode mkdir $dirs(comma seperated)
  - hdfs.sh journalnode enable
  - hdfs.sh journalnode disable
  - hdfs.sh journalnode start
  - hdfs.sh journalnode stop
  - hdfs.sh journalnode restart
  - hdfs.sh zkfc logs log
  - hdfs.sh zkfc logs out
  - hdfs.sh zkfc enable
  - hdfs.sh zkfc disable
  - hdfs.sh zkfc start
  - hdfs.sh zkfc stop
  - hdfs.sh zkfc restart
  - hdfs.sh initha shareedits
  - hdfs.sh initha bootstrap
  - hdfs.sh initha formatZK

# yarn.sh
  - yarn.sh resourcemanager [ start | stop | restart ]
  - yarn.sh resourcemanager logs [ log | out ]
  - yarn.sh nodemanager [ start | stop | restart ]
  - yarn.sh nodemanager logs [ log | out ]
  - yarn.sh jobhistory [ start | stop | restart ]
  - yarn.sh jobhistory logs out

# hbase.sh
  - hbase.sh master [ start | stop | restart | enable | disable ]
  - hbase.sh master initHBaseHDFSDir $dir
  - hbase.sh regionserver [ start | stop | restart | enable | disable ]
  - hbase.sh regionserver logs [ log | out ]
  - hbase.sh thrift [ start | stop | restart ]
  - hbase.sh thrift logs [ log | out ]
  - hbase.sh rest [ start | stop | restart ]
  - hbase.sh rest logs [ log | out ]
  - hbase.sh zookeeper [ start | stop | restart ]
  - hbase.sh zookeeper logs [ log | out ]

# zookeeper.sh
  - zookeeper.sh init [1|2|3] (每台机器一个id, 先要配置好zoo.cfg后执行初始化, 然后再启动)
  - zookeeper.sh start
  - zookeeper.sh stop
  - zookeeper.sh restart
  - zookeeper.sh logs [ log | out ]






