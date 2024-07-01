#!/usr/bin/env bash


function FirewalldAndSELinux() {
  systemctl stop firewalld
  systemctl disable firewalld
  setenforce 0
  sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
}

function PrepareDependences() {
  sudo timedatectl set-timezone Asia/Shanghai
  sudo yum install -y ntp ipvsadm ipset
  sudo systemctl start ntpd
  sudo systemctl enable ntpd
  sudo cat > /etc/sysconfig/modules/ipvs.modules << EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack

EOF
  sudo chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules && lsmod |grep -e ip_vs -e nf_conntrack
}

function SysctlAndModprobe() {
  modprobe br_netfilter
  modprobe overlay
  echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables
  echo '1' > /proc/sys/net/bridge/bridge-nf-call-ip6tables
  echo '1' > /proc/sys/net/bridge/bridge-nf-call-arptables
  echo '1' > /proc/sys/net/bridge/bridge-nf-filter-pppoe-tagged
  echo '1' > /proc/sys/net/ip4/ip_forward
  echo '0' > /proc/sys/vm/swappiness
  cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-arptables = 1
net.bridge.bridge-nf-filter-pppoe-tagged = 1
net.ipv4.ip_forward = 1
vm.swappiness = 0
EOF
  sysctl -p /etc/sysctl.d/k8s.conf
  swapoff -a
}


function K8SOperation() {
    if [ $1 = 'enable' ]; then
        echo "Enabling k8s"
        sudo systemctl enable kubelet
        exit $?
    elif [ $1 = 'disable' ]; then
        echo "Disabling k8s"
        sudo systemctl disable kubelet
        exit $?
    elif [ $1 = 'start' ];then
        echo "Starting k8s"
        sudo systemctl start kubelet
        exit $?
    elif [ $1 = 'stop' ]; then
        echo "Stopping k8s"
        sudo systemctl stop kubelet
        exit $?
    elif [ $1 = 'restart' ]; then
        echo "Restarting k8s"
        sudo systemctl restart kubelet
        exit $?
    elif [ $1 = 'status' ]; then
        echo "Checking k8s status"
        sudo systemctl status kubelet
        exit $?
    else
        echo "Invalid operation"
    fi
}

K8SOperation $1
