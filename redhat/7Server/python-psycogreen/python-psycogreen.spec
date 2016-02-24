%global pypi_name       psycogreen

Name:       python-psycogreen
Version:    1.0
Release:    1%{?dist}
Summary:    psycopg2 integration with coroutine libraries

License:    BSD
URL:        https://bitbucket.org/dvarrazzo/psycogreen
Source0:    https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools

%description
The psycogreen package enables psycopg2 to work with coroutine libraries,
using asynchronous calls internally but offering a blocking interface so that
regular code can run unmodified.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg
rm -rf %{pypi_name}.egg-info

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%license COPYING
%doc README.rst
%{python_sitelib}/%{pypi_name}/
%{python_sitelib}/%{pypi_name}-*.egg-info

%changelog
* Wed Feb 24 2016 Matthias Saou <matthias@saou.eu> 1.0-1
- Initial RPM release.

