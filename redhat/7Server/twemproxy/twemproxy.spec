Name: twemproxy
Version: 0.4.1
Release: 0%{?dist}
Summary: Fast and lightweight proxy for memcached and twemproxy protocols
Group: System Environment/Daemons
License: ASL 2.0
URL: https://github.com/twitter/twemproxy
Source0: https://github.com/twitter/twemproxy/archive/v0.4.1.tar.gz
Source1: twemproxy.service
Patch0: twemproxy-0.4.1-nutcracker-rename.patch
Patch1: twemproxy-0.4.1-conf_path.patch
BuildRequires: autoconf, automake, libtool
BuildRequires: systemd-units
# FIXME : Uses bundled yaml-0.1.4 in contrib directory
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and
lightweight proxy for memcached and twemproxy protocol. It was built primarily
to reduce the number of connections to the caching servers on the backend.
This, together with protocol pipelining and sharding enables you to
horizontally scale your distributed caching architecture.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Rename files
rename nutcracker twemproxy conf/*.yml man/*.8


%build
autoreconf -fvi
%configure
make %{?_smp_mflags}


%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
echo "#OPTIONS=" > %{buildroot}%{_sysconfdir}/sysconfig/twemproxy
touch %{buildroot}%{_sysconfdir}/twemproxy.yml
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/twemproxy.service


%pre
getent group twemproxy &>/dev/null || \
groupadd -r twemproxy &>/dev/null
getent passwd twemproxy &>/dev/null || \
useradd -r -g twemproxy -d / -s /sbin/nologin \
  -c 'twemproxy' twemproxy &>/dev/null
exit 0

%post
%systemd_post twemproxy.service

%preun
%systemd_preun twemproxy.service

%postun
%systemd_postun_with_restart twemproxy.service


%files
%license LICENSE
%doc ChangeLog NOTICE README.md notes/
%ghost %config %{_sysconfdir}/twemproxy.yml
%config(noreplace) %{_sysconfdir}/sysconfig/twemproxy
%{_sbindir}/twemproxy
%{_mandir}/man8/twemproxy.8*
%{_unitdir}/twemproxy.service


%changelog
* Thu Jun 23 2016 Matthias Saou <matthias@saou.eu> 0.4.1-1
- Initial RPM release.

