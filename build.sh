#!/bin/bash
mkdir -p  src/rpm/SOURCES/home/develenv/app/jenkins/plugins/ src/rpm/SOURCES/usr/lib/jenkins
rsync --delete -avr /var/develenv/repositories/artifacts/develenv/jenkins/home/develenv/app/jenkins/* \
  src/rpm/SOURCES/home/develenv/app/jenkins/

rsync --delete -avr /var/develenv/repositories/artifacts/develenv/jenkins/usr/lib/jenkins/* \
  src/rpm/SOURCES/usr/lib/jenkins/

dp_package.sh