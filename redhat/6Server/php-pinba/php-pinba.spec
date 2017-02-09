Summary:       PHP extension for Pinba
Name:          php-pinba
Version:       1.1.0
Release:       1%{?dist}
License:       PHP License
Group:         Development/Languages
URL:           http://pinba.org/
Source:        https://github.com/tony2001/pinba_extension/archive/RELEASE_1_1_0.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
BuildRequires: php-devel
BuildRequires: protobuf-devel

%description
Pinba is a realtime monitoring/statistics server for PHP using MySQL as a
read-only interface. It accumulates and processes data sent over UDP by
multiple PHP processes and displays statistics in a nice human-readable form
of simple "reports", also providing read-only interface to the raw data in
order to make possible generation of more sophisticated reports and stats.

With this Pinba extension, users also can measure particular parts of the
code using timers with arbitrary tags.

Pinba is not a debugging tool in a common sense, since you're not supposed
to do debugging on production servers, but its main goal is to help
developers to monitor performance of PHP scripts, locate bottlenecks in
realtime and direct developers' attention to the code that really needs it. 

%prep
%setup -q -n pinba_extension-RELEASE_1_1_0

%build
%{_bindir}/phpize
%configure --with-pinba
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

%{__rm} -rf %{buildroot}/%{_includedir}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/pinba.ini << 'EOF'
; Enable pinba extension module
extension=pinba.so
pinba.enabled=1
pinba.server=127.0.0.1:30002
EOF

%check
# Check if the built extension can be loaded
%{_bindir}/php \
    -n -q -d extension_dir=modules \
    -d extension=pinba.so \
    --modules | grep pinba

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%config(noreplace) %{_sysconfdir}/php.d/pinba.ini
%{php_extdir}/pinba.so

%changelog
* Wed Feb  8 2017 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Update to 1.1.0 final.

* Sat Sep 24 2011 Builder <builder@local> 77:0.0.6-1
- no changelogs

