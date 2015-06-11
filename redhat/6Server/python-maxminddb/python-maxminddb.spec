%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           python-maxminddb
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python module for reading MaxMind DB files

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-maxminddb
Source0:        https://pypi.python.org/packages/source/m/maxminddb/maxminddb-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  libmaxminddb-devel

%description
This is a Python module for reading MaxMind DB files.
The module includes the C extension.


%prep
%setup -q -n maxminddb-%{version}
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
%{python2_sitearch}/maxminddb/
%{python2_sitearch}/maxminddb*.egg-info

%changelog
* Thu Jun 11 2015 Matthias Saou <matthias@saou.eu> 1.2.0-1
- Initial RPM release.

