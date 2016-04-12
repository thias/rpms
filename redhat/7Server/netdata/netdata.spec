Name:		netdata
Version:	1.0.0
Release:	1%{?dist}
Summary:	Real-time performance monitoring

Group:		Applications/System
License:	GPLv3+
URL:		http://netdata.firehol.org/
Source0:	http://firehol.org/download/netdata/releases/v1.0.0/netdata-1.0.0.tar.xz

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires:	systemd
BuildRequires:	zlib-devel

%description
Highly optimized Linux daemon providing real-time performance monitoring for
Linux systems, Applications, SNMP devices, over the web.


%prep
%setup -q


%build
%configure --with-user=netdata
make %{?_smp_mflags}


%install
%make_install
install -p -m 0644 -D system/netdata-systemd \
  %{buildroot}%{_unitdir}/netdata.service
touch %{buildroot}%{_sysconfdir}/netdata/netdata.conf


%pre
getent group netdata > /dev/null || groupadd -r netdata
getent passwd netdata > /dev/null || useradd -r -g netdata -M \
  -d %{_localstatedir}/cache/netdata -s /sbin/nologin -c "netdata user" netdata
exit 0

%post
%systemd_post netdata.service

%preun
%systemd_preun netdata.service

%postun
%systemd_postun_with_restart netdata.service


%files
%license LICENSE.md
%doc ChangeLog README.md
%dir %{_sysconfdir}/netdata/
%config(noreplace) %{_sysconfdir}/netdata/apps_groups.conf
%config(noreplace) %{_sysconfdir}/netdata/charts.d.conf
%ghost %config %{_sysconfdir}/netdata/netdata.conf
%{_unitdir}/netdata.service
%{_libexecdir}/netdata/
%{_sbindir}/netdata
%dir %{_datadir}/netdata/
# Owner must be the daemon's running user, even though access is read-only
%attr(-,netdata,netdata) %{_datadir}/netdata/web/
%attr(-,netdata,netdata) %{_localstatedir}/cache/netdata/
%exclude %{_localstatedir}/cache/netdata/.keep
%attr(-,netdata,netdata) %{_localstatedir}/log/netdata/
%exclude %{_localstatedir}/log/netdata/.keep


%changelog
* Tue Apr 12 2016 Matthias Saou <matthias@saou.eu> 1.0.0-1
- Initial RPM release.

