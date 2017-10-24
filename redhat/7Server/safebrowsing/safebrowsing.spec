%global ghlcommit ce39ae7e50e719c4518fcac8a81032c2f43046aa
%global ghscommit ce39ae7
%global daemon_name sbserver

Name:		safebrowsing
Version:	0
Release:	3.%{ghscommit}%{?dist}
Summary:	Google Safe Browsing Proxy Server and CLI Lookup

Group:		Applications/Internet
License:	ASL 2.0
URL:		https://github.com/google/safebrowsing
# Created by prep-packages.sh
Source0:    safebrowsing-%{ghscommit}.tar.gz
Source1:    safebrowsing-packages.tar.gz
Source2:    %{daemon_name}.service
Source3:    %{daemon_name}.sysconfig

BuildRequires:	golang
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
The sbserver server binary runs a Safe Browsing API lookup proxy that allows
users to check URLs via a simple JSON API. The server also runs an URL
redirector to show an interstitial for anything marked unsafe.
The interstitial shows warnings recommended by Safe Browsing.

The sblookup command-line binary is another example of how the Go Safe
Browsing library can be used to protect users from unsafe URLs.
This command-line tool filters unsafe URLs piped via STDIN.


%prep
%setup -q -a 1 -n safebrowsing-%{ghscommit}
mv safebrowsing-packages _build
mkdir -p _build/src/github.com/google
ln -s $(pwd) _build/src/github.com/google/safebrowsing


%build
export GOPATH=$(pwd)/_build
# Workaround for missing build id which makes debuginfo extraction fail
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -v -o sbserver github.com/google/safebrowsing/cmd/sbserver
gobuild -a -v -o sblookup github.com/google/safebrowsing/cmd/sblookup


%install
install -D -p -m 0755 sbserver %{buildroot}%{_bindir}/sbserver
install -D -p -m 0755 sblookup %{buildroot}%{_bindir}/sblookup
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{daemon_name}
install -d -m 0770 %{buildroot}/var/lib/%{daemon_name}


%pre
getent group %{daemon_name} >/dev/null || groupadd -r %{daemon_name}
getent passwd %{daemon_name} >/dev/null || \
  useradd -r -d /var/lib/%{daemon_name} -g %{daemon_name} \
  -s /sbin/nologin -c "Google Safe Browsing Proxy Server" %{daemon_name}

%post
%systemd_post %{daemon_name}.service

%preun
%systemd_preun %{daemon_name}.service

%postun
%systemd_postun_with_restart %{daemon_name}.service

%files
%license LICENSE
%doc README.md
%{_unitdir}/%{daemon_name}.service
%config(noreplace) %attr(0640,root,%{daemon_name}) %{_sysconfdir}/sysconfig/%{daemon_name}
%{_bindir}/sbserver
%{_bindir}/sblookup
%attr(0775,root,%{daemon_name}) /var/lib/%{daemon_name}


%changelog
* Tue Oct 24 2017 Matthias Saou <matthias@saou.eu> 0-3.ce39ae7
- Relax permissions of the data directory, nothing critical there.

* Mon Nov  7 2016 Matthias Saou <matthias@saou.eu> 0-2.20160823
- Relax permissions of the data directory, nothing critical there.

* Tue Oct  4 2016 Matthias Saou <matthias@saou.eu> 0-1.20160823
- Initial RPM release.

