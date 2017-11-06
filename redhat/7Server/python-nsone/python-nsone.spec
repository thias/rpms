Name:       python-nsone
Version:    0.9.16
Release:    1%{?dist}
Summary:    NSONE Python SDK

License:    MIT
URL:        https://pypi.python.org/pypi/nsone
Source0:    https://pypi.python.org/packages/source/n/nsone/nsone-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-setuptools
BuildRequires:      python2-pytest-runner

%description
Python SDK for accessing the NSONE DNS platform and includes both a simple
NSONE REST API wrapper as well as a higher level interface for managing
zones, records, data feeds, and more. It supports synchronous and asynchronous
transports.

%prep
%setup -q -n nsone-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%{python_sitelib}/nsone/
%{python_sitelib}/nsone-*.egg-info

%changelog
* Mon Nov  6 2017 Matthias Saou <matthias@saou.eu> 0.9.16-1
- Initial RPM release.

