# remirepo spec file for php-pecl-mongodb
#
# SPDX-FileCopyrightText:  Copyright 2015-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%{?scl:%scl_package php-pecl-mongodb}

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pie_vend   mongodb
%global pie_proj   mongodb-extension
%global pecl_name  mongodb
# After 40-smbclient.ini, see https://jira.mongodb.org/browse/PHPC-658
%global ini_name   50-%{pecl_name}.ini

# test suite requires a MongoDB server
%bcond_with         tests

# always use bundled libraries
%bcond_with         syslib

# Bundled versions
%global bundled_libmongo  1.30.6
%global bundled_libcrypt  1.12.0
# Required versions (in config.m4)
%global minimal_libmongo  1.30.6
%global minimal_libcrypt  1.12.0

%if %{with syslib}
# Build dependencies (in repository)
%global system_libmongo   1.30
%global system_libcrypt   1.12
# Runtime dependencies
%global runtime_libmongo  %(pkg-config --silence-errors --modversion libmongoc-1.0 2>/dev/null || echo %{system_libmongo})
%global runtime_libcrypt  %(pkg-config --silence-errors --modversion libmongocrypt 2>/dev/null || echo %{system_libcrypt})
%endif

Summary:        MongoDB driver for PHP version 1
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
%global upstream_version 1.21.2
#global upstream_prever  beta1
#global upstream_lower   ~beta1
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure       ../%{sources}/configure
Version:        %{upstream_version}%{?upstream_lower}
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
%if %{with syslib}
License:        Apache-2.0
%else
License:        Apache-2.0 AND ISC AND MIT AND Zlib AND BSD-3-Clause
%endif
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?scl_prefix}php-devel >= 8.1
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-json
%if %{with syslib}
BuildRequires:  pkgconfig(libbson-1.0)      >= %{system_libmongo}
BuildRequires:  pkgconfig(libmongoc-1.0)    >= %{system_libmongo}
BuildRequires:  pkgconfig(libmongocrypt)    >= %{system_libcrypt}
Requires:       libbson%{?_isa}             >= %{runtime_libmongo}
Requires:       mongo-c-driver-libs%{?_isa} >= %{runtime_libmongo}
Requires:       libmongocrypt%{?_isa}       >= %{runtime_libcrypt}
%else
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(libsasl2)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(snappy)
%if 0%{?rhel} == 8
# EL-8 will use bundled as only in subversion module
Provides:       bundled(libutf8proc)= 2.8.0
%else
BuildRequires:  pkgconfig(libutf8proc)
%endif
Provides:       bundled(libbson)           = %{bundled_libmongo}
Provides:       bundled(mongo-c-driver)    = %{bundled_libmongo}
Provides:       bundled(libmongocrypt)     = %{bundled_libcrypt}
%endif
%if %{with tests}
BuildRequires:  mongodb-server
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-json%{?_isa}

# Don't provide php-mongodb which is the pure PHP library
# PECL
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})           = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa}   = %{version}
# PIE
Provides:       %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:       %{?scl_prefix}php-%{pie_vend}-%{pie_proj}      = %{version}

%description
The purpose of this driver is to provide exceptionally thin glue between
MongoDB and PHP, implementing only fundemental and performance-critical
components necessary to build a fully-functional MongoDB driver.

This package provides version 1 of the extension,
php-pecl-mongodb2 provides version 2.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c
# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

pushd %{sources}

