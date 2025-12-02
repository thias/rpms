# remirepo spec file for php-pecl-ds
#
# SPDX-FileCopyrightText:  Copyright 2016-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%scl_package         php-pecl-ds
# No phpunit in SCL
%bcond_with          tests
%else
%bcond_without       tests
%endif

%global with_zts     0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name    ds
%global pie_vend     php-ds
%global pie_proj     ext-ds
# After json
%global ini_name     40-%{pecl_name}.ini
%global sources      %{pecl_name}-%{version}
%global _configure   ../%{sources}/configure

# For test suite, see https://github.com/php-ds/tests/commits/master
# version 1.5.1  (version 1.6.0 exist but requires phpunit12, so PHP 8.3)
%global gh_commit    3d14aa6f8c25d38d79c90924150c51636544e4a8
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     php-ds
%global gh_project   tests


Summary:        Data Structures for PHP
Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Version:        1.6.0
Release:        3%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        MIT
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{version}.tgz
# Only use for tests during the build, no value to be packaged separately
# in composer.json:  "require-dev": {  "php-ds/tests": "^1.5.0" }
Source1:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{gh_short}.tar.gz

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?scl_prefix}php-devel >= 7.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-gmp
BuildRequires:  %{?scl_prefix}php-json
%if %{with tests}
BuildRequires:  %{_bindir}/phpunit9
BuildRequires:  %{_bindir}/phpab
%endif
#BuildRequires:  php-debuginfo
#BuildRequires:  gdb

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-json%{?_isa}

# Extension
Provides:       %{?scl_prefix}php-%{pecl_name}                 = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}         = %{version}
# PECL
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})           = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa}   = %{version}
# PIE
Provides:       %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:       %{?scl_prefix}php-%{pie_vend}-%{pie_proj}      = %{version}


%description
An extension providing specialized data structures as efficient alternatives
to the PHP array.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -c -a 1
mv %{gh_project}-%{gh_commit} tests

# Don't install/register tests, install examples as doc
sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

cd %{sources}
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_DS_VERSION/{s/.* "//;s/".*$//;p}' php_ds.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension=%{pecl_name}.so
EOF


%build
%{?dtsenable}

peclbuild() {
%configure \
    --enable-ds \
    --with-php-config=$1

%make_build
}

cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

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
[ -f %{php_extdir}/json.so ] && modules="-d extension=json.so"

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif

%if %{with tests}
: Generate autoloader for tests
%{_bindir}/phpab \
   --output tests/autoload.php \
   tests

: Run upstream test suite
%{_bindir}/php \
   -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
   %{_bindir}/phpunit9 \
      --do-not-cache-result \
      --bootstrap tests/autoload.php \
      --verbose tests
%endif


%files
%license %{sources}/LICENSE
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 1.6.0-3
- rebuild for PHP 8.5.0RC1

* Wed Jul 30 2025 Remi Collet <remi@remirepo.net> - 1.6.0-2
- rebuild for 8.5.0alpha3

* Sat May  3 2025 Remi Collet <remi@remirepo.net> - 1.6.0-1
- update to 1.6.0
- re-license spec file to CECILL-2.1

* Wed Dec 20 2023 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 1.4.0-3
- rebuild for PHP 8.3.0RC1

* Wed Jul 12 2023 Remi Collet <remi@remirepo.net> - 1.4.0-2
- build out of sources tree
- add upstream patch for PHP 8.3

* Tue Dec 14 2021 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0
- raise dependency on PHP 7.3
- drop all patches merged upstream
- switch to phpunit8

* Wed Nov  3 2021 Remi Collet <remi@remirepo.net> - 1.3.0-6
- add patches for PHP 8.1 from upstream and from
  https://github.com/php-ds/ext-ds/pull/187

* Fri Mar 26 2021 Remi Collet <remi@remirepo.net> - 1.3.0-4
- switch to phpunit7

* Tue Nov  3 2020 Remi Collet <remi@remirepo.net> - 1.3.0-2
- fix segfault using patch from
  https://github.com/php-ds/ext-ds/pull/165

* Wed Oct 14 2020 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 1.2.9-2
- rebuild for 7.4.0RC1

* Mon May 13 2019 Remi Collet <remi@remirepo.net> - 1.2.9-1
- update to 1.2.9

* Tue Jan 29 2019 Remi Collet <remi@remirepo.net> - 1.2.8-1
- update to 1.2.8

* Mon Nov 19 2018 Remi Collet <remi@remirepo.net> - 1.2.7-1
- update to 1.2.7

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 1.2.6-3
- rebuild for 7.3.0beta2 new ABI

* Wed Jul 18 2018 Remi Collet <remi@remirepo.net> - 1.2.6-2
- rebuld for 7.3.0alpha4 new ABI

* Fri May 25 2018 Remi Collet <remi@remirepo.net> - 1.2.6-1
- update to 1.2.6

* Mon Mar 12 2018 Remi Collet <remi@remirepo.net> - 1.2.5-1
- update to 1.2.5

* Wed Nov 29 2017 Remi Collet <remi@remirepo.net> - 1.2.4-1
- Update to 1.2.4
- switch to phpunit 6

* Wed Aug 16 2017 Remi Collet <remi@remirepo.net> - 1.2.3-2
- Update to 1.2.3
- drop patch merged upstream

* Wed Aug  9 2017 Remi Collet <remi@remirepo.net> - 1.2.2-2
- add patch for bigendian

* Mon Aug  7 2017 Remi Collet <remi@remirepo.net> - 1.2.2-1
- Update to 1.2.2

* Thu Aug  3 2017 Remi Collet <remi@remirepo.net> - 1.2.1-1
- Update to 1.2.1

* Tue Aug  1 2017 Remi Collet <remi@remirepo.net> - 1.2.0-1
- Update to 1.2.0

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 1.1.10-2
- rebuild for PHP 7.2.0beta1 new API

* Thu Jun 22 2017 Remi Collet <remi@remirepo.net> - 1.1.10-1
- Update to 1.1.10

* Fri Mar 24 2017 Remi Collet <remi@remirepo.net> - 1.1.8-1
- Update to 1.1.8

* Mon Feb 13 2017 Remi Collet <remi@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-3
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-2
- rebuild for PHP 7.1 new API version

* Sun Sep 04 2016 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Mon Aug 08 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Mon Aug 08 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3
- Fix License tag

* Fri Aug 05 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2 (stable)

* Wed Aug 03 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)

* Wed Aug 03 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)

* Mon Aug 01 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4 (stable)

* Mon Aug 01 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (stable)

* Sat Jul 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (stable)

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package, version 1.0.0 (devel)
  open tests/tests/Map/sort.php
  open https://github.com/php-ds/extension/pull/26

