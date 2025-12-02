# remirepo spec file for php-pecl-memcached
# With SCL compatibility, from:
#
# Fedora spec file for php-pecl-memcached
#
# SPDX-FileCopyrightText:  Copyright 2009-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package         php-pecl-memcached
%else
%global _root_prefix %{_prefix}
%endif

%bcond_without fastlz
%bcond_without zstd
%bcond_without igbinary
%bcond_without msgpack
%bcond_without tests

%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global pie_vend    php-memcached
%global pie_proj    php-memcached
%global pecl_name   memcached
# After 40-igbinary, 40-json, 40-msgpack
%global ini_name    50-%{pecl_name}.ini

%global upstream_version 3.4.0
#global upstream_prever  RC1
# upstream use    dev => alpha => beta => RC
# make RPM happy  DEV => alpha => beta => rc
%global upstream_lower   %(echo %{upstream_prever} | tr '[:upper:]' '[:lower:]')
%global sources    %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure ../%{sources}/configure


Summary:      Extension to work with the Memcached caching daemon
Name:         %{?scl_prefix}php-pecl-memcached
Version:      %{upstream_version}%{?upstream_prever:~%{upstream_lower}}
Release:      1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:      PHP-3.01
URL:          https://pecl.php.net/package/%{pecl_name}

Source0:      https://pecl.php.net/get/%{sources}.tgz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel >= 7.0
BuildRequires: %{?scl_prefix}php-pear
BuildRequires: %{?scl_prefix}php-json
%if %{with igbinary}
BuildRequires: %{?scl_prefix}php-pecl-igbinary-devel
%endif
%if %{with msgpack}
BuildRequires: %{?scl_prefix}php-pecl-msgpack-devel
%endif
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel
%if %{with fastlz}
BuildRequires: fastlz-devel
%endif
%if %{with zstd}
BuildRequires: libzstd-devel
%endif
%if %{with tests}
BuildRequires: memcached
%endif

BuildRequires: pkgconfig(libevent) >= 2.0.2
%if 0%{?rhel} && 0%{?rhel} < 10
%global move_to_opt 1
BuildRequires: %{?vendeur:%{vendeur}-}libmemcached-awesome-devel >= 1.1
Requires:      libevent%{?_isa}
Requires:      fastlz%{?_isa}
Requires:      zlib%{?_isa}
Requires:      libzstd%{?_isa}
Requires:      cyrus-sasl-lib%{?_isa}
Requires:      %{?vendeur:%{vendeur}-}libmemcached-awesome%{?_isa}
%else
%global move_to_opt 0
BuildRequires: pkgconfig(libmemcached) >= 1.1
%endif

Requires:     %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:     %{?scl_prefix}php(api) = %{php_core_api}
Requires:     %{?scl_prefix}php-json%{?_isa}
%if %{with igbinary}
Requires:     %{?scl_prefix}php-igbinary%{?_isa}
%endif
%if %{with msgpack}
Requires:     %{?scl_prefix}php-msgpack%{?_isa}
%endif

# Extension
Provides:     %{?scl_prefix}php-%{pecl_name}                 = %{version}
Provides:     %{?scl_prefix}php-%{pecl_name}%{?_isa}         = %{version}
# PECL
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})           = %{version}
Provides:     %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa}   = %{version}
# PIE
Provides:     %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}
Provides:     %{?scl_prefix}php-%{pie_vend}-%{pie_proj}      = %{version}

%if %{move_to_opt}
%global __requires_exclude_from ^%{_libdir}/.*$
%endif


%description
This extension uses libmemcached-awesome library to provide API for
communicating with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep 
%setup -c -q

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

cd %{sources}
%if %{with fastlz}
rm -r fastlz
sed -e '/name=.fastlz/d' -i ../package.xml
%endif

# Check version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MEMCACHED_VERSION/{s/.* "//;s/".*$//;p}' php_memcached.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever:%{upstream_prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever:%{upstream_prever}}.
   : Update the macro and rebuild.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

