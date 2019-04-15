%global srcname clickhouse-driver
%global eggname clickhouse_driver

Name: python-%{srcname}
Version: 0.0.19
Release: 1%{?dist}
Summary: ClickHouse Python Driver
License: MIT
URL: https://pypi.python.org/pypi/clickhouse-driver
Source0: %{pypi_source}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python-enum34
BuildRequires: python2-pytz
BuildRequires: python2-clickhouse-cityhash
BuildRequires: python2-zstd
BuildRequires: python2-lz4
#BuildRequires: python%{python3_pkgversion}-devel
#BuildRequires: python%{python3_pkgversion}-setuptools
#BuildRequires: python%{python3_pkgversion}-enum34
#BuildRequires: python%{python3_pkgversion}-pytz
#BuildRequires: python%{python3_pkgversion}-clickhouse-cityhash
#BuildRequires: python%{python3_pkgversion}-zstd
#BuildRequires: python%{python3_pkgversion}-lz4
BuildArch: noarch

%description
ClickHouse Python Driver with native (TCP) interface support.


%package -n python2-%{srcname}
Summary: %{summary}
Requires: python-enum34
Requires: python2-pytz
Requires: python2-clickhouse-cityhash
Requires: python2-zstd
Requires: python2-lz4
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
ClickHouse Python Driver with native (TCP) interface support.


%package -n python%{python3_pkgversion}-%{srcname}
Summary: %{summary}
Requires: python%{python3_pkgversion}-enum34
Requires: python%{python3_pkgversion}-pytz
Requires: python%{python3_pkgversion}-clickhouse-cityhash
Requires: python%{python3_pkgversion}-zstd
Requires: python%{python3_pkgversion}-lz4
BuildRequires: python%{python3_pkgversion}-devel
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
ClickHouse Python Driver with native (TCP) interface support.


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
#py3_build

%install
%py2_install
#py3_install

%check
#{__python2} setup.py test
#{__python3} setup.py test


%files -n python2-%{srcname}
%doc README.rst
%{python2_sitelib}/%{eggname}-*.egg-info/
%{python2_sitelib}/%{eggname}/


#files -n python%{python3_pkgversion}-%{srcname}
#doc README.rst
#{python3_sitelib}/%{eggname}-*.egg-info/
#{python3_sitelib}/%{eggname}/


%changelog
* Mon Apr 15 2019 Matthias Saou <matthias@saou.eu> 0.0.19-1
- Initial RPM release.

