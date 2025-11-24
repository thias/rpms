# remirepo spec file for php-pecl-zip
# with SCL compatibility, from:
#
# fedora spec file for php-pecl-zip
#
# SPDX-FileCopyrightText:  Copyright 2013-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%{?scl:%scl_package    php-pecl-zip}

%if ( 0%{?scl:1} && 0%{?rhel} == 8 ) || 0%{?rhel} >= 9
%bcond_without         move_to_opt
%else
%bcond_with            move_to_opt
%endif

%bcond_without         tests

%global with_zts         0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name        zip
%global pie_vend         pecl
%global pie_proj         zip

%global upstream_version 1.22.7
#global upstream_prever  dev
#global upstream_lower   DEV
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure       ../%{sources}/configure

%global libzip_version   1.11.1

%if "%{php_version}" < "5.6"
%global ini_name  %{pecl_name}.ini
%else
# ensure we are loaded before 40-imagick (for libzip)
%global ini_name  30-%{pecl_name}.ini
%endif

Summary:      A ZIP archive management extension
Name:         %{?scl_prefix}php-pecl-zip
Version:      %{upstream_version}%{?upstream_prever:~%{upstream_lower}}
Release:      1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:      PHP-3.01
Group:        Development/Languages
URL:          https://pecl.php.net/package/zip

Source0:      https://pecl.php.net/get/%{sources}.tgz

BuildRequires: make
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: zlib-devel
BuildRequires: %{?scl_prefix}php-pear

%if %{with move_to_opt}
BuildRequires: %{?vendeur:%{vendeur}-}libzip-devel   >= %{libzip_version}
Requires:      %{?vendeur:%{vendeur}-}libzip%{?_isa} >= %{libzip_version}
%global __brp_check_rpaths  /bin/true
%global __requires_exclude ^libzip\\.so.*$
%else
# Ensure latest version is used
BuildRequires: libzip-devel    >= %{libzip_version}
Requires:      libzip%{?_isa}  >= %{libzip_version}
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}

# Extension
Provides:     %{?scl_prefix}php-%{pecl_name} = 1:%{version}-%{release}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa} = 1:%{version}-%{release}
# PECL
Provides:     %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
# PIE
Provides:     %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}

%if "%{php_version}" > "7.0"
Obsoletes:     %{?scl_prefix}php-zip <= 7.0.0
%endif

%if 0%{?rhel} >= 10 && "%{?vendeur}" == "remi" && 0%{!?scl:1}
%if "%{php_version}" >= "8.5"
Obsoletes: php8.4-pecl-zip         < %{version}-%{release}
Obsoletes: php8.5-pecl-zip         < %{version}-%{release}
Provides:  php8.5-pecl-zip         = %{version}-%{release}
Provides:  php8.5-pecl-zip%{?_isa} = %{version}-%{release}
%elif "%{php_version}" >= "8.4"
Obsoletes: php8.4-pecl-zip         < %{version}-%{release}
Provides:  php8.4-pecl-zip         = %{version}-%{release}
Provides:  php8.4-pecl-zip%{?_isa} = %{version}-%{release}
%endif
%endif


%description
Zip is an extension to create and read zip files.

Package built with libzip %{libzip_version}.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{scl_vendor})}.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

cd %{sources}
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_ZIP_VERSION/{s/.* "//;s/".*$//;p}' php74/php_zip.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}" -a "x${extver}" != "x%{upstream_version}-%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
cd ..

: Create the configuration file
cat >%{ini_name} << 'EOF'
; Enable ZIP extension module
extension=%{pecl_name}.so
EOF

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif


%build
%{?dtsenable}

%if %{with move_to_opt}
export PKG_CONFIG_PATH=/opt/%{?vendeur:%{vendeur}/}libzip/%{_lib}/pkgconfig
%endif

cd %{sources}
%{__phpize}
[ -f Makefile.global ] && GLOBAL=Makefile.global || GLOBAL=build/Makefile.global
sed -e 's/INSTALL_ROOT/DESTDIR/' -i $GLOBAL

cd ../NTS
%configure \
  --with-libzip \
  --with-libdir=%{_lib} \
  --with-php-config=%{__phpconfig}

%make_build

%if %{with_zts}
cd ../ZTS
%configure \
  --with-libzip \
  --with-libdir=%{_lib} \
  --with-php-config=%{__ztsphpconfig}

%make_build
%endif


%install
%{?dtsenable}

%make_install -C NTS
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%make_install -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
cd %{sources}
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}
OPT="-q --show-diff"
%if "%{php_version}" > "8.0"
OPT="$OPT %{?_smp_mflags}"
%endif

