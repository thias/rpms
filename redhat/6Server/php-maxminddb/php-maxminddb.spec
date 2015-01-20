%global gh_commit    cbd695a5309c15249ef5944997cfb71f2a8a7963
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     maxmind
%global gh_project   MaxMind-DB-Reader-php
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

%{!?php_inidir:  %global php_inidir       %{_sysconfdir}/php.d}

%global ext_name     maxminddb

%if "%{php_version}" < "5.6"
%global ini_name  %{ext_name}.ini
%else
%global ini_name  40-%{ext_name}.ini
%endif

Name:           php-%{ext_name}
Summary:        API for reading MaxMind DB files
Version:        1.0.2
Release:        1%{?dist}

URL:            http://www.maxmind.com/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/v%{version}.tar.gz
License:        BSD
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  libmaxminddb-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

Provides:       php-composer(maxmind-db/reader) = %{version}


%description
This is the PHP API for reading MaxMind DB files. MaxMind DB is a binary
file format that stores data indexed by IP address subnets (IPv4 or IPv6).


%prep
%setup -q -n %{gh_project}-%{version}


%build
cd ext
%{_bindir}/phpize
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C ext install INSTALL_ROOT=%{buildroot}
mkdir -p %{buildroot}%{php_inidir}
cat > %{buildroot}%{php_inidir}/%{ini_name} << EOF
; Enable MaxMind DB extension module
extension=%{ext_name}.so
EOF


%check
%if %{with_tests}
make -C ext test
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.md examples
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so


%changelog
* Tue Jan 20 2015 Matthias Saou <matthias@saou.eu> 1.0.2-1
- Update to 1.0.2.

* Mon Jan 12 2015 Matthias Saou <matthias@saou.eu> 1.0.0-2
- Fix phpinfo() reported version from 0.2.0 to 1.0.0.

* Tue Dec 30 2014 Matthias Saou <matthias@saou.eu> 1.0.0-1
- Initial RPM release.

