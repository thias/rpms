%global srcname clickhouse-cityhash
%global eggname clickhouse_cityhash

Name: python-%{srcname}
Version: 1.0.2.2
Release: 1%{?dist}
Summary: Python-bindings for CityHash, a fast non-cryptographic hash algorithm
License: MIT
URL: https://pypi.python.org/pypi/clickhouse-cityhash
Source0: %{pypi_source}

%description
A fork of Python wrapper around CityHash with downgraded version of algorithm.
This fork used as 3-rd party library for hashing data in ClickHouse protocol.


%package -n python2-%{srcname}
Summary: %{summary}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
#BuildRequires: python2-enum34
#BuildRequires: pytz
#{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A fork of Python wrapper around CityHash with downgraded version of algorithm.
This fork used as 3-rd party library for hashing data in ClickHouse protocol.


%package -n python3-%{srcname}
Summary: %{summary}
#BuildRequires: python3-devel
#{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A fork of Python wrapper around CityHash with downgraded version of algorithm.
This fork used as 3-rd party library for hashing data in ClickHouse protocol.


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
#py3_build

%install
%py2_install
#py3_install

%check
%{__python2} setup.py test
#{__python3} setup.py test


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/%{eggname}-*.egg-info/
%{python2_sitearch}/%{eggname}/


#files -n python3-%{srcname}
#license LICENSE
#doc README.rst
#{python3_sitearch}/%{eggname}-*.egg-info/
#{python3_sitearch}/%{eggname}/


%changelog
* Mon Apr 15 2019 Matthias Saou <matthias@saou.eu> 1.0.2.2-1
- Initial RPM release.

