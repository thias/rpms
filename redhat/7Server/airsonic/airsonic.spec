%global __jar_repack 0
%global debug_package %{nil}

Name: airsonic
Version: 10.1.2
Release: 1%{?dist}
Summary: Media server providing ubiquitous music access
Group: System Environment/Daemons
License: GPLv3+
URL: https://airsonic.github.io/
Source0: https://github.com/airsonic/airsonic/releases/download/v%{version}/airsonic.war
Source1: airsonic.service
Requires: java-1.8.0-openjdk-headless
%{?systemd_requires}

%description
Airsonic is a free, web-based media streamer, providing ubiquitous access to
your music. Use it to share your music with friends, or to listen to your own
music while at work. You can stream to multiple players simultaneously, for
instance to one player in your kitchen and another in your living room.


%prep
# Nope :-)


%build
# Nope (bis)


%install
mkdir -p %{buildroot}/var/lib/airsonic
install -p -m 0644 -D %{SOURCE0} %{buildroot}/usr/share/airsonic/airsonic.war
# Service
install -p -m 0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/airsonic.service


%pre
/usr/bin/getent group airsonic >/dev/null || /usr/sbin/groupadd -r airsonic
if ! /usr/bin/getent passwd airsonic >/dev/null; then
  /usr/sbin/useradd -r -g airsonic -M -N -d /var/lib/airsonic \
    -s /sbin/nologin -c "Airsonic" airsonic
fi

%post
%systemd_post airsonic.service

%preun
%systemd_preun airsonic.service

%postun
%systemd_postun_with_restart airsonic.service


%files
%{_unitdir}/airsonic.service
/usr/share/airsonic/airsonic.war
%dir %attr(0755,airsonic,airsonic) /var/lib/airsonic


%changelog
* Thu Aug  9 2018 Matthias Saou <matthias@saou.eu> 10.1.2-1
- Initial RPM release.

