Name:       docker-distribution-auth
Version:    1.2
Release:    1%{?dist}
Summary:    Docker Registry 2 authentication server

License:    ASL 2.0
URL:        https://github.com/cesanta/docker_auth
Source0:    https://github.com/cesanta/docker_auth/archive/%{version}.tar.gz
Source1:    docker_auth-packages.tar.gz
Source2:    docker-distribution-auth.service
Patch0:     docker_auth-1.2.patch

BuildRequires: golang
%{?systemd_requires}
BuildRequires: systemd

%description
Authentication server implementing the Docker Registry 2.0 token-based
authentication and authorization protocol.


%prep
%setup -q -n docker_auth-%{version} -a 1
%patch0 -p1
mv docker_auth-packages _build
cat > auth_server/version.go << EOF
package main
const (
	Version = "%{version}"
	BuildId = "RPM %{version}-%{release}"
)
EOF


%build
mkdir -p _build/src/github.com/cesanta/docker_auth
ln -s $PWD/auth_server _build/src/github.com/cesanta/docker_auth/auth_server
export GOPATH=$PWD/_build
# Workaround for missing build id which makes debuginfo extraction fail
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
gobuild -a -o docker_auth github.com/cesanta/docker_auth/auth_server


%install
install -D -m 0755 docker_auth \
  %{buildroot}%{_bindir}/docker-distribution-auth
install -D -m 0644 -p %{SOURCE2} \
  %{buildroot}%{_unitdir}/docker-distribution-auth.service
mkdir -p %{buildroot}/etc/docker-distribution/auth
cat > %{buildroot}/etc/docker-distribution/auth/config.yml << EOF
# See /usr/share/doc/docker-distribution-auth-*/examples/ files.
EOF


%pre
/usr/bin/getent group dockauth >/dev/null || /usr/sbin/groupadd -r dockauth
if ! /usr/bin/getent passwd dockauth >/dev/null; then
  /usr/sbin/useradd -r -g dockauth -M -N -d / -s /sbin/nologin -c "Docker Distribution Auth" dockauth
fi

%post
%systemd_post docker-distribution-auth.service

%preun
%systemd_preun docker-distribution-auth.service

%postun
%systemd_postun_with_restart docker-distribution-auth.service


%files
%license LICENSE
%doc examples docs/Backend_MongoDB.md README.md
%dir /etc/docker-distribution/
%dir /etc/docker-distribution/auth
%config(noreplace) /etc/docker-distribution/auth/config.yml
%{_bindir}/docker-distribution-auth
%{_unitdir}/docker-distribution-auth.service


%changelog
* Mon Feb 27 2017 Matthias Saou <matthias@saou.eu> 1.2-1
- Initial RPM release.