# Check our macro values
cat src/*_VERSION_CURRENT
grep -q %{bundled_libmongo} src/LIBMONGOC_VERSION_CURRENT
grep -q %{bundled_libcrypt} src/LIBMONGOCRYPT_VERSION_CURRENT

grep CHECK_MODULES config.m4
grep -q %{minimal_libmongo} config.m4
grep -q %{minimal_libcrypt} config.m4

%if %{with syslib}
# temporary: lower minimal required versions
sed -e 's/%{minimal_libmongo}/%{system_libmongo}/;s/%{minimal_libcrypt}/%{system_libcrypt}/' -i config.m4
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_MONGODB_VERSION /{s/.* "//;s/".*$//;p}' phongo_version.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi

popd

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{summary} extension module
extension=%{pecl_name}.so

; Configuration
;mongodb.debug=''
EOF


%build
%{?dtsenable}

peclbuild() {
  %configure \
%if %{with syslib}
    --with-mongodb-system-libs \
%else
    --enable-mongodb-crypto-system-profile \
    --with-mongodb-snappy \
    --with-mongodb-zlib \
    --with-mongodb-zstd \
    --with-mongodb-sasl=cyrus \
    --with-mongodb-ssl=openssl \
%if 0%{?rhel} == 8
    --with-mongodb-utf8proc=bundled \
%else
    --with-mongodb-utf8proc=system \
%endif
%endif
    --with-php-config=${1} \
    --with-mongodb-client-side-encryption \
    --enable-mongodb

  %make_build
}

cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

%if %{with syslib}
  # Ensure we use system library
  # Need to be removed only after phpize because of m4_include
  rm -r src/libmongoc*
%endif

cd ../NTS
peclbuild %{__phpconfig}

%if %{with_zts}
cd ../ZTS
peclbuild %{__ztsphpconfig}
%endif


%install
%{?dtsenable}

%make_install -C NTS

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%make_install -C ZTS

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 %{sources}/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
OPT="-n"
[ -f %{php_extdir}/json.so ] && OPT="$OPT -d extension=json.so"

: Minimal load test for NTS extension
%{__php} $OPT \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%if %{with tests}
ret=0

%global mongo_version  %(mongod --version | sed -n '/db version/{s/.*v//;p}' 2>/dev/null)
#global mongo_version 4

: Run a mongodb server version %{mongo_version}
mkdir dbtest
mongod \
  --journal \
  --bind_ip     127.0.0.1 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork   || : skip test as server cant start

if [ -s server.pid ] ; then
  : Drop known to fail tests
%if "%{mongo_version}" < "3.4"
    ### With mongodb 3.2
%endif

  : Run the test suite
  echo '{"STANDALONE": "mongodb://127.0.0.1:27017"}' | tee /tmp/PHONGO-SERVERS.json

  pushd %{sources}
    TEST_PHP_ARGS="$OPT -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
    REPORT_EXIT_STATUS=1 \
    %{__php} -n run-tests.php -q -P --show-diff || ret=1
  popd

%if %{with_zts}
  pushd ZTS
    TEST_PHP_ARGS="$OPT -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
    REPORT_EXIT_STATUS=1 \
    %{__ztsphp} -n run-tests.php -q -P --show-diff || ret=1
  popd
%endif

  : Cleanup
  kill $(cat server.pid)
fi

exit $ret
%else
: check disabled, missing '--with tests' option
%endif


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Wed Oct  8 2025 Remi Collet <remi@remirepo.net> - 1.21.2-1
- update to 1.21.2
- use bundled libbson and libmongc 1.30.6

* Mon Jun 16 2025 Remi Collet <remi@remirepo.net> - 1.21.1-1
- update to 1.21.1 (no change)
- use bundled libbson and libmongc 1.30.5

* Thu Apr 10 2025 Remi Collet <remi@remirepo.net> - 1.21.0-2
- rebuild using bundled libraries
- add note in description about php-pecl-mongodb2

* Fri Feb 28 2025 Remi Collet <remi@remirepo.net> - 1.21.0-1
- update to 1.21.0
- raise dependency on PHP 8.1
- raise dependency on libbson and libmongc 1.30
- raise dependency on libmongocrypt 1.12

* Wed Nov 27 2024 Remi Collet <remi@remirepo.net> - 1.20.1-1
- update to 1.20.1

* Mon Sep 30 2024 Remi Collet <remi@remirepo.net> - 1.20.0-2
- EL: rebuild with system libraries

* Tue Sep 24 2024 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0

* Mon Sep  9 2024 Remi Collet <remi@remirepo.net> - 1.19.4-1
- update to 1.19.4

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 1.19.3-1
- update to 1.19.3

* Thu Jun  6 2024 Remi Collet <remi@remirepo.net> - 1.19.2-1
- update to 1.19.2 (no change)
- EL-7 use bundled libbson and libmongc 1.27.2

* Wed May 29 2024 Remi Collet <remi@remirepo.net> - 1.19.1-1
- update to 1.19.1

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0
- raise dependency on libbson and libmongc 1.27.0
- raise dependency on libmongocrypt 1.10.0

* Fri Apr 12 2024 Remi Collet <remi@remirepo.net> - 1.18.1-1
- update to 1.18.1 (no change)
- EL use bundled libbson and libmongc 1.26.2

* Thu Mar 28 2024 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0
- EL use bundled libbson and libmongc 1.26.1
- EL use bundled libmongocrypt 1.9.1

* Tue Mar 19 2024 Remi Collet <remi@remirepo.net> - 1.17.3-1
- update to 1.17.3 (no change)
- EL use bundled libbson and libmongc 1.25.4
- EL use bundled libmongocrypt 1.8.4

* Thu Dec 21 2023 Remi Collet <remi@remirepo.net> - 1.17.2-1
- update to 1.17.2

* Wed Dec  6 2023 Remi Collet <remi@remirepo.net> - 1.17.1-1
- update to 1.17.1
- EL use bundled libbson and libmongc 1.25.2

* Wed Nov 15 2023 Remi Collet <remi@remirepo.net> - 1.17.0-1
- update to 1.17.0
- raise dependency on PHP 7.4
- EL use bundled libbson and libmongc 1.25.1
- EL use bundled libmongocrypt 1.8.2
- open https://github.com/mongodb/mongo-php-driver/pull/1490 drop ICU information

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 1.16.2-2
- rebuild for PHP 8.3.0RC1

* Thu Aug 17 2023 Remi Collet <remi@remirepo.net> - 1.16.2-1
- update to 1.16.2

* Thu Jul 13 2023 Remi Collet <remi@remirepo.net> - 1.16.1-2
- EL-8/9 rebuild with libraries in EPEL stable

* Fri Jun 23 2023 Remi Collet <remi@remirepo.net> - 1.16.1-1
- update to 1.16.1 (no change)

* Thu Jun 22 2023 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0
- EL use bundled libbson and libmongc 1.24.1
- EL use bundled libmongocrypt 1.8.1

* Sat May 13 2023 Remi Collet <remi@remirepo.net> - 1.15.3-1
- update to 1.15.3
- EL-7 use bundled libbson and libmongc 1.23.4

* Tue Apr 25 2023 Remi Collet <remi@remirepo.net> - 1.15.2-2
- build out of sources tree

* Sat Apr 22 2023 Remi Collet <remi@remirepo.net> - 1.15.2-1
- update to 1.15.2 (no change)
- EL-7 use bundled libbson and libmongc 1.23.3

* Thu Feb  9 2023 Remi Collet <remi@remirepo.net> - 1.15.1-1
- update to 1.15.1
- EL-7 use bundled libbson and libmongc 1.23.2
- cleanup spec macros
- use SPDX license ID

* Wed Nov 23 2022 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0
- EL-7 use bundled libbson and libmongc 1.23.1

* Fri Oct 21 2022 Remi Collet <remi@remirepo.net> - 1.14.2-1
- update to 1.14.2
- EL-7 use bundled libmongocrypt 1.5.2

* Mon Sep 12 2022 Remi Collet <remi@remirepo.net> - 1.14.1-2
- EL-9 rebuild with libraries in EPEL stable

* Sat Sep 10 2022 Remi Collet <remi@remirepo.net> - 1.14.1-1
- update to 1.14.1

* Wed Jul 27 2022 Remi Collet <remi@remirepo.net> - 1.14.0-2
- build with system libraries

* Mon Jul 18 2022 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0
- use bundled libmongocrypt 1.5.0
- use bundled libbson and libmongc 1.22.0

* Wed Jun  8 2022 Remi Collet <remi@remirepo.net> - 1.14.0~beta1-1
- update to 1.14.0beta1
- use bundled libmongocrypt 1.5.0-rc1
- use bundled libbson and libmongc 1.22.0-beta0

* Thu Mar 24 2022 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0
- with libbson and libmongoc 1.21.1 and libmongocrypt 1.3.2

* Wed Feb 23 2022 Remi Collet <remi@remirepo.net> - 1.12.1-1
- update to 1.12.1 (no change)
- with libbson and libmongoc 1.20.1

* Wed Dec 15 2021 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0
- with libbson and libmongoc 1.20.0
- with libmongocrypt 1.3.0
- raise dependency on PHP 7.2

* Wed Nov  3 2021 Remi Collet <remi@remirepo.net> - 1.11.1-1
- update to 1.11.1 (no change)

* Sat Oct 30 2021 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0
- with libbson and libmongoc 1.19.1

* Wed Sep 29 2021 Remi Collet <remi@remirepo.net> - 1.11.0~alpha1-2
- rebuild using ICU 69

* Tue Sep 14 2021 Remi Collet <remi@remirepo.net> - 1.11.0~alpha1-1
- update to 1.11.0alpha1
- with libbson and libmongoc 1.19.0
- drop patch merged upstream

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 1.10.0-4
- rebuild for 8.1.0RC1

* Thu Aug  5 2021 Remi Collet <remi@remirepo.net> - 1.10.0-3
- rebuild with system library on EL-8

* Fri Jul 23 2021 Remi Collet <remi@remirepo.net> - 1.10.0-2
- add patch for PHP 8.1.0beta1 from
  https://github.com/mongodb/mongo-php-driver/pull/1240

* Wed Jul 14 2021 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0
- with libbson and libmongoc 1.18.0
- with libmongocrypt 1.2.1
- raise dependency on PHP 7.1

* Fri Apr  9 2021 Remi Collet <remi@remirepo.net> - 1.10.0~alpha1-1
- update to 1.10.0alpha1
- with libbson and libmongoc 1.18.0alpha
- with libmongocrypt 1.2.1dev

* Wed Apr  7 2021 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1
- with libbson and libmongoc 1.17.4

* Wed Nov 25 2020 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0 (stable)

* Wed Nov 11 2020 Remi Collet <remi@remirepo.net> - 1.9.0~RC1-1
- update to 1.9.0RC1 (beta)

* Thu Nov  5 2020 Remi Collet <remi@remirepo.net> - 1.8.2-1
- update to 1.8.2 (no change)
- with libbson and libmongoc 1.17.2
- with libmongocrypt 1.0.4

* Tue Oct  6 2020 Remi Collet <remi@remirepo.net> - 1.8.1-1
- update to 1.8.1

* Thu Aug 27 2020 Remi Collet <remi@remirepo.net> - 1.8.0-2
- rebuild with system library on EL-8

* Fri Jul 31 2020 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0
- with libbson and libmongoc 1.17.0

* Fri Jul 17 2020 Remi Collet <remi@remirepo.net> - 1.8.0~rc1-1
- update to 1.8.0RC1
- with libbson and libmongoc 1.17.0-rc0

* Thu Jun 11 2020 Remi Collet <remi@remirepo.net> - 1.8.0~beta2-1
- update to 1.8.0beta2
- with libbson and libmongoc 1.17.0-beta2

* Wed Apr 15 2020 Remi Collet <remi@remirepo.net> - 1.8.0~beta1-1
- update to 1.8.0beta1
- with libbson and libmongoc 1.17.0-beta

* Wed Mar 11 2020 Remi Collet <remi@remirepo.net> - 1.7.4-1
- update to 1.7.4 (no change)

* Tue Feb 25 2020 Remi Collet <remi@remirepo.net> - 1.7.3-1
- update to 1.7.3 (no change)
- with libbson and libmongoc 1.16.2

* Thu Feb 13 2020 Remi Collet <remi@remirepo.net> - 1.7.2-1
- update to 1.7.2 (no change)
- with libmongocrypt 1.0.3

* Wed Feb  5 2020 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1 (no change)
- drop patch merged upstream

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 1.7.0-1
- update to 1.7.0
- with libbson and libmongoc 1.16.1
- with libmongocrypt 1.0.1
- fix build with system libraries using patch from
  https://github.com/mongodb/mongo-php-driver/pull/1095

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 1.6.1-1
- update to 1.6.1

* Mon Sep  9 2019 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 1.6.0~rc1-2
- rebuild for 7.4.0RC1

* Mon Sep  2 2019 Remi Collet <remi@remirepo.net> - 1.6.0~rc1-1
- update to 1.6.0RC1

* Thu Aug 22 2019 Remi Collet <remi@remirepo.net> - 1.6.0~alpha3-1
- update to 1.6.0alpha3
- with libbson and libmongoc 1.15.0
- ensure proper library version is required
- raise minimal PHP version to 5.6

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 1.6.0~alpha2-2
- rebuild for 7.4.0beta1

* Tue Jun  4 2019 Remi Collet <remi@remirepo.net> - 1.6.0~alpha2-1
- update to 1.6.0alpha2
- with libbson and libmongoc 1.14.0

* Thu Mar  7 2019 Remi Collet <remi@remirepo.net> - 1.6.0~alpha1-2
- rebuild with libicu62

* Mon Dec  3 2018 Remi Collet <remi@remirepo.net> - 1.6.0~alpha1-1
- update to 1.6.0alpha1

* Sat Dec  1 2018 Remi Collet <remi@remirepo.net> - 1.5.3-2
- EL-8 build (using bundled libmongc for now)

* Fri Sep 21 2018 Remi Collet <remi@remirepo.net> - 1.5.3-1
- update to 1.5.3
- with libbson and libmongoc 1.13.0

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 1.5.2-2
- rebuild for 7.3.0beta2 new ABI

* Wed Aug  8 2018 Remi Collet <remi@remirepo.net> - 1.5.2-1
- update to 1.5.2

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 1.5.1-2
- rebuld for 7.3.0alpha4 new ABI

* Mon Jul  9 2018 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1

* Tue Jun 26 2018 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0
- with libbson and libmongoc 1.11.0
- add dependency on icu

* Thu Jun  7 2018 Remi Collet <remi@remirepo.net> - 1.4.4-1
- update to 1.4.4

* Thu Apr 19 2018 Remi Collet <remi@remirepo.net> - 1.4.3-1
- update to 1.4.3
- with libbson and libmongoc 1.9.4

* Wed Mar  7 2018 Remi Collet <remi@remirepo.net> - 1.4.2-1
- Update to 1.4.2 (no change)
- with libbson and libmongoc 1.9.3

* Wed Feb 21 2018 Remi Collet <remi@remirepo.net> - 1.4.1-1
- Update to 1.4.1 (stable)
- disable test suite because of #1547618

* Fri Feb  9 2018 Remi Collet <remi@remirepo.net> - 1.4.0-1
- Update to 1.4.0 (stable)

* Wed Feb  7 2018 Remi Collet <remi@remirepo.net> - 1.4.0~rc2-1
- Update to 1.4.0RC2

* Fri Dec 22 2017 Remi Collet <remi@remirepo.net> - 1.4.0~rc1-1
- Update to 1.4.0RC1
- with libbson and libmongoc 1.9.2

* Fri Dec 22 2017 Remi Collet <remi@remirepo.net> - 1.4.0~beta1-1
- Update to 1.4.0beta1
- with libbson and libmongoc 1.9.0

* Sun Dec  3 2017 Remi Collet <remi@remirepo.net> - 1.3.4-1
- Update to 1.3.4

* Wed Nov 22 2017 Remi Collet <remi@remirepo.net> - 1.3.3-1
- Update to 1.3.3 (stable)
- with libbson and libmongoc 1.8.2

* Tue Oct 31 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- Update to 1.3.2

* Tue Oct 17 2017 Remi Collet <remi@remirepo.net> - 1.3.1-1
- Update to 1.3.1 (stable)
- with libbson and libmongoc 1.8.1

* Wed Sep 20 2017 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0 (stable)
- with libbson and libmongoc 1.8.0

* Fri Sep 15 2017 Remi Collet <remi@remirepo.net> - 1.3.0~RC1-1
- update to 1.3.0RC1
- raise dependency on libbson and mongo-c-driver 1.8.0
- raise dependency on PHP 5.5

* Wed Aug 23 2017 Remi Collet <remi@remirepo.net> - 1.3.0~beta1-2
- add patch for upcoming PHP 7.2.0RC1 and new timelib from
  https://github.com/mongodb/mongo-php-driver/pull/633

* Fri Aug 11 2017 Remi Collet <remi@remirepo.net> - 1.3.0~beta1-1
- update to 1.3.0beta1
- raise dependency on libbson and mongo-c-driver 1.7.0

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 1.2.9-4
- rebuild for PHP 7.2.0beta1 new API

* Wed Jun 21 2017 Remi Collet <remi@remirepo.net> - 1.2.9-3
- rebuild for 7.2.0alpha2

* Tue May 30 2017 Remi Collet <remi@remirepo.net> - 1.2.9-2
- rebuild (for 7.2)

* Thu May  4 2017 Remi Collet <remi@remirepo.net> - 1.2.9-1
- Update to 1.2.9

* Mon Mar 20 2017 Remi Collet <remi@remirepo.net> - 1.2.8-1
- Update to 1.2.8

* Wed Mar 15 2017 Remi Collet <remi@remirepo.net> - 1.2.7-1
- Update to 1.2.7

* Wed Mar  8 2017 Remi Collet <remi@remirepo.net> - 1.2.6-1
- Update to 1.2.6

* Wed Feb 01 2017 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5

* Tue Jan 31 2017 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Wed Dec 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Thu Dec  8 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- rebuild with PHP 7.1.0 GA

* Tue Nov 29 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- internal dependency on date, json, spl and standard

* Wed Sep 28 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.alpha3
- update to 1.2.0alpha3
- use bundled libbson and libmongoc

* Mon Aug  8 2016 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.1.alpha1
- update to 1.2.0alpha1
- open https://jira.mongodb.org/browse/PHPC-762 missing symbols

* Tue Jul 19 2016 Remi Collet <remi@fedoraproject.org> - 1.1.8-4
- License is ASL 2.0, from review #1269056

* Wed Jul 06 2016 Remi Collet <remi@fedoraproject.org> - 1.1.8-2
- Update to 1.1.8

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-3
- run the test suite during the build (x86_64 only)
- ignore known to fail tests

* Thu Jun  2 2016 Remi Collet <remi@fedoraproject.org> - 1.1.7-2
- Update to 1.1.7

* Thu Apr  7 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-2
- Update to 1.1.6

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-4
- load after smbclient to workaround
  https://jira.mongodb.org/browse/PHPC-658

* Fri Mar 18 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-2
- Update to 1.1.5 (stable)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- Update to 1.1.4 (stable)

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-2
- Update to 1.1.3 (stable)

* Thu Jan 07 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-2
- Update to 1.1.2 (stable)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-4
- fix patch for 32bits build
  open https://github.com/mongodb/mongo-php-driver/pull/191

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.1.1-2
- Update to 1.1.1 (stable)
- add patch for 32bits build,
  open https://github.com/mongodb/mongo-php-driver/pull/185

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)
- raise dependency on libmongoc >= 1.3.0

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- update to 1.0.1 (stable)
- ensure libmongoc >= 1.2.0 and < 1.3 is used

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- update to 1.0.0 (stable)

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.RC0
- Update to 1.0.0RC0 (beta)

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3-beta2
- Update to 1.0.0beta2 (beta)

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2-beta1
- Update to 1.0.0beta1 (beta)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha2
- Update to 1.0.0alpha2 (alpha)
- buid with system libmongoc

* Thu May 07 2015 Remi Collet <remi@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 (alpha)

* Wed May 06 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0 (alpha)

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1 (alpha)

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-2
- build with system libbson
- open https://jira.mongodb.org/browse/PHPC-259

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- initial package, version 0.5.0 (alpha)

