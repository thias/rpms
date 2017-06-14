Name:       python-google-auth
Version:    1.0.1
Release:    1%{?dist}
Summary:    Google Auth Python Library

License:    ASL 2.0
URL:        https://github.com/GoogleCloudPlatform/google-auth-library-python
Source0:    https://github.com/GoogleCloudPlatform/google-auth-library-python/archive/%{version}.tar.gz/google-auth-library-python-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools
Requires:           python-setuptools
Requires:           python2-pyasn1 >= 0.1.7
Requires:           python2-pyasn1-modules >= 0.0.5
Requires:           python-rsa >= 3.1.4
Requires:           python-six >= 1.9.0
Requires:           python-cachetools >= 2.0.0

%description
This library simplifies using Google's various server-to-server
authentication mechanisms to access Google APIs.

%prep
%setup -q -n google-auth-library-python-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%doc CHANGELOG.rst CONTRIBUTING.rst CONTRIBUTORS.md README.rst
%{python_sitelib}/google/
%{python_sitelib}/google_auth*.egg-info
%exclude %{python_sitelib}/google_auth*-nspkg.pth

%changelog
* Wed Jun 14 2017 Matthias Saou <matthias@saou.eu> 1.0.1-1
- Initial RPM release.

