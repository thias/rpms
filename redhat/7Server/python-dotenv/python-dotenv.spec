%global pypi_name python-dotenv

Name:       python-dotenv
Version:    0.1.3
Release:    1%{?dist}
Summary:    Add .env support to your django/flask apps in development and deployments
License:    BSD
URL:        https://github.com/theskumar/python-dotenv
Source0:    https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools
Requires:       python-click >= 5.0

%description
Reads the key,value pair from .env and adds them to environment variable.
It is great of managing app settings during development and in production
using 12-factor principles.

%prep
%setup -qn %{pypi_name}-%{version}
# Remove bundled egg
rm -rf python_dotenv.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
 
%files
%doc PKG-INFO
%{_bindir}/dotenv
%{python_sitelib}/dotenv*
%{python_sitelib}/python_dotenv-*.egg-info

%changelog
* Wed Sep  9 2015 Matthias Saou <matthias@saou.eu> 0.1.3-1
- Initial RPM release.

