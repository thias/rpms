%global pypi_name scrapyd

Name:       python-scrapyd
Version:    1.1.0
Release:    0%{?dist}
Summary:    Service for running Scrapy spiders, with an HTTP API

License:    BSD
URL:        https://github.com/scrapy/scrapyd
Source0:    https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:  noarch
Requires:   python-twisted
Requires:   python-scrapy
BuildRequires:  python2-devel
BuildRequires:  python-twisted
BuildRequires:  python-setuptools

%description
Scrapyd is a service for running Scrapy spiders.
It allows you to deploy your Scrapy projects and control their spiders using
a HTTP JSON API.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg
rm -rf scrapyd.egg-info

%build
%{__python2} setup.py build
#PYTHONPATH=$(pwd) make -C docs html

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc LICENSE README.rst
%{python_sitelib}/scrapyd
%{python_sitelib}/scrapyd-*.egg-info
%{_bindir}/scrapyd

%changelog
* Wed Oct 28 2015 Matthias Saou <matthias@saou.eu> 1.1.0-0
- Initial RPM release.