; RPM note : save_handler and save_path are defined
; for mod_php, in /etc/httpd/conf.d/php.conf
; for php-fpm, in %{_sysconfdir}/php-fpm.d/*conf

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"

; ----- Configuration options
; https://php.net/manual/en/memcached.configuration.php

EOF

# default options with description from upstream
cat %{sources}/memcached.ini >>%{ini_name}

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif


%build
%{?dtsenable}

%if %{move_to_opt}
export PKG_CONFIG_PATH=/opt/%{?vendeur:%{vendeur}/}libmemcached-awesome/%{_lib}/pkgconfig
%endif

peclconf() {
%configure \
%if %{with igbinary}
           --enable-memcached-igbinary \
%endif
           --enable-memcached-json \
           --enable-memcached-sasl \
%if %{with msgpack}
           --enable-memcached-msgpack \
%endif
%if 0
           --disable-memcached-protocol \
%else
           --enable-memcached-protocol \
%endif
%if %{with fastlz}
           --with-system-fastlz \
%endif
%if %{with zstd}
           --with-zstd \
%endif
           --with-php-config=$1
}
cd %{sources}
%{__phpize}
[ -f Makefile.global ] && GLOBAL=Makefile.global || GLOBAL=build/Makefile.global
sed -e 's/INSTALL_ROOT/DESTDIR/' -i $GLOBAL

cd ../NTS
peclconf %{__phpconfig}
%make_build

%if %{with_zts}
cd ../ZTS
peclconf %{__ztsphpconfig}
%make_build
%endif


%install
%{?dtsenable}

# Install the NTS extension
%make_install -C NTS

# Drop in the bit of configuration
# rename to z-memcached to be load after msgpack
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the ZTS extension
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
OPT="-n"
[ -f %{php_extdir}/igbinary.so ] && OPT="$OPT -d extension=igbinary.so"
[ -f %{php_extdir}/json.so ]     && OPT="$OPT -d extension=json.so"
[ -f %{php_extdir}/msgpack.so ]  && OPT="$OPT -d extension=msgpack.so"

: Minimal load test for NTS extension
%{__php} $OPT \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif

%if %{with tests}
cd %{sources}
ret=0

%if "%{php_version}" < "7.3"
# ::1:50770 vs [::1]:%s
rm tests/memcachedserver6.phpt
%endif

: Launch the Memcached service
port=$(%{__php} -r 'echo 10000 + PHP_MAJOR_VERSION*1000 + PHP_MINOR_VERSION*100 + PHP_INT_SIZE + 0%{?scl:10} + %{?fedora}%{?rhel};')
memcached -p $port -U $port      -d -P $PWD/memcached.pid
sed -e "s/11211/$port/" -i tests/*

: Port for MemcachedServer
port=$(%{__php} -r 'echo 12000 + PHP_MAJOR_VERSION*1000 + PHP_MINOR_VERSION*100 + PHP_INT_SIZE + 0%{?scl:10} + %{?fedora}%{?rhel};')
sed -e "s/3434/$port/" -i tests/*

: Run the upstream test Suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="$OPT -d extension=$PWD/../NTS/modules/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q -x --show-diff || ret=1

# Cleanup
if [ -f memcached.pid ]; then
   kill $(cat memcached.pid)
   sleep 1
fi

exit $ret
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
* Tue Oct 14 2025 Remi Collet <remi@remirepo.net> - 3.4.0-1
- update to 3.4.0
- drop patches merged upstream

* Thu Sep 25 2025 Remi Collet <remi@remirepo.net> - 3.3.0-5
- rebuild for PHP 8.5.0RC1

* Wed Jul 30 2025 Remi Collet <remi@remirepo.net> - 3.3.0-4
- add patch for PHP 8.5.0alpha4 from
  https://github.com/php-memcached-dev/php-memcached/pull/574

* Tue Jul 15 2025 Remi Collet <remi@remirepo.net> - 3.3.0-3
- add patch for PHP 8.5.0alpha2 from
  https://github.com/php-memcached-dev/php-memcached/pull/573

* Mon Jul  7 2025 Remi Collet <remi@remirepo.net> - 3.3.0-2
- re-license spec file to CECILL-2.1
- add pie virtual provides

* Fri Oct 18 2024 Remi Collet <remi@remirepo.net> - 3.3.0-1
- update to 3.3.0

* Fri Oct  4 2024 Remi Collet <remi@remirepo.net> - 3.3.0~RC1-1
- update to 3.3.0RC1
- enable zstd compression support

* Tue Jan 30 2024 Remi Collet <remi@remirepo.net> - 3.2.0-9
- fix incompatible pointer types using patch from
  https://github.com/php-memcached-dev/php-memcached/pull/555

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 3.2.0-7
- rebuild for PHP 8.3.0RC1

* Wed Jul 12 2023 Remi Collet <remi@remirepo.net> - 3.2.0-6
- build out of sources tree

* Fri Sep  9 2022 Remi Collet <remi@remirepo.net> - 3.2.0-5
- rebuild for PHP 8.2 with msgpack and igbinary

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 3.2.0-4
- rebuild for PHP 8.2.0RC1

* Thu Jul 28 2022 Remi Collet <remi@remirepo.net> - 3.2.0-3
- more upstream patches for PHP 8.2

* Fri Jun  3 2022 Remi Collet <remi@remirepo.net> - 3.2.0-2
- add upstream patches for PHP 8.2

* Thu Mar 24 2022 Remi Collet <remi@remirepo.net> - 3.2.0-1
- update to 3.2.0

* Wed Mar  9 2022 Remi Collet <remi@remirepo.net> - 3.2.0~rc2-1
- update to 3.2.0RC2

* Mon Mar  7 2022 Remi Collet <remi@remirepo.net> - 3.2.0~rc1-1
- update to 3.2.0RC1

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 3.1.6~DEV-1
- update to 3.1.6-dev (2022-03-02)

* Fri Feb 25 2022 Remi Collet <remi@remirepo.net> - 3.1.5-13
- rebuild using remi-libmemcached-awesome

* Fri Nov  5 2021 Remi Collet <remi@remirepo.net> - 3.1.5-12
- add patch for MemcachedServer from
  https://github.com/php-memcached-dev/php-memcached/pull/474

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 3.1.5-11
- rebuild for 8.1.0RC1

* Tue Jul 27 2021 Remi Collet <remi@remirepo.net> - 3.1.5-10
- add patch to report about libmemcached-awesome from
  https://github.com/php-memcached-dev/php-memcached/pull/488

* Fri Jul 23 2021 Remi Collet <remi@remirepo.net> - 3.1.5-9
- add patch for PHP 8.1.0beta1 from
  https://github.com/php-memcached-dev/php-memcached/pull/487

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 3.1.5-8
- rebuild using remi-libmemcached-awesome (relocated on /opt/remi)

* Thu Jun 24 2021 Remi Collet <remi@remirepo.net> - 3.1.5-6
- rebuild using libmemcached-awesome

* Wed Jun  9 2021 Remi Collet <remi@remirepo.net> - 3.1.5-5
- rebuild with igbinary and msgpack enabled

* Wed Jun  9 2021 Remi Collet <remi@remirepo.net> - 3.1.5-4
- add patch got PHP 8.1 from
  https://github.com/php-memcached-dev/php-memcached/pull/486
- switch to bcond and add option to disable msgpack usage

* Thu Oct  8 2020 Remi Collet <remi@remirepo.net> - 3.1.5-3
- more patches for PHP 8 from
  https://github.com/php-memcached-dev/php-memcached/pull/465
  https://github.com/php-memcached-dev/php-memcached/pull/467
  https://github.com/php-memcached-dev/php-memcached/pull/468
  https://github.com/php-memcached-dev/php-memcached/pull/469
  https://github.com/php-memcached-dev/php-memcached/pull/472
  https://github.com/php-memcached-dev/php-memcached/pull/473

* Thu Oct  8 2020 Remi Collet <remi@remirepo.net> - 3.1.5-3
- add patches for PHP 8 from
  https://github.com/php-memcached-dev/php-memcached/pull/461
  https://github.com/php-memcached-dev/php-memcached/pull/463

* Wed Dec  4 2019 Remi Collet <remi@remirepo.net> - 3.1.5-1
- update to 3.1.5

* Mon Oct  7 2019 Remi Collet <remi@remirepo.net> - 3.1.4-1
- update to 3.1.4

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 3.1.3-4
- rebuild for 7.4.0RC1

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 3.1.3-3
- rebuild for 7.4.0beta1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 3.1.3-2
- rebuild

* Wed Dec 26 2018 Remi Collet <remi@remirepo.net> - 3.1.3-1
- update to 3.1.3

* Sun Dec 23 2018 Remi Collet <remi@remirepo.net> - 3.1.2-1
- update to 3.1.2

* Fri Dec 21 2018 Remi Collet <remi@remirepo.net> - 3.1.1-1
- update to 3.1.1

* Fri Dec 21 2018 Remi Collet <remi@remirepo.net> - 3.1.0-1
- update to 3.1.0

* Tue Nov 20 2018 Remi Collet <remi@remirepo.net> - 3.0.4-8
- rebuild using libmemcached-opt for EL

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 3.0.4-7
- rebuild for 7.3.0beta2 new ABI

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 3.0.4-6
- rebuld for 7.3.0alpha4 new ABI

* Thu Jun 28 2018 Remi Collet <remi@remirepo.net> - 3.0.4-5
- add upstream patch for PHP 7.3

* Tue Feb 27 2018 Remi Collet <remi@remirepo.net> - 3.0.4-4
- bump release

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 3.0.4-2
- add upstream patch to disable binary protocol with
  old libmemcached 1.0.16 in EL-7

* Tue Nov 21 2017 Remi Collet <remi@remirepo.net> - 3.0.4-1
- Update to 3.0.4

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 3.0.3-5
- rebuild for PHP 7.2.0beta1 new API

* Wed Jul 12 2017 Remi Collet <remi@remirepo.net> - 3.0.3-4
- add upstream patch (tests) for PHP 7.2

* Sun Jul  9 2017 Remi Collet <remi@remirepo.net> - 3.0.3-3
- add upstream patch (tests) for PHP 7.2

* Fri Apr 14 2017 Remi Collet <remi@fedoraproject.org> - 3.0.3-2
- ensure we use libevent2 on EL-6

* Mon Feb 20 2017 Remi Collet <remi@fedoraproject.org> - 3.0.3-1
- update to 3.0.3 (php 7, stable)
- build with --enable-memcached-protocol option

* Mon Feb 13 2017 Remi Collet <remi@fedoraproject.org> - 3.0.2-1
- update to 3.0.2 (php 7, stable)

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 3.0.1-3
- test build for https://github.com/php-memcached-dev/php-memcached/pull/320

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 3.0.1-2
- switch to pecl sources
- enable test suite
- open https://github.com/php-memcached-dev/php-memcached/pull/319
  fix test suite for 32bits build

* Tue Feb  7 2017 Remi Collet <remi@fedoraproject.org> - 3.0.1-1
- update to 3.0.1 (php 7, stable)

* Fri Dec  9 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.4.20161207gite65be32
- refresh to more recent snapshot

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.3.20160217git6ace07d
- rebuild with PHP 7.1.0 GA

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.2.20160217git6ace07d
- rebuild for PHP 7.1 new API version

* Thu Mar  3 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-0.1.20160217git6ace07d
- update to 3.0.0-dev
- switch back to php-memcached-dev sources

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-0.2.20150628git3c79a97
- add patch for igbinary, see
  https://github.com/rlerdorf/php-memcached/pull/3

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-0.1.20150628git3c79a97
- bump version to 2.2.1-dev, stability=devel

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-11.20150628git3c79a97
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-10.20150628git3c79a97
- F23 rebuild with rh_layout

* Wed Jul 22 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-9.20150628git3c79a97
- rebuild against php 7.0.0beta2

* Wed Jul  8 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-8.20150628git3c79a97
- new snapshot

* Sat Jun 27 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-7.20150423git4187e22
- switch sources from pecl to github
- temporarily use rlerdorf fork (php7 compatibility)
- disable igbinary
- open https://github.com/rlerdorf/php-memcached/pull/2 - msgpack

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 2.2.0-6
- allow build against rh-php56 (as more-php56)
- don't install/register tests
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-5.1
- Fedora 21 SCL mass rebuild

* Fri Aug 29 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-5
- test build with system fastlz

* Fri Aug 29 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-4
- improve SCL build

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 2.2.0-3
- add numerical prefix to extension configuration file

* Wed Apr  2 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-2
- add all ini options in configuration file (comments)

* Wed Apr  2 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- update to 2.2.0 (stable)
- msgpack not available for ppc64

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 2.2.0-0.3.RC1
- allow SCL build

* Thu Mar 13 2014  Remi Collet <remi@fedoraproject.org> - 2.2.0-0.2.RC1
- update to 2.2.0RC1 (beta)

* Mon Nov 25 2013  Remi Collet <remi@fedoraproject.org> - 2.2.0-0.1.b1
- update to 2.2.0b1 (beta)
- cleanups for Copr
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)
- add dependency on pecl/msgpack
- add --with tests option to run upstream test suite during build

* Fri Nov 15 2013  Remi Collet <remi@fedoraproject.org> - 2.1.0-7
- drop requires libmemcached >= build version
  as this can also be libmemcached-last

* Mon Nov 19 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-6
- requires libmemcached >= build version

* Sat Nov 17 2012  Remi Collet <remi@fedoraproject.org> - 2.1.0-5
- rebuild for libmemcached 1.0.14 (with SASL)
- switch to upstream patch
- add patch to report about SASL support in phpinfo

* Fri Oct 19 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-4
- improve comment in configuration about session.

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-3
- rebuild for new libmemcached
- drop sasl support

* Sat Sep  8 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- sync with rawhide, cleanups
- Obsoletes php53*, php54* on EL

* Tue Aug 07 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- add patch to lower libmemcached required version

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-6
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.4

* Sun Apr 22 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- rebuild for libmemcached 1.0.6 (with SASL) and php 5.3

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-4
- rebuild for libmemcached 1.0.6 and php 5.4

* Sat Apr 21 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- rebuild for libmemcached 1.0.6 and php 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- update to 2.0.1 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 for PHP 5.3

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- update to 2.0.0 for PHP 5.4

* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0 for PHP 5.3

* Wed Nov 16 2011  Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.1736623
- update to git snapshot (post 2.0.0b2) for php 5.4 build

* Sun Oct 16 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-10
- rebuild against latest libmemcached (f16 only)

* Tue Oct 04 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-9
- ZTS extension

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-8
- allow relocation
- work for ZTS (not yet ok)

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- rebuild against libmemcached 0.52
- adapted filter
- clean spec

* Thu Jun 02 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-6
- rebuild against libmemcached 0.49

* Sat Feb 19 2011 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.2
- rebuild for remi repo with SASL for fedora <= 10 and EL <= 5

* Sat Oct 02 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.1
- remove patch 

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3
- rebuild against libmemcached 0.44 with SASL support

* Wed Sep 29 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild with igbinary support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Wed Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

