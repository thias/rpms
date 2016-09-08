Summary:       Tideways PHP Profiler Extension
Name:          php-tideways
Version:       4.0.5
Release:       1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:       ASL 2.0
Group:         Development/Languages
URL:           https://github.com/tideways/php-profiler-extension
Source:        https://github.com/tideways/php-profiler-extension/archive/v%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
BuildRequires: php-devel

%description
The Profiler extension contains functions for finding performance bottlenecks
in PHP code. The extension is one core piece of functionality for the
Tideways Profiler Platform. It solves the problem of efficiently collecting,
aggregating and analyzing the profiling data when running a Profiler in
production.


%prep
%setup -q -n php-profiler-extension-%{version}


%build
phpize
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
mkdir -p %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/60-tideways.ini << 'EOF'
; Enable tideways extension module
extension=tideways.so
tideways.auto_prepend_library=0
EOF


%check
make test
# Check if the built extension can be loaded
php \
  -n -q -d extension_dir=modules \
  -d extension=tideways.so \
  --modules | grep tideways


%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/php.d/60-tideways.ini
%{php_extdir}/tideways.so


%changelog
* Thu Sep  1 2016 Matthias Saou <matthias@saou.eu> 4.0.5-1
- Initial RPM release.

