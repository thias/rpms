Name:       python-google-cloud
Version:    0.25.0
Release:    1%{?dist}
Summary:    Python idiomatic client for Google Cloud Platform services

License:    ASL 2.0
URL:        https://github.com/GoogleCloudPlatform/google-cloud-python
Source0:    https://github.com/GoogleCloudPlatform/google-cloud-python/archive/%{version}.tar.gz/google-cloud-python-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:      python-setuptools
Requires:           python-setuptools
# Technically, not all modules require it, but many/most do
Requires:           python-google-auth
Requires:           protobuf-python >= 3.0.0
# bigquery
Requires:           python-google-auth-httplib2
# Old name
Obsoletes:          python-gcloud <= 0.10.1

%description
Python idiomatic client for Google Cloud Platform services.

%prep
%setup -q -n google-cloud-python-%{version}
rm -rf test_utils

%build
for dir in . *; do
  [ -f ${dir}/setup.py ] || continue
  cd $dir
  python2 setup.py build
  cd -
done

%install
for dir in . *; do
  [ -f ${dir}/setup.py ] || continue
  cd $dir
  python2 setup.py install --skip-build --root %{buildroot}
  cd -
done
# FIXME : Not sure why the . install doesn't create this?
touch %{buildroot}%{python_sitelib}/google/cloud/__init__.py

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.rst README.rst
%{python_sitelib}/google/
%{python_sitelib}/google_cloud*.egg-info
%exclude %{python_sitelib}/google_cloud*-nspkg.pth

%changelog
* Wed Jun 14 2017 Matthias Saou <matthias@saou.eu> 0.25.0-1
- Rename from python-gcloud to python-google-cloud to match upstream rename.
- Update to 0.25.0.

* Tue Mar  1 2016 Matthias Saou <matthias@saou.eu> 0.10.1-1
- Initial RPM release.

