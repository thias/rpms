%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-geoip2
Version:        2.1.0
Release:        1%{?dist}
Summary:        Python module for the GeoIP2 web services and databases

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/geoip2
Source0:        https://pypi.python.org/packages/source/g/geoip2/geoip2-%{version}.tar.gz

Requires:       python-maxminddb

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
This package provides an API for the GeoIP2 web services and databases.
The API also works with MaxMind’s free GeoLite2 databases.
The module includes the C extension.


%prep
%setup -q -n geoip2-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{python2_sitelib}/geoip2/
%{python2_sitelib}/geoip2*.egg-info

%changelog
* Mon Jun 15 2015 Matthias Saou <matthias@saou.eu> 2.1.0-1
- Initial RPM release.