: minimal load test of NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with tests}
: upstream test suite for NTS extension
TEST_PHP_ARGS="-n -d extension_dir=$PWD/../NTS/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
TEST_PHP_EXECUTABLE=%{__php} \
%{__php} -n run-tests.php $OPT
%endif

%if %{with_zts}
: minimal load test of ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with tests}
: upstream test suite for ZTS extension
TEST_PHP_ARGS="-n -d extension_dir=$PWD/../ZTS/modules -d extension=%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
TEST_PHP_EXECUTABLE=%{__ztsphp} \
%{__ztsphp} -n run-tests.php $OPT
%endif
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
* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 1.22.7-1
- update to 1.22.7

* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 1.22.6-6
- rebuild for PHP 8.5.0RC1

* Thu Sep 18 2025 Remi Collet <remi@remirepo.net> - 1.22.6-4
- more upstream patches for PHP 8.5

* Wed Jul 30 2025 Remi Collet <remi@remirepo.net> - 1.22.6-3
- rebuild for 8.5.0alpha3

* Tue Jul  1 2025 Remi Collet <remi@remirepo.net> - 1.22.6-2
- add upstream patch for 8.5

* Wed May  7 2025 Remi Collet <remi@remirepo.net> - 1.22.6-1
- update to 1.22.6

* Thu Feb 20 2025 Remi Collet <remi@remirepo.net> - 1.22.5-1.1
- fix reported version with PHP 7.4

* Thu Feb 20 2025 Remi Collet <remi@remirepo.net> - 1.22.5-1
- update to 1.22.5
- re-license spec file to CECILL-2.1

* Fri Nov 15 2024 Remi Collet <remi@remirepo.net> - 1.22.4-2
- don't check rpath

* Thu Sep 26 2024 Remi Collet <remi@remirepo.net> - 1.22.4-1
- update to 1.22.4

* Tue Sep 24 2024 Remi Collet <remi@remirepo.net> - 1.22.3-5
- rebuild for 8.4.0RC1

* Wed Aug 21 2024 Remi Collet <remi@remirepo.net> - 1.22.3-4
- fix previous patch (for 8.0)

* Wed Jul 17 2024 Remi Collet <remi@remirepo.net> - 1.22.3-3
- rebuild for 8.4.0alpha2

* Thu Jul  4 2024 Remi Collet <remi@remirepo.net> - 1.22.3-2
- add upstream patches for PHP 8.4

* Tue Nov 14 2023 Remi Collet <remi@remirepo.net> - 1.22.3-1
- update to 1.22.3
- build out of sources tree

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 1.22.2-2
- rebuild for PHP 8.3.0RC1

* Wed Aug 23 2023 Remi Collet <remi@remirepo.net> - 1.22.2-1
- update to 1.22.2

* Thu Jun 29 2023 Remi Collet <remi@remirepo.net> - 1.22.1-1
- update to 1.22.1

* Mon Jun 26 2023 Remi Collet <remi@remirepo.net> - 1.22.0-1
- update to 1.22.0

* Mon Jun  5 2023 Remi Collet <remi@remirepo.net> - 1.21.1-2
- add upstream patches for 8.3

* Fri Sep 16 2022 Remi Collet <remi@remirepo.net> - 1.21.1-1
- update to 1.21.1

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 1.21.0-5
- rebuild for PHP 8.2.0RC1

* Wed Jul 20 2022 Remi Collet <remi@remirepo.net> - 1.21.0-4
- add upstream patch for 8.2.0beta1

* Wed Jun 29 2022 Remi Collet <remi@remirepo.net> - 1.21.0-3
- require minimal libzip version
- rebuild using libzip5 on EL-7

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.21.0-2
- rebuild using libzip 1.9.2 (remi-libzip on EL)

* Tue Jun 28 2022 Remi Collet <remi@remirepo.net> - 1.21.0-1
- update to 1.21.0

* Mon Jun 13 2022 Remi Collet <remi@remirepo.net> - 1.20.1-3
- more upstream patch for PHP 8.2

* Wed May 11 2022 Remi Collet <remi@remirepo.net> - 1.20.1-2
- add upstream patch for PHP 8.2

* Mon May  2 2022 Remi Collet <remi@remirepo.net> - 1.20.1-1
- update to 1.20.1

* Mon Nov  8 2021 Remi Collet <remi@remirepo.net> - 1.20.0-2
- use remi-libzip on EL-9

* Tue Oct 12 2021 Remi Collet <remi@remirepo.net> - 1.20.0-1
- update to 1.20.0

* Tue Oct 12 2021 Remi Collet <remi@remirepo.net> - 1.20.0~DEV-2
- test build for 1.20.0-dev

* Wed Oct  6 2021 Remi Collet <remi@remirepo.net> - 1.20.0~DEV-1
- test build for 1.20.0-dev

* Mon Sep 27 2021 Remi Collet <remi@remirepo.net> - 1.19.5-1
- update to 1.19.5

* Wed Sep  1 2021 Remi Collet <remi@remirepo.net> - 1.19.4-1
- update to 1.19.4

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 1.19.3-4
- rebuild for 8.1.0RC1

* Fri Jul  2 2021 Remi Collet <remi@remirepo.net> - 1.19.3-3
- rename configuration file to 30-zip.ini to ensure zip extension
  will be loaded before imagick to find proper libzip
  reported as https://github.com/remicollet/remirepo/issues/182

* Sat Jun 19 2021 Remi Collet <remi@remirepo.net> - 1.19.3-2
- rebuild with libzip 1.8.0 and zstd support

* Mon Jun  7 2021 Remi Collet <remi@remirepo.net> - 1.19.3-1
- update to 1.19.3

* Wed Apr 28 2021 Remi Collet <remi@remirepo.net> - 1.19.2-2
- F34 rebuild for https://github.com/remicollet/remirepo/issues/174

* Mon Nov 23 2020 Remi Collet <remi@remirepo.net> - 1.19.2-1
- update to 1.19.2

* Thu Nov  5 2020 Remi Collet <remi@remirepo.net> - 1.19.1-2
- rebuild against latest libzip SCL packages (EL-8)

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 1.19.1-1
- update to 1.19.1

* Wed Sep 16 2020 Remi Collet <remi@remirepo.net> - 1.19.0-7
- rebuild for 8.0.0beta4

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 1.19.0-6
- rebuild for 8.0.0beta3

* Mon Aug 17 2020 Remi Collet <remi@remirepo.net> - 1.19.0-5
- rebuild for 8.0.0beta2

* Wed Aug  5 2020 Remi Collet <remi@remirepo.net> - 1.19.0-4
- rebuild for 8.0.0beta1

* Wed Jul 22 2020 Remi Collet <remi@remirepo.net> - 1.19.0-3
- more change for PHP 8.0
- procedural API is deprecated

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 1.19.0-2
- fix encode parameter is option

* Fri Jun  5 2020 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0

* Fri Apr 10 2020 Remi Collet <remi@remirepo.net> - 1.19.0~DEV-2
- refresh for test suite

* Thu Apr  9 2020 Remi Collet <remi@remirepo.net> - 1.19.0~DEV-1
- update to 1.19.0-dev

* Fri Mar 20 2020 Remi Collet <remi@remirepo.net> - 1.18.2-1
- update to 1.18.2

* Thu Mar 19 2020 Remi Collet <remi@remirepo.net> - 1.18.1-1
- update to 1.18.1

* Mon Mar 16 2020 Remi Collet <remi@remirepo.net> - 1.18.0-1
- update to 1.18.0

* Mon Mar  9 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC6-1
- update to 1.18.0RC6

* Mon Mar  9 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC5-1
- update to 1.18.0RC5

* Thu Mar  5 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC4-1
- update to 1.18.0RC4

* Thu Mar  5 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC3-1
- update to 1.18.0RC3

* Wed Mar  4 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC2-1
- update to 1.18.0RC2

* Mon Mar  2 2020 Remi Collet <remi@remirepo.net> - 1.18.0RC1-1
- update to 1.18.0RC1

* Fri Feb 28 2020 Remi Collet <remi@remirepo.net> - 1.17.2-1
- update to 1.17.2

* Mon Feb  3 2020 Remi Collet <remi@remirepo.net> - 1.17.1-1
- update to 1.17.1

* Fri Jan 31 2020 Remi Collet <remi@remirepo.net> - 1.17.0-1
- update to 1.17.0

