# remirepo spec file for php-pecl-igbinary
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-igbinary
#
# SPDX-FileCopyrightText:  Copyright 2010-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
# Please, preserve the changelog entries
#

%{?scl:%scl_package      php-pecl-igbinary}

%bcond_without           tests

%global pecl_name        igbinary
%global with_zts         0%{!?_without_zts:%{?__ztsphp:1}}
%global gh_commit        6a2d5b7ea71489c4d7065dc7746d37cfa80d501c
%global gh_short         %(c=%{gh_commit}; echo ${c:0:7})
%global ini_name         40-%{pecl_name}.ini

%global upstream_version 3.2.16
#global upstream_prever  RC1
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure       ../%{sources}/configure

Summary:        Replacement for the standard PHP serializer
Name:           %{?scl_prefix}php-pecl-igbinary
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        8%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD-3-Clause
URL:            https://pecl.php.net/package/igbinary
Source0:        https://pecl.php.net/get/%{sources}.tgz

Patch0:         393.patch
Patch1:         398.patch
Patch2:         399.patch

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-devel >= 7.0
BuildRequires:  %{?scl_prefix}php-pecl-apcu-devel
BuildRequires:  %{?scl_prefix}php-json
# used by tests
BuildRequires:  tzdata

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

Obsoletes:      %{?scl_prefix}php-%{pecl_name}               <= 1.1.1
Provides:       %{?scl_prefix}php-%{pecl_name}                = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}        = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})          = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa}  = %{version}


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       Igbinary developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

Obsoletes:     %{?scl_prefix}php-%{pecl_name}-devel             <= 1.1.1
Provides:      %{?scl_prefix}php-%{pecl_name}-devel              = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{pecl_name}-devel%{?_isa}      = %{version}-%{release}

%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c

%if 0%{?gh_date}
%{__php} -r '
  $pkg = simplexml_load_file("NTS/package.xml");
  $pkg->date = substr("%{gh_date}",0,4)."-".substr("%{gh_date}",4,2)."-".substr("%{gh_date}",6,2);
  $pkg->version->release = "%{version}dev";
  $pkg->stability->release = "devel";
  $pkg->asXML("package.xml");
'
%endif

sed -e '/COPYING/s/role="doc"/role="src"/' -i package.xml

pushd %{sources}
%patch -P0 -p1 -b .pr393
%patch -P1 -p1 -b .pr398
%patch -P2 -p1 -b .pr399

