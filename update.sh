#!/bin/bash
plugins_dir=/home/develenv/app/jenkins/plugins/
jenkins_plugins_url=https://updates.jenkins-ci.org/latest/
jenkins_artifacts=/var/develenv/repositories/artifacts/develenv/jenkins
jenkins_output_dir=${jenkins_artifacts}/home/develenv/app/jenkins/plugins/
jenkins_war_dir=${jenkins_artifacts}/usr/lib/jenkins
mkdir -p $jenkins_output_dir $jenkins_war_dir
curl -L -k http://mirrors.jenkins.io/war/latest/jenkins.war >$jenkins_war_dir/jenkins.war

rm -Rf $jenkins_output_dir/*.jpi
for i in $(ls $plugins_dir/*.jpi); do 
  plugin=$(basename $i)
  plugin_name=${plugin/.jpi/}
  echo $plugin_name
  echo curl -L -k ${jenkins_plugins_url}/${plugin/.jpi/.hpi} 
  curl -L -k ${jenkins_plugins_url}/${plugin/.jpi/.hpi} > $jenkins_output_dir/$plugin
done;