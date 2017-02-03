# rpmbuild -bb SPECS/jenkins.spec --define '_topdir '`pwd` -v --clean

Name:       jenkins
Version:    2.44
Release:    33.g75d63d9.%{os_release}
Summary:    An extendable open source continuous integration server
Group:      develenv
License:    http://creativecommons.org/licenses/by/3.0/
Packager:   softwaresano.com
URL:        http://jenkins-ci.org/
Source0:    %{package_name}.war
BuildArch:  noarch
BuildRoot:  %{_topdir}/BUILDROOT
Requires:   ss-develenv-user > 33
Vendor:     softwaresano

%define package_name jenkins
%define target_dir  /

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
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

# ------------------------------------------------------------------------------
# INSTALL
# ------------------------------------------------------------------------------
%install
%{__mkdir_p} %{buildroot}/%{target_dir}
cp -R %{source_dir}/*  %{buildroot}/%{target_dir}

# ------------------------------------------------------------------------------
# PRE-INSTALL
# ------------------------------------------------------------------------------
%pre
# Deleting jenkins dir on tomcat to assure the update of jenkins
rm -Rf %{target_dir}
# ------------------------------------------------------------------------------
# POST-INSTALL
# ------------------------------------------------------------------------------
%post
/sbin/chkconfig --add jenkins
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
%{target_dir}/var/*
%defattr(-,root,root,-)
%{target_dir}/etc/*
%{target_dir}/usr/*

%changelog