# Check version
subdir=php7
extver=$(sed -n '/#define PHP_IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' src/$subdir/igbinary.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
popd

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

cat <<EOF | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary

; Use igbinary as APC serializer
;apc.serializer=igbinary
EOF


%build
%{?dtsenable}

cd %{sources}
%{__phpize}
[ -f Makefile.global ] && GLOBAL=Makefile.global || GLOBAL=build/Makefile.global
sed -e 's/INSTALL_ROOT/DESTDIR/' -i $GLOBAL

cd ../NTS
%configure --with-php-config=%{__phpconfig}
%make_build

%if %{with_zts}
cd ../ZTS
%configure --with-php-config=%{__ztsphpconfig}
%make_build
%endif


%install
%{?dtsenable}

%make_install -C NTS

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
%make_install -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd %{sources}
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f $i       ] && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
   [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd %{sources}
MOD=""
# drop extension load from phpt
sed -e '/^extension=/d' -i tests/*phpt

: simple NTS module load test, without APCu, as optional
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

# APC required for test 045*
if [ -f %{php_extdir}/apcu.so ]; then
  MOD="-d extension=apcu.so"
fi
# Json used in tests
if [ -f %{php_extdir}/json.so ]; then
  MOD="$MOD -d extension=json.so"
fi

%if %{with tests}
%if "%{php_version}" > "8.0"
OPTS="-q --show-diff %{?_smp_mflags}"
%else
OPTS="-q -P --show-diff"
%endif

: upstream NTS test suite
TEST_PHP_ARGS="-n $MOD -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php $OPTS
%endif

%if %{with_zts}
: simple ZTS module load test, without APCu, as optional
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif


%files
%license %{sources}/COPYING
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}

%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Tue Oct  7 2025 Remi Collet <remi@remirepo.net> - 3.2.16-8
- rebuild for PHP 8.5.0RC2
- re-enable full test suite

* Mon Sep 29 2025 Remi Collet <remi@remirepo.net> - 3.2.16-7
- only ignore tests using deprecated call in PHP 8.5

* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 3.2.16-6
- rebuild for PHP 8.5.0RC1
- disable test suite with PHP 8.5

* Mon Sep  1 2025 Remi Collet <remi@remirepo.net> - 3.2.16-5
- fix for PHP 8.5.0beta2 using patch from
  https://github.com/igbinary/igbinary/pull/399

* Wed Jul 30 2025 Remi Collet <remi@remirepo.net> - 3.2.16-4
- fix for PHP 8.5.0alpha3 using patch from
  https://github.com/igbinary/igbinary/pull/398
- re-license spec file to CECILL-2.1

* Mon Sep 30 2024 Remi Collet <remi@remirepo.net> - 3.2.16-3
- fix test suite with PHP 8.4 using patch from
  https://github.com/igbinary/igbinary/pull/393

* Tue Sep 24 2024 Remi Collet <remi@remirepo.net> - 3.2.16-2
- rebuild for 8.4.0RC1

* Mon Aug 12 2024 Remi Collet <remi@remirepo.net> - 3.2.16-1
- update to 3.2.16 (no change)
- drop patch merged upstream

* Fri Jul  5 2024 Remi Collet <remi@remirepo.net> - 3.2.15-2
- fix test suite with 8.4 using patch from
  https://github.com/igbinary/igbinary/pull/390

* Mon Dec  4 2023 Remi Collet <remi@remirepo.net> - 3.2.15-1
- update to 3.2.15
- build out of sources tree

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 3.2.14-2
- rebuild for PHP 8.3.0RC1

* Mon Feb 27 2023 Remi Collet <remi@remirepo.net> - 3.2.14-1
- update to 3.2.14

* Thu Feb  2 2023 Remi Collet <remi@remirepo.net> - 3.2.13-1
- update to 3.2.13

* Mon Nov  7 2022 Remi Collet <remi@remirepo.net> - 3.2.12-1
- update to 3.2.12

* Mon Nov  7 2022 Remi Collet <remi@remirepo.net> - 3.2.11-1
- update to 3.2.11

* Mon Oct 17 2022 Remi Collet <remi@remirepo.net> - 3.2.9-1
- update to 3.2.9

* Thu Sep  8 2022 Remi Collet <remi@remirepo.net> - 3.2.7-2
- ignore 2 failed tests with 8.2

* Wed Jan 12 2022 Remi Collet <remi@remirepo.net> - 3.2.7-1
- update to 3.2.7

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 3.2.6-2
- rebuild for 8.1.0RC1

* Wed Aug 11 2021 Remi Collet <remi@remirepo.net> - 3.2.6-1
- update to 3.2.6 (no change)

* Sun Aug  8 2021 Remi Collet <remi@remirepo.net> - 3.2.5-1
- update to 3.2.5

* Sun Jul 25 2021 Remi Collet <remi@remirepo.net> - 3.2.4-1
- update to 3.2.4

* Thu Jun 10 2021 Remi Collet <remi@remirepo.net> - 3.2.3-1
- update to 3.2.3

* Mon Apr 19 2021 Remi Collet <remi@remirepo.net> - 3.2.2-1
- update to 3.2.2

* Tue Jan 12 2021 Remi Collet <remi@remirepo.net> - 3.2.2~RC1-1
- update to 3.2.2RC1

* Mon Dec 28 2020 Remi Collet <remi@remirepo.net> - 3.2.1-1
- update to 3.2.1

* Sun Dec 27 2020 Remi Collet <remi@remirepo.net> - 3.2.0-1
- update to 3.2.0

* Fri Oct  9 2020 Remi Collet <remi@remirepo.net> - 3.1.6-1
- update to 3.1.6
- drop patch merged upstream

* Wed Oct  7 2020 Remi Collet <remi@remirepo.net> - 3.1.6~RC1-1
- update to 3.1.6RC1
- add patch for old gcc from
  https://github.com/igbinary/igbinary/pull/291

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 3.1.5-3
- rebuild for PHP 8.0.0RC1

* Wed Sep 23 2020 Remi Collet <remi@remirepo.net> - 3.1.5-2
- rebuild for PHP 8.0.0beta4

* Thu Sep  3 2020 Remi Collet <remi@remirepo.net> - 3.1.5-1
- update to 3.1.5
- drop patch merged upstream

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 3.1.4-2
- add upstream patch for test suite
- add patch for PHP 8.0.0beta3 from
  https://github.com/igbinary/igbinary/pull/284

* Thu Aug  6 2020 Remi Collet <remi@remirepo.net> - 3.1.4-1
- update to 3.1.4

* Wed Aug  5 2020 Remi Collet <remi@remirepo.net> - 3.1.3-1
- update to 3.1.3

* Wed Jul 22 2020 Remi Collet <remi@remirepo.net> - 3.1.2-4
- rebuild for PHP 8.0.0alpha3

* Thu May  7 2020 Remi Collet <remi@remirepo.net> - 3.1.2-3
- add upstream patch for test suite with PHP 7.4.6

* Wed Apr 15 2020 Remi Collet <remi@remirepo.net> - 3.1.2-2
- add upstream patch for test suite with PHP 8
  and ignore 3 other failing tests

* Wed Jan 22 2020 Remi Collet <remi@remirepo.net> - 3.1.2-1
- update to 3.1.2

* Thu Jan 16 2020 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1

* Sun Jan 12 2020 Remi Collet <remi@remirepo.net> - 3.1.1~a1-1
- update to 3.1.0a1 (alpha)

* Sat Dec 28 2019 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Sat Dec 21 2019 Remi Collet <remi@remirepo.net> - 3.1.0~b4-1
- update to 3.1.0b4 (beta)

* Tue Dec 10 2019 Remi Collet <remi@remirepo.net> - 3.1.0~b3-1
- update to 3.1.0b3 (beta)

* Mon Dec  9 2019 Remi Collet <remi@remirepo.net> - 3.1.0~b2-1
- update to 3.1.0b2 (beta)

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 3.0.1-5
- rebuild for 7.4.0RC1

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 3.0.1-4
- rebuild for 7.4.0beta1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 3.0.1-3
- rebuild

* Wed May 22 2019 Remi Collet <remi@remirepo.net> - 3.0.1-2
- cleanup

* Thu Mar 21 2019 Remi Collet <remi@remirepo.net> - 3.0.1-1
- update to 3.0.1 (no change)

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 3.0.0-1
- update to 3.0.0

* Thu Feb 14 2019 Remi Collet <remi@remirepo.net> - 3.0.0~a2-1
- update to 3.0.0a2 (alpha)
- raise dependency on PHP 7.0

* Sun Oct 21 2018 Remi Collet <remi@remirepo.net> - 2.0.8-1
- update to 2.0.8

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 2.0.7-3
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 2.0.7-2
- rebuld for 7.3.0alpha4 new ABI

* Wed Jun 27 2018 Remi Collet <remi@remirepo.net> - 2.0.7-1
- update to 2.0.7

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 2.0.6-1
- update to 2.0.6 (stable)

* Mon Apr  2 2018 Remi Collet <remi@remirepo.net> - 2.0.6~RC1-1
- update to 2.0.6RC1 (beta)

* Sun Nov  5 2017 Remi Collet <remi@remirepo.net> - 2.0.5-1
- update to 2.0.5 (stable)

* Mon Oct 16 2017 Remi Collet <remi@remirepo.net> - 2.0.5~RC1-1
- update to 2.0.5RC1 (beta)

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 2.0.4-3
- rebuild for PHP 7.2.0beta1 new API

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 2.0.4-2
- rebuild for 7.2.0alpha2

* Mon Apr 24 2017 Remi Collet <remi@remirepo.net> - 2.0.4-1
- Update to 2.0.4

* Thu Apr 13 2017 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3
- tarball generated from github (not yet available on pecl)
- add patch "Don't call __wakeup if Serializable::unserialize() was used
  to build object" from https://github.com/igbinary/igbinary/pull/130
- add patch "Fix test suite for PHP 7.2"
  from https://github.com/igbinary/igbinary/pull/131

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- rebuild with PHP 7.1.0 GA

* Mon Nov 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 (php 5 and 7, stable)

* Tue Oct 18 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.6.20161018git6a2d5b7
- refresh with sources from igbinary instead of old closed repo igbinary7

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.5.20160724git332a3d7
- rebuild for PHP 7.1 new API version

* Mon Jul 25 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.4.20160724git332a3d7
- refresh

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.3.20160715gita87a993
- ignore 1 test with 7.1

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.2.20160715gita87a993
- refresh, newer snapshot

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.1.20151217git2b7c703
- update to 1.2.2dev for PHP 7
- ignore test results, 4 failed tests: igbinary_009.phpt, igbinary_014.phpt
  igbinary_026.phpt and igbinary_unserialize_v1_compatible.phpt
- session support not yet available

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-2
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1.1
- Fedora 21 SCL mass rebuild

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- open https://github.com/igbinary/igbinary/pull/36

* Sun Aug 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.11.git3b8ab7e
- improve SCL stuff

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.10.git3b8ab7e
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.9.git3b8ab7e
- fix SCL dependencies

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.8.git3b8ab7e
- cleanups
- move doc in pecl_docdir
- move tests in pecl_testdir (devel)

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.6.git3b8ab7e
- latest snapshot
- fix build with APCu

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.3.git3b8ab7e
- cleanups

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.2.git3b8ab7e
- macro usage for latest PHP

* Mon Nov 14 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.1.git3b8ab7e
- latest git against php 5.4
- partial patch for https://bugs.php.net/60298
- ignore test result because of above bug

* Sat Sep 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- use latest macro
- build zts extension

* Mon Mar 14 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- version 1.1.1 published on pecl.php.net
- rename to php-pecl-igbinary

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- allow relocation using phpname macro

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- update to 1.1.1

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM

