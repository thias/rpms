# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%{?scl:          %scl_package         php-FiftyOneDegreesTrieV3}

%global gh_commit   313ebe792b61af17c31b3a782b1d6c3b48038753
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    51Degrees
%global gh_project  Device-Detection
%global pecl_name   FiftyOneDegreesTrieV3
%global with_zts    0%{?_with_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

Summary:       Client extension for 51Degrees Device-Detection
Name:          %{?scl_prefix}php-FiftyOneDegreesTrieV3
Version:       3.2.15.2
%if 0%{?gh_date:1}
Release:       0.1.%{gh_date}git%{gh_short}%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%else
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%endif
License:       MPLv2.0
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel > 7
#BuildRequires: %{?scl_prefix}php-tokenizer

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Client extension for 51Degrees Device-Detection.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
cd %{gh_project}-%{gh_commit}/php
mv trie NTS

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension = %{pecl_name}.so

; Configuration
FiftyOneDegreesTrieV3.data_file = ''
FiftyOneDegreesTrieV3.property_list = 'BrowserName,BrowserVendor,BrowserVersion,DeviceType,HardwareVendor'
EOF


%build
%{?dtsenable}
cd %{gh_project}-%{gh_commit}/php

cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    PHP7=1
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    PHP7=1
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}
cd %{gh_project}-%{gh_commit}/php

# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif



%check
cd %{gh_project}-%{gh_commit}/php
cd NTS
: Minimal load test for NTS extension
#%{__php} -c ../%{ini_name} --modules | grep %{pecl_name}
#%{__php} --no-php-ini \
#    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
#    --modules | grep %{pecl_name}

#: Upstream test suite  for NTS extension
#TEST_PHP_EXECUTABLE=%{__php} \
#TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
#NO_INTERACTION=1 \
#REPORT_EXIT_STATUS=1 \
#%{__php} -n run-tests.php --show-diff || : ignore

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

#: Upstream test suite  for ZTS extension
#TEST_PHP_EXECUTABLE=%{__ztsphp} \
#TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
#NO_INTERACTION=1 \
#REPORT_EXIT_STATUS=1 \
#%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%{!?_licensedir:%global license %%doc}
#license NTS/LICENSE
#doc NTS/{CREDITS,NEWS,README}

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Apr  2 2019 Matthias Saou <matthias@saou.eu> 3.2.15.2-1
- Initial RPM release.

