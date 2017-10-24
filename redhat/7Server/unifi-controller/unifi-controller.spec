%global __jar_repack 0
%global debug_package %{nil}
%global unifi_prefix /opt/UniFi

Name: unifi-controller
Version: 5.6.19
Release: 1%{?dist}
Summary: UniFi wireless AP (UAP), routing (USG), and switching (USW) controller
Group: System Environment/Daemons
License: It's complicated
URL: https://www.ubnt.com/download/unifi/
Source0: https://dl.ubnt.com/unifi/%{version}/UniFi.unix.zip
Source1: unifi.service
Requires: mongodb-server
Requires: java-1.8.0-openjdk-headless
%{?systemd_requires}
BuildRequires: systemd
ExclusiveArch: x86_64 %{arm}

%description
Ubiquiti UniFi wireless AP (UAP), routing (USG), and switching (USW)
controller.

This package is made from the UniFi.unix.zip archive, and installs everything
to %{unifi_prefix}, while providing a nice systemd unit to manage the unifi
service, running as a non-privileged user.


%prep
%setup -q -n UniFi
# Remove non-relevant arch-specific libraries
rm -rf lib/native/Mac
rm -rf lib/native/Windows
%ifarch x86_64
rm -rf lib/native/Linux/armhf
%endif
%ifarch %{arm}
rm -rf lib/native/Linux/amd64
%endif
# This directory seems obsolete, conf is data/system.properties
rmdir conf


%build


%install
mkdir -p %{buildroot}%{unifi_prefix}
mv * %{buildroot}%{unifi_prefix}/
mkdir -p %{buildroot}%{unifi_prefix}/{data,logs,run,work}
# Service
mkdir -p %{buildroot}%{_unitdir}
sed -e "s|@UNIFI_PREFIX@|%{unifi_prefix}|" %{SOURCE1} > \
  %{buildroot}%{_unitdir}/unifi.service


%pre
/usr/bin/getent group ubnt >/dev/null || /usr/sbin/groupadd -r ubnt
if ! /usr/bin/getent passwd ubnt >/dev/null; then
  /usr/sbin/useradd -r -g ubnt -M -N -d %{unifi_prefix} -s /sbin/nologin -c "Ubiquiti Networks" ubnt
fi

%post
%systemd_post unifi.service

%preun
%systemd_preun unifi.service

%postun
%systemd_postun_with_restart unifi.service


%files
%doc %{unifi_prefix}/readme.txt
%{_unitdir}/unifi.service
%{unifi_prefix}/bin/
%attr(0755,ubnt,ubnt) %{unifi_prefix}/data/
%attr(0755,ubnt,ubnt) %{unifi_prefix}/dl/
%{unifi_prefix}/lib/
%attr(0755,ubnt,ubnt) %{unifi_prefix}/logs/
%attr(0755,ubnt,ubnt) %{unifi_prefix}/run/
%{unifi_prefix}/webapps/
%attr(0755,ubnt,ubnt) %{unifi_prefix}/work/


%changelog
* Tue Oct 24 2017 Matthias Saou <matthias@saou.eu> 5.6.19-1
- Update to 5.6.19.

* Mon Oct 16 2017 Matthias Saou <matthias@saou.eu> 5.5.24-1
- Update to 5.5.24.

* Mon Jul 31 2017 Matthias Saou <matthias@saou.eu> 5.5.20-1
- Update to 5.5.20.

* Tue Jul  4 2017 Matthias Saou <matthias@saou.eu> 5.5.19-1
- Update to 5.5.19.

* Tue Jun 27 2017 Matthias Saou <matthias@saou.eu> 5.4.18-1
- Update to 5.4.18.

* Tue Jun  6 2017 Matthias Saou <matthias@saou.eu> 5.4.16-1
- Update to 5.4.16.
- Disable (empty) debuginfo package creation.

* Mon Jan  9 2017 Matthias Saou <matthias@saou.eu> 5.3.8-1
- Update to 5.3.8.

* Tue Nov 22 2016 Matthias Saou <matthias@saou.eu> 5.2.9-1
- Initial RPM release.

