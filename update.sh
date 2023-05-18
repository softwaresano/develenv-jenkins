#!/bin/bash -ex
plugins_dir=/home/develenv/app/jenkins/plugins/
jenkins_plugins_url=https://updates.jenkins-ci.org/latest/
jenkins_artifacts=/var/develenv/repositories/artifacts/develenv/jenkins
jenkins_output_dir=${jenkins_artifacts}/home/develenv/app/jenkins/plugins/
jenkins_war_dir=${jenkins_artifacts}/usr/lib/jenkins
jenkins_version=$(grep -A1 "<artifactId>jenkins-war</artifactId>" pom.xml|tail -1|grep -Po --color=no "(?<=<version>).*(?=<)")
mkdir -p "$jenkins_output_dir" "$jenkins_war_dir"
curl -f -L -k "http://mirrors.jenkins.io/war/${jenkins_version:?}/jenkins.war" >$jenkins_war_dir/jenkins.war || exit 1

rm -Rf $jenkins_output_dir/*.jpi
for i in $(cat plugins.list); do 
  plugin=$(basename $i)
  plugin_name=${plugin/.jpi/}
  echo $plugin_name
  echo curl --retry 5 --http2 -f -L -k ${jenkins_plugins_url}/${plugin/.jpi/.hpi} 
  curl --retry 5 --http1.1 -f -L -k ${jenkins_plugins_url}/${plugin/.jpi/.hpi} > $jenkins_output_dir/$plugin || exit 1
done;
