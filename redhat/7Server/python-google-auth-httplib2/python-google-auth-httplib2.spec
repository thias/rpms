Name:       python-google-auth-httplib2
Version:    0.0.2
Release:    1%{?dist}
Summary:    httplib2 Transport for Google Auth

License:    ASL 2.0
URL:        https://github.com/GoogleCloudPlatform/google-auth-library-python-httplib2
#Source0:    https://github.com/GoogleCloudPlatform/google-auth-library-python-httplib2/archive/%{version}.tar.gz/google-auth-library-python-httplib2-%{version}.tar.gz
Source0:    https://github.com/GoogleCloudPlatform/google-auth-library-python-httplib2/archive/136da2c.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools
Requires:           python-google-auth
Requires:           python-httplib2 >= 0.9.1

%description
This library provides an httplib2 transport for google-auth.

%prep
#setup -q -n google-auth-library-python-httplib2-%{version}
%setup -q -n google-auth-library-python-httplib2-136da2cd50aa7deb769062cf1d77259d64743a7f

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python_sitelib}/google_auth_httplib2.py*
%{python_sitelib}/google_auth_httplib2-*.egg-info

%changelog
* Wed Jun 14 2017 Matthias Saou <matthias@saou.eu> 0.0.2-1
- Initial RPM release.

