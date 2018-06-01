# rpmbuild -bb SPECS/jenkins.spec --define '_topdir '`pwd` -v --clean
%define jenkins_version 2.125
Name:       jenkins
Version:    %{versionModule}
Release:    %{jenkins_version}.%{releaseModule}
Epoch:      2
Summary:    An extendable open source continuous integration server
Group:      develenv
License:    http://creativecommons.org/licenses/by/3.0/
Packager:   softwaresano.com
URL:        http://jenkins-ci.org/
Source0:    %{package_name}.war
BuildArch:  noarch
BuildRoot:  %{_topdir}/BUILDROOT
Requires:   ss-develenv-user >= 33 httpd jdk mod_proxy_html
Vendor:     softwaresano

%define package_name jenkins
%define target_dir /
%define jenkins_home /home/develenv/app/jenkins

%description
Jenkins is an award-winning application that monitors executions of repeated jobs,
 such as building a software project or jobs run by cron. Among those things, 
current Jenkins focuses on the following two jobs:

1 - Building/testing software projects continuously, just like CruiseControl or 
DamageControl. In a nutshell, Jenkins provides an easy-to-use so-called 
continuous integration system, making it easier for developers to integrate
changes to the project, and making it easier for users to obtain a fresh build. 
The automated, continuous build increases the productivity.

2 - Monitoring executions of externally-run jobs, such as cron jobs and procmail
jobs, even those that are run on a remote machine. For example, with cron, all 
you receive is regular e-mails that capture the output, and it is up to you to
 look at them diligently and notice when it broke. Jenkins keeps those outputs
and makes it easy for you to notice when something is wrong.

# ------------------------------------------------------------------------------
# CLEAN
# ------------------------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

# ------------------------------------------------------------------------------
# INSTALL
# ------------------------------------------------------------------------------
%install
%{__mkdir_p} $RPM_BUILD_ROOT/%{target_dir} $RPM_BUILD_ROOT/%{jenkins_home}
%{__mkdir_p} $RPM_BUILD_ROOT/%{jenkins_home}/jobs/ $RPM_BUILD_ROOT/%{jenkins_home}/users/
%{__mkdir_p} $RPM_BUILD_ROOT/%{jenkins_home}/workflow-libs


printf "%{jenkins_version}" >$RPM_BUILD_ROOT/%{jenkins_home}/jenkins.install.InstallUtil.lastExecVersion
cp -R %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
# ------------------------------------------------------------------------------
# PRE-INSTALL
# ------------------------------------------------------------------------------
%pre
# ------------------------------------------------------------------------------
# POST-INSTALL
# ------------------------------------------------------------------------------
%post
/sbin/chkconfig --add jenkins
if [[ "$(sestatus -b|awk '{print $1$2}'|grep 'httpd_can_network_connectoff')" != "" ]]; then \
  setsebool -P httpd_can_network_connect true
fi

# ------------------------------------------------------------------------------
# PRE-UNINSTALL
# ------------------------------------------------------------------------------
%preun
if [ "$1" = 0 ] ; then
    # if this is uninstallation as opposed to upgrade, delete the service
    /sbin/service jenkins stop > /dev/null 2>&1
    /sbin/chkconfig --del jenkins
fi
# ------------------------------------------------------------------------------
# POST-UNINSTALL
# ------------------------------------------------------------------------------
%postun
if [ "$1" -ge 1 ]; then
    /sbin/service jenkins condrestart > /dev/null 2>&1
fi
%files
%defattr(-,develenv,develenv,-)
%{jenkins_home}
%dir %{jenkins_home}/jobs/
%dir %{jenkins_home}/users/
%dir %{jenkins_home}/workflow-libs/
%{target_dir}/var/log/jenkins
%{target_dir}/var/cache/jenkins
%{target_dir}/var/lib/jenkins
%{target_dir}/var/lib/jenkins
%defattr(-,root,root,-)
%{target_dir}/etc/init.d/jenkins
%{target_dir}/etc/logrotate.d/jenkins
%{target_dir}/etc/sysconfig/jenkins
%{target_dir}/usr/lib/jenkins/*
%{target_dir}/etc/httpd/conf.d/*
%config(noreplace) /etc/sysconfig/jenkins

