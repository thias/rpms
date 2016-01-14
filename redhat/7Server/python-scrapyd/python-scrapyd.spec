%global pypi_name       scrapyd
%global scrapyd_user    scrapyd
%global scrapyd_group   scrapyd

Name:       python-scrapyd
Version:    1.1.0
Release:    1%{?dist}
Summary:    Service for running Scrapy spiders, with an HTTP API

License:    BSD
URL:        https://github.com/scrapy/scrapyd
Source0:    https://pypi.python.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source10:   000-default
Source11:   scrapyd.service
Source12:   scrapyd.logrotate

BuildArch:          noarch
Requires:           python-twisted
Requires:           python-scrapy
BuildRequires:      python2-devel
BuildRequires:      python-twisted
BuildRequires:      python-setuptools
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Provides:           scrapyd = %{version}-%{release}

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
install -p -D -m 0644 %{SOURCE10} \
  %{buildroot}/etc/scrapyd/conf.d/000-default
install -p -D -m 0644 %{SOURCE11} \
  %{buildroot}%{_unitdir}/scrapyd.service
# As of 1.1.0, USR1 does nothing... :-(
#install -p -D -m 0644 %{SOURCE12} \
#  %{buildroot}%{_sysconfdir}/logrotate.d/scrapyd
mkdir -p %{buildroot}/var/lib/scrapyd/{eggs,dbs,items}
mkdir -p %{buildroot}/var/log/scrapyd

%pre
getent group %{scrapyd_group} > /dev/null || groupadd -r %{scrapyd_group}
getent passwd %{scrapyd_user} > /dev/null || \
  useradd -r -d /var/lib/scrapyd -g %{scrapyd_group} \
  -s /sbin/nologin -c "Scrapy Daemon" %{scrapyd_user}
exit 0

%post
%systemd_post scrapyd.service

%preun
%systemd_preun scrapyd.service

%postun
%systemd_postun scrapyd.service

%files
%doc LICENSE README.rst
%dir /etc/scrapyd
%dir /etc/scrapyd/conf.d
%config(noreplace) /etc/scrapyd/conf.d/000-default
#config(noreplace) %{_sysconfdir}/logrotate.d/scrapyd
%{_bindir}/scrapyd
%{_unitdir}/scrapyd.service
%{python_sitelib}/scrapyd
%{python_sitelib}/scrapyd-*.egg-info
%attr(-,scrapyd,scrapyd) /var/lib/scrapyd
%attr(-,scrapyd,scrapyd) /var/log/scrapyd

%changelog
* Thu Jan 14 2016 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Include user creation.
- Include systemd unit.

* Wed Oct 28 2015 Matthias Saou <matthias@saou.eu> 1.1.0-0
- Initial RPM release.

