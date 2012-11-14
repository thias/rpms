Summary: Log management solution using Elasticsearch and MongoDB
Name: graylog2-server
Version: 0.9.6p1
Release: 1%{?dist}
License: GPLv3+
Group: System Environment/Daemons
URL: http://graylog2.org/
Source0: https://github.com/downloads/Graylog2/graylog2-server/graylog2-server-%{version}.tar.gz
Source1: graylog2-server.init
Source2: graylog2-server.sysconfig
Source3: graylog2-server.logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: java
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): initscripts, chkconfig
Requires(postun): initscripts

%description
Graylog2 is an open source log management solution that stores your logs in
ElasticSearch. It consists of a server written in Java that accepts your
syslog messages via TCP, UDP or AMQP and stores it in the database.


%prep
%setup -q


%build


%install
rm -rf %{buildroot}
install -D -p -m 0644 graylog2-server.jar \
    %{buildroot}%{_datadir}/graylog2-server/graylog2-server.jar
install -D -p -m 0644 graylog2.conf.example \
    %{buildroot}%{_sysconfdir}/graylog2.conf
install -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/init.d/graylog2-server
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/graylog2-server
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/logrotate.d/graylog2-server
mkdir -p %{buildroot}/var/log/graylog2
mkdir -p %{buildroot}/var/run/graylog2


%clean
rm -rf %{buildroot}


%pre
%{_sbindir}/useradd -d / -r -s /sbin/nologin graylog2 2>/dev/null || :

%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add graylog2-server
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service graylog2-server stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del graylog2-server
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service graylog2-server condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_sysconfdir}/init.d/graylog2-server
%config(noreplace) %{_sysconfdir}/logrotate.d/graylog2-server
%config(noreplace) %{_sysconfdir}/sysconfig/graylog2-server
%config(noreplace) %{_sysconfdir}/graylog2.conf
%{_datadir}/graylog2-server/
%dir %attr(0755,graylog2,graylog2) /var/log/graylog2/
%dir %attr(0755,graylog2,graylog2) /var/run/graylog2/


%changelog
* Wed Nov 14 2012 Matthias Saou <matthias@saou.eu> 0.9.6p1-1
- Initial RPM release.

