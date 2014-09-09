%global commithash e53a39ce90d84668244f2f4c1f81938c695a3afd

Summary:       PHP extension for sending metrics to http://datadoghq.com/
Name:          php-datadog
Version:       0.0.0
Release:       1%{?dist}
License:       PHP License
Group:         Development/Languages
URL:           https://github.com/snappymob/php-datadog
Source:        https://github.com/mkoppanen/php-datadog/archive/%{commithash}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
BuildRequires: php-devel

%description
PHP extension for sending metrics to http://datadoghq.com/.


%prep
%setup -q -n %{name}-%{commithash}


%build
%{_bindir}/phpize
%configure --with-datadog
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}
# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/datadog.ini << 'EOF'
; Enable datadog extension module
extension=datadog.so
EOF


%check
# Check if the built extension can be loaded
%{_bindir}/php \
    -n -q -d extension_dir=modules \
    -d extension=datadog.so \
    --modules | grep datadog


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md examples/*
%config(noreplace) %{_sysconfdir}/php.d/datadog.ini
%{php_extdir}/datadog.so


%changelog
* Tue Sep  9 2014 Matthias Saou <matthias@saou.eu> 0.0.0-1
- Initial quick-n-dirty RPM package.

