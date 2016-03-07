Name:       python-gcloud
Version:    0.11.0
Release:    1%{?dist}
Summary:    Python idiomatic client for Google Cloud Platform services

License:    ASL 2.0
URL:        https://github.com/GoogleCloudPlatform/gcloud-python
Source0:    https://github.com/GoogleCloudPlatform/gcloud-python/archive/%{version}.tar.gz/gcloud-python-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools
Requires:           python-setuptools
Requires:           python-httplib2 >= 0.9.1
Requires:           python-oauth2client >= 2.0.1
Requires:           protobuf-python >= 3.0.0
Requires:           pyOpenSSL
Requires:           python-six

%description
Python idiomatic client for Google Cloud Platform services.

%prep
%setup -q -n gcloud-python-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.rst README.rst
%{python_sitelib}/gcloud/
%{python_sitelib}/gcloud-*.egg-info

%changelog
* Tue Mar  1 2016 Matthias Saou <matthias@saou.eu> 0.10.1-1
- Initial RPM release.

