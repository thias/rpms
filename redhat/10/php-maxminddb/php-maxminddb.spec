# remirepo spec file for php-maxminddb
#
# SPDX-FileCopyrightText:  Copyright 2018-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%scl_package        php-maxminddb
%global with_lib    0
%else
%global pkg_name    %{name}
%global with_lib    1
%endif
%bcond_without       tests

%global gh_commit   2194f58d0f024ce923e685cdf92af3daf9951908
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    maxmind
%global gh_project  MaxMind-DB-Reader-php
# Extension
%global pie_vend    maxmind-db
%global pie_proj    reader-ext
%global pecl_name   maxminddb
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini
# pure PHP library
%global pk_vendor    maxmind-db
%global pk_project   reader
%global _configure   ../ext/configure

Summary:       MaxMind DB Reader extension
Name:          %{?scl_prefix}php-maxminddb
Version:       1.13.1
Release:       1%{?dist}
License:       Apache-2.0
URL:           https://github.com/%{gh_owner}/%{gh_project}

# keep using git snapshot to retrieve extension + library + test
Source0:       %{pkg_name}-%{version}-%{gh_short}.tgz
Source1:       makesrc.sh

BuildRequires: %{?scl_prefix}php-devel >= 7.2
BuildRequires: %{?scl_prefix}php-pear  >= 1.10
BuildRequires: pkgconfig(libmaxminddb) >= 1.0.0

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
# Weak dependencie on databasess
Recommends:    geolite2-country
Suggests:      geolite2-city

# PECL
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
# PIE
Provides:       %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:       %{?scl_prefix}php-%{pie_vend}-%{pie_proj} = %{version}


%description
MaxMind DB is a binary file format that stores data indexed by
IP address subnets (IPv4 or IPv6).

This optional PHP C Extension is a drop-in replacement for
MaxMind\Db\Reader.

Databases are available in geolite2-country and geolite2-city packages.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%if %{with_lib}
%package -n php-%{pk_vendor}-%{pk_project}
Summary:       MaxMind DB Reader

BuildArch:     noarch
BuildRequires: php-fedora-autoloader-devel
%if %{with tests}
BuildRequires: php-bcmath
BuildRequires: php-gmp
# from composer.json "require-dev": {
#        "friendsofphp/php-cs-fixer": "*",
#        "phpunit/phpunit": ">=8.0.0,<10.0.0",
#        "php-coveralls/php-coveralls": "^2.1",
#        "phpunit/phpcov": ">=6.0.0",
#        "squizlabs/php_codesniffer": "3.*"
BuildRequires: phpunit8
%endif

# from composer.json "require": {
#        "php": ">=7.2"
Requires:      php(language) >= 7.2
# from composer.json "suggest": {
#        "ext-bcmath": "bcmath or gmp is required for decoding larger integers with the pure PHP decoder",
#        "ext-gmp": "bcmath or gmp is required for decoding larger integers with the pure PHP decoder",
#        "ext-maxminddb": "A C-based database decoder that provides significantly faster lookups"
Recommends:    php-bcmath
Recommends:    php-gmp
Recommends:    php-maxminddb
# Weak dependencies on databases
Recommends:    geolite2-country
Suggests:      geolite2-city
# from composer.json "conflict": {
#        "ext-maxminddb": "<1.11.1,>=2.0.0"
Conflicts:     php-maxminddb < %{version}
# From phpcompatifo report for 1.3.0
Requires:      php-filter
Requires:      php-spl
# Autoloader
Requires:      php-composer(fedora/autoloader)

Provides:      php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description -n php-%{pk_vendor}-%{pk_project}
MaxMind DB Reader PHP API.

MaxMind DB is a binary file format that stores data indexed by
IP address subnets (IPv4 or IPv6).

Databases are available in geolite2-country and geolite2-city packages.

The extension available in php-maxminddb package allow better
performance.

Autoloader: %{_datadir}/php/MaxMind/Db/Reader/autoload.php
%endif


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%if %{with_lib}
%{_bindir}/phpab \
    --template fedora \
    --output src/MaxMind/Db/Reader/autoload.php \
    src/MaxMind/Db
%endif

