Name:       python-dyn
Version:    1.8.0
Release:    1%{?dist}
Summary:    Dyn API Python SDK

License:    BSD
URL:        https://pypi.python.org/pypi/dyn
Source0:    https://pypi.python.org/packages/source/d/dyn/dyn-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools

%description
This library provides an easily scriptable approach to accessing all of the
features provided by your Traffic Management (TM) or Message Management (MM)
services.

%prep
%setup -q -n dyn-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%doc HISTORY.rst README.rst
%{python_sitelib}/dyn/
%{python_sitelib}/dyn-*.egg-info

%changelog
* Mon Nov  6 2017 Matthias Saou <matthias@saou.eu> 1.8.0-1
- Update to 1.8.0.

* Tue Mar  8 2016 Matthias Saou <matthias@saou.eu> 1.6.2-1
- Update to 1.6.2 from pypi (no releases on github, it seems).

* Thu Mar  3 2016 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Initial RPM release.

