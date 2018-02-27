Name:       python-ns1
Version:    0.9.17
Release:    1%{?dist}
Summary:    NS1 Python SDK

License:    MIT
URL:        https://pypi.python.org/pypi/ns1-python
Source0:    https://pypi.python.org/packages/b8/37/1fef95fd419cb14d9b6ac713759e2a1311f60174175c3c329f54aa615ef1/ns1-python-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python2-setuptools
BuildRequires:      python2-pytest-runner

%description
NS1 REST API wrapper as well as a higher level interface for managing zones,
records, data feeds, and more. It supports synchronous and asynchronous
transports.

%prep
%setup -q -n ns1-python-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%{python_sitelib}/ns1/
%{python_sitelib}/ns1_python-*.egg-info

%changelog
* Mon Feb 26 2018 Matthias Saou <matthias@saou.eu> 0.9.17-1
- Initial RPM release.