cd ext
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MAXMINDDB_VERSION/{s/.* "//;s/".*$//;p}'  php_maxminddb.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:-dev}.
   exit 1
fi
cd ..

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{pecl_name}' extension module
extension = %{pecl_name}.so
EOF


%build
%{?dtsenable}

cd ext
%{__phpize}
[ -f Makefile.global ] && GLOBAL=Makefile.global || GLOBAL=build/Makefile.global
sed -e 's/INSTALL_ROOT/DESTDIR/' -i $GLOBAL

cd ../NTS
%configure \
    --with-php-config=%{__phpconfig} \
    --with-libdir=%{_lib} \
    --with-maxminddb

%make_build

%if %{with_zts}
cd ../ZTS
%configure \
    --with-php-config=%{__ztsphpconfig} \
    --with-libdir=%{_lib} \
    --with-maxminddb

%make_build
%endif


%install
%{?dtsenable}
# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the NTS stuff
%make_install -C NTS
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
%make_install -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

%if %{with_lib}
mkdir -p                %{buildroot}%{_datadir}/php/MaxMind
cp -pr src/MaxMind/Db   %{buildroot}%{_datadir}/php/MaxMind/Db
%endif


%check
ret=0

cd ext
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q --show-diff || ret=1

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

: Upstream test suite for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php -q --show-diff || ret=1
%endif

%if %{with_lib} && %{with tests}
cd ..
: Upstream test suite for the library
for cmd in php php81 php82 php83 php84 php85; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit8 \
      --bootstrap %{buildroot}%{_datadir}/php/MaxMind/Db/Reader/autoload.php \
      --verbose || ret=1
  fi
done

: Upstream test suite for the library with the extension
php --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
  %{_bindir}/phpunit8 \
    --bootstrap %{buildroot}%{_datadir}/php/MaxMind/Db/Reader/autoload.php \
    --verbose || ret=1
%endif
exit $ret


%files
%license LICENSE
%doc *.md
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%if %{with_lib}
%files -n php-%{pk_vendor}-%{pk_project}
%license LICENSE
%doc composer.json
%doc *.md
%dir %{_datadir}/php/MaxMind
     %{_datadir}/php/MaxMind/Db
%endif

# when using pkgup, CHECK Release!

%changelog
* Sat Nov 22 2025 Remi Collet <remi@remirepo.net> - 1.13.1-1
- update to 1.13.1 (no changes)
- add pie virtual provides

* Fri Nov 21 2025 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0

* Tue May  6 2025 Remi Collet <remi@remirepo.net> - 1.12.1-1
- update to 1.12.1
- re-license spec file to CECILL-2.1

* Fri Nov 15 2024 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Mon Dec  4 2023 Remi Collet <remi@remirepo.net> - 1.11.1-1
- update to 1.11.1

* Fri Sep 29 2023 Remi Collet <remi@remirepo.net> - 1.11.0-5
- add missing dependency on fedora/autoloader

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 1.11.0-4
- rebuild for PHP 8.3.0RC1

* Tue Jul 11 2023 Remi Collet <remi@remirepo.net> - 1.11.0-3
- build out of sources tree

* Fri Aug  5 2022 Remi Collet <remi@remirepo.net> - 1.11.0-2
- rebuild

* Tue Oct 19 2021 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 1.10.1-2
- rebuild for 8.1.0RC1

* Thu Apr 15 2021 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Wed Feb 10 2021 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0

* Fri Jan  8 2021 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0

* Fri Oct  2 2020 Remi Collet <remi@remirepo.net> - 1.8.0-2
- update to 1.8.0
- drop patches merged upstream

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 1.7.0-3
- rebuild for PHP 8.0.0RC1
- add patch for PHP 8.0.0rc1 from
  https://github.com/maxmind/MaxMind-DB-Reader-php/pull/109

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 1.7.0-2
- add patch for PHP 8.0.0beta3 from
  https://github.com/maxmind/MaxMind-DB-Reader-php/pull/108

* Sat Aug  8 2020 Remi Collet <remi@remirepo.net> - 1.7.0-1
- update to 1.7.0
- now available on pecl
- raise dependency on PHP 7.2
- switch to phpunit8

* Fri Dec 20 2019 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0

* Fri Dec 13 2019 Remi Collet <remi@remirepo.net> - 1.5.1-2
- update to 1.5.1
- drop patch merged upstream

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 1.5.0-3
- update to 1.5.0
- raise dependency on PHP 5.6
- add patch for old libmaxmindb in EL-6 from
  https://github.com/maxmind/MaxMind-DB-Reader-php/pull/90

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 1.4.1-2
- rebuild for 7.4.0RC1

* Sat Jan  5 2019 Remi Collet <remi@remirepo.net> - 1.4.1-1
- update to 1.4.1

* Wed Nov 21 2018 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0
- open https://github.com/maxmind/MaxMind-DB-Reader-php/issues/79
  to report test failure on 32-bit

* Wed Nov 14 2018 Remi Collet <remi@remirepo.net> - 1.3.0-3
- add php-maxmind-db-reader sub-package providing the library
- open https://github.com/maxmind/MaxMind-DB-Reader-php/issues/77
  to report test failures on 32-bit

* Thu Nov  8 2018 Remi Collet <remi@remirepo.net> - 1.3.0-2
- add upstream patches from merged PRs
- add weak dependencies on geolite2 databases

* Wed Nov  7 2018 Remi Collet <remi@remirepo.net> - 1.3.0-1
- new package, version 1.3.0
- open https://github.com/maxmind/MaxMind-DB-Reader-php/pull/73 pkg-config
- open https://github.com/maxmind/MaxMind-DB-Reader-php/pull/74 MINFO
- open https://github.com/maxmind/MaxMind-DB-Reader-php/pull/75 arginfo
