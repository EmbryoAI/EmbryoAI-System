#!/bin/bash

until ping -nq -c3 A.B.C.D; do
   # Waiting for network
   sleep 1
done
/bin/mount -t cifs -o rw,vers=1.0,username=username,password=password,uid=linuxuser,_netdev //192.168.40.10/Public/temp /mnt/share
export DB_DIR='/home/astec/mysql'
export CAPTURE_DIR='/mnt/share'
docker start mysql
cd /var/lib/jenkins/workspace/embryoai_sys/code/ && docker-compose up -d
