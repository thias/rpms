# ClickHouse - See https://clickhouse.yandex/
#
# https://github.com/yandex/ClickHouse/blob/master/doc/build.md
# https://clickhouse.yandex/reference_en.html#Installation
#
# This spec file requires custom RHEL/CentOS 7 (re)builds in order to build
# with GCC 6.x against many static libraries.
#
# Originally deb-specific, the build logic has been extracted from the
# 'release' script and the 'debian/*' files.


# cat debian/daemons
%global daemons compressor clickhouse-client clickhouse-server clickhouse-benchmark config-processor
%global daemon_name clickhouse-server
%global daemon_user clickhouse
%global revision 54030

# FIXME: Find out why this gets in, and remove it cleanly
%global __requires_exclude GLIBC_PRIVATE


Name: clickhouse
Version: 1.1.%{revision}
Release: 1%{?dist}
Summary: Column-oriented database management system
Group: Applications/Databases
License: ASL 2.0
URL: https://clickhouse.yandex/
Source0: https://github.com/yandex/ClickHouse/archive/v%{version}-stable.tar.gz
Source1: clickhouse-server.service
Patch0: ClickHouse-1.1.54022-stable-mysqlxx.patch
Patch1: ClickHouse-1.1.54022-stable-readline.patch
Patch2: ClickHouse-1.1.54030-stable-less-static.patch

# These are tough ones on RHEL7, tricky (re)builds, but not impossible!
BuildRequires: gcc >= 6.2.0
BuildRequires: libtool-ltdl-static%{?_isa}
BuildRequires: boost-static%{?_isa} >= 1.57
BuildRequires: mariadb-static%{?_isa}

# These are the RHEL provided ones
BuildRequires: cmake
BuildRequires: glib2-devel%{?_isa}
BuildRequires: libicu-devel%{?_isa}
BuildRequires: libstdc++-static%{?_isa}
BuildRequires: openssl-devel%{?_isa}
BuildRequires: readline-devel%{?_isa}
BuildRequires: unixODBC-devel%{?_isa}
BuildRequires: zlib-devel%{?_isa}

Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: systemd


%description
ClickHouse is an open-source column-oriented database management system that
allows generating analytical data reports in real time.

%package server
Summary: ClickHouse column-oriented database management system server

%description server
ClickHouse is an open-source column-oriented database management system that
allows generating analytical data reports in real time.
This package contains the ClickHouse Server.


%package client
Summary: ClickHouse column-oriented database management system client

%description client
ClickHouse is an open-source column-oriented database management system that
allows generating analytical data reports in real time.
This package contains the ClickHouse Client.


%package utils
Summary: ClickHouse column-oriented database management utilities

%description utils
ClickHouse is an open-source column-oriented database management system that
allows generating analytical data reports in real time.
This package contains the ClickHouse utilities.


%prep
%setup -q -n ClickHouse-%{version}-stable
%patch0 -p1
%patch1 -p1
%patch2 -p1
# Set proper revision, the included git command fails with release tarballs
sed -i -e 's|77777|%{revision}|' libs/libcommon/src/create_revision.sh


%build
export DISABLE_MONGODB=1
export GLIBC_COMPATIBILITY=1
mkdir build
cd build
cmake ..
make %{?_smp_mflags}
cd ..


%install
cd build
for daemon in %{daemons}; do
  DESTDIR=%{buildroot} cmake -DCOMPONENT=$daemon -P cmake_install.cmake
done
cd ..
# We don't want these
rm -f %{buildroot}%{_sysconfdir}/security/limits.d/metrika.conf
# Data and log directories
mkdir -p %{buildroot}/var/lib/clickhouse/{data/default,metadata/default,tmp}
mkdir -p %{buildroot}/var/log/%{daemon_name}
# Service file, replace legacy init.d script
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{daemon_name}.service
rm -f %{buildroot}%{_sysconfdir}/init.d/%{daemon_name}
# Update default configuration
sed -i -e 's|/opt/clickhouse|/var/lib/clickhouse|g; /listen_host/s|::|::1|' \
  %{buildroot}%{_sysconfdir}/clickhouse-server/config.xml


%pre server
/usr/sbin/groupadd -r %{daemon_user} >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g %{daemon_user} -r -d /var/lib/clickhouse \
  -s /sbin/nologin -c "ClickHouse Server" %{daemon_user} >/dev/null 2>&1 || :

%post server
%systemd_post %{daemon_name}.service

%preun server
%systemd_preun %{daemon_name}.service

%postun server
# Don't restart the server automatically
%systemd_postun %{daemon_name}.service


%files server
%license LICENSE
%doc README.md
%attr(0755,%{daemon_user},%{daemon_user}) %dir %{_sysconfdir}/clickhouse-server/
%attr(0644,%{daemon_user},%{daemon_user}) %config(noreplace) %{_sysconfdir}/clickhouse-server/config.xml
%attr(0644,%{daemon_user},%{daemon_user}) %config(noreplace) %{_sysconfdir}/clickhouse-server/users.xml
%{_bindir}/clickhouse-server
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/data/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/data/default/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/metadata/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/metadata/default/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/lib/clickhouse/tmp/
%attr(0750,%{daemon_user},%{daemon_user}) %dir /var/log/%{daemon_name}/
%{_unitdir}/%{daemon_name}.service


%files client
%license LICENSE
%dir %{_sysconfdir}/clickhouse-client/
%config(noreplace) %{_sysconfdir}/clickhouse-client/config.xml
%{_bindir}/clickhouse-client


%files utils
%license LICENSE
%{_bindir}/clickhouse-benchmark
%{_bindir}/compressor
%{_bindir}/config-processor


%changelog
* Mon Nov  7 2016 Matthias Saou <matthias@saou.eu> 1.1.54030-1
- Update to 1.1.54030-stable.

* Tue Oct 11 2016 Matthias Saou <matthias@saou.eu> 1.1.54022-3
- Dynamically link openssl, glib2, icu, glibc and zlib.
- Set proper revision for the built binaries.
- Remove init.d conditional, systemd only now.

* Mon Oct 10 2016 Matthias Saou <matthias@saou.eu> 1.1.54022-2
- Try GLIBC_COMPATIBILITY=1 but build fails on sqlite errors.
- Filter requirements because of libpthread.so.0(GLIBC_PRIVATE)(64bit).
- Switch to more generic 'clickhouse' user and group.
- Include systemd service now.
- Remove limits.d file, the systemd service takes care of that.
- Use /var/lib/clickhouse as the default data path.
- Listen on loopback only by default.

* Thu Oct  6 2016 Matthias Saou <matthias@saou.eu> 1.1.54022-1
- Initial RPM release.