* Wed Jan 29 2020 Remi Collet <remi@remirepo.net> - 1.16.1-1
- update to 1.16.1

* Mon Jan 27 2020 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0

* Mon Sep  9 2019 Remi Collet <remi@remirepo.net> - 1.15.5-1
- update to 1.15.5

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 1.15.4-7
- rebuild for 7.4.0RC1

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 1.15.4-6
- rebuild for 7.4.0beta1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 1.15.4-4
- rebuild

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 1.15.4-3
- add upstream patch for 7.4

* Fri Nov 30 2018 Remi Collet <remi@remirepo.net> - 1.15.4-2
- EL-8 build

* Wed Oct  3 2018 Remi Collet <remi@remirepo.net> - 1.15.4-1
- update to 1.15.4 (stable)

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 1.15.3-4
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 1.15.3-3
- rebuld for 7.3.0alpha4 new ABI

* Tue Jun 19 2018 Remi Collet <remi@remirepo.net> - 1.15.3-2
- rebuild for PHP 7.3.0alpha2 new API

* Tue Jun 12 2018 Remi Collet <remi@remirepo.net> - 1.15.3-1
- update to 1.15.3 (stable)

* Tue Dec 19 2017 Remi Collet <remi@remirepo.net> - 1.15.2-1
- update to 1.15.2 (stable)

* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.15.1-4
- add upstream patch for libzip 1.3.1

* Tue Oct  3 2017 Remi Collet <remi@remirepo.net> - 1.15.1-3
- F27: release bump

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 1.15.1-2
- rebuild for PHP 7.2.0beta1 new API

* Tue Jul 11 2017 Remi Collet <remi@remirepo.net> - 1.15.1-1
- update to 1.15.1 (stable)

* Mon Jul 10 2017 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0 (stable)

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 1.14.0-2
- rebuild for 7.2.0alpha2

* Wed Apr  5 2017 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0 (stable)
- always buid with system libzip (bundled lib dropped upstream)

* Wed Mar  1 2017 Remi Collet <remi@fedoraproject.org> - 1.14.0-0.2.20170301dev
- refresh with pasword support in stream wrapper

* Sun Feb 19 2017 Remi Collet <remi@fedoraproject.org> - 1.14.0-0.1.20170219dev
- update to 1.4.0-dev with encryption support
- raise dependency on libzip 1.2.0

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-2
- rebuild with PHP 7.1.0 GA

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.5-1
- Update to 1.13.5

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.13.4-2
- rebuild for PHP 7.1 new API version

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.13.4-1
- Update to 1.13.4

* Thu Jun 23 2016 Remi Collet <remi@fedoraproject.org> - 1.13.3-1
- Update to 1.13.3

* Tue Mar  1 2016 Remi Collet <remi@fedoraproject.org> - 1.13.2-1
- Update to 1.13.2
- fix license management

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-3
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-2
- F23 rebuild with rh_layout

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 1.13.1-1
- Update to 1.13.1

* Mon Sep  7 2015 Remi Collet <remi@fedoraproject.org> - 1.13.0-1
- Update to 1.13.0
- raise dependency on libzip 1.0.0

* Wed Apr 15 2015 Remi Collet <remi@fedoraproject.org> - 1.12.5-1
- Update to 1.12.5
- Don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.12.1-3
- new scriptlets

* Sun Aug 24 2014 Remi Collet <rcollet@redhat.com> 1.12.1-2
- allow SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.12.4-2
- add numerical prefix to extension configuration file

* Wed Jan 29 2014 Remi Collet <remi@fedoraproject.org> - 1.12.4-1
- Update to 1.12.4 (stable) for libzip 0.11.2

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> - 1.12.3-1
- Update to 1.12.3 (stable)
- drop merged patch

* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-2
- upstream patch, don't use any libzip private struct
- drop LICENSE_libzip when system version is used
- always build ZTS extension

* Wed Oct 23 2013 Remi Collet <remi@fedoraproject.org> 1.12.2-1
- update to 1.12.2 (beta)
- drop merged patches
- install doc in pecl doc_dir
- install tests in pecl test_dir

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> 1.12.1-2.1
- backport stuff

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> 1.12.1-2
- refresh our merged patches from upstream git

* Thu Aug 08 2013 Remi Collet <rcollet@redhat.com> 1.12.1-1
- New spec for version 1.12.1
