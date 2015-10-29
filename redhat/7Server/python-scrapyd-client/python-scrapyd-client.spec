%global pypi_name scrapyd-client

Name:       python-scrapyd-client
Version:    1.0.1
Release:    0%{?dist}
Summary:    Client for scrapyd

License:    BSD
URL:        https://github.com/scrapy/scrapyd-client
Source0:    https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:  noarch
Requires:   python-scrapy
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Scrapyd-client is a client for scrapyd. It provides the scrapyd-deploy
utility which allows you to deploy your project to a Scrapyd server.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg
rm -rf scrapyd_client.egg-info

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%doc LICENSE README.rst
%{python_sitelib}/scrapyd-client
%{python_sitelib}/scrapyd_client-*.egg-info
%{_bindir}/scrapyd-deploy

%changelog
* Thu Oct 29 2015 Matthias Saou <matthias@saou.eu> 1.0.1-0
- Initial RPM release.

