# remirepo spec file for php-pecl-swoole6
#
# SPDX-FileCopyrightText:  Copyright 2013-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%scl_package       php-pecl-swoole6
%else
%global _root_prefix %{_prefix}
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pie_vend   swoole
%global pie_proj   swoole
%global pecl_name  swoole
# After 20-sockets, 20-json and 20-mysqlnd
%global ini_name   40-%{pecl_name}.ini

%bcond_without     cares
%bcond_without     nghttpd2
# disabled by default to avoid dependency on Oracle Instant Client
%bcond_with        oracle

%ifarch aarch64
%global oraclever 19.22
%global oraclelib 19.1
%global oracledir 19.22
%else
%global oraclever 21.13
%global oraclelib 21.1
%global oracledir 21
%endif


%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without     uring
%else
%bcond_with        uring
%endif

%bcond_without     pgsql
%bcond_without     brotli
%bcond_without     zstd
%bcond_without     curl
%bcond_without     nghttpd2

%global upstream_version 6.0.1
#global upstream_prever  RC1
%global sources          %{pecl_name}-%{upstream_version}%{?upstream_prever}
%global _configure       ../%{sources}/configure

Summary:        PHP's asynchronous concurrent distributed networking framework
Name:           %{?scl_prefix}php-pecl-%{pecl_name}6
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
# Extension is Apache-2.0
# BSD-3-Clause: Hiredis
# MIT: nlohmann/json, nghttp2
License:        Apache-2.0 AND BSD-3-Clause AND MIT
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?dtsprefix}gcc-c++
BuildRequires:  %{?scl_prefix}php-devel >= 8.1
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-curl
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?scl_prefix}php-sockets
BuildRequires:  %{?scl_prefix}php-mysqlnd
BuildRequires:  %{?scl_prefix}php-pdo
BuildRequires:  openssl-devel >= 1.0.2
BuildRequires:  zlib-devel
%if %{with curl}
BuildRequires:  pkgconfig(libcurl)
%endif
%if %{with cares}
BuildRequires:  pkgconfig(libcares)
%endif
%if %{with brotli}
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlienc)
%endif
%if %{with zstd}
BuildRequires:  pkgconfig(libzstd) >= 1.4
%endif
%if %{with pgsql}
BuildRequires:  pkgconfig(libpq)
%endif
%if %{with nghttpd2}
BuildRequires:  pkgconfig(libnghttp2)
%endif
%if %{with uring}
BuildRequires:  pkgconfig(liburing) >= 2.5
%endif
BuildRequires:  pkgconfig(odbc)
BuildRequires:  pkgconfig(sqlite3)
%if %{with oracle}
%ifarch aarch64
BuildRequires:  oracle-instantclient%{oraclever}-devel
# Should requires libclntsh.so.19.1()(aarch-64), but it's not provided by Oracle RPM.
Requires:       libclntsh.so.%{oraclelib}
AutoReq:        0
%else
BuildRequires:  oracle-instantclient-devel >= %{oraclever}
%endif
%endif


Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
Requires:       %{?scl_prefix}php-sockets%{?_isa}
Requires:       %{?scl_prefix}php-mysqlnd%{?_isa}
Requires:       %{?scl_prefix}php-pdo%{?_isa}

Provides:       %{?scl_prefix}php-%{pecl_name}                 = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})           = %{version}
Provides:       %{?scl_prefix}php-pie(%{pie_vend}/%{pie_proj}) = %{version}

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10 || "%{php_version}" >= "8.4"
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}          < 6
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}2         < 6
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2         = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2%{?_isa} = %{version}-%{release}
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}4         < 6
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}4         = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}4%{?_isa} = %{version}-%{release}
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}5         < 6
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}5         = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}5%{?_isa} = %{version}-%{release}
%else
# Single version can be installed
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}  < 6
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}2 < 6
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}4 < 6
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}5 < 6
%endif
# Only one extension can be installed (same symbols)
Conflicts:      %{?scl_prefix}php-pecl-openswoole
Conflicts:      %{?scl_prefix}php-pecl-openswoole22
Conflicts:      %{?scl_prefix}php-pecl-openswoole25


%description
Event-driven asynchronous and concurrent networking engine with
high performance for PHP.
- event-driven
- coroutines
- asynchronous non-blocking
- built-in tcp/http/websocket/http2 server
- coroutine tcp/http/websocket client
- coroutine mysql client
- coroutine redis client
- coroutine read/write file system
- coroutine dns lookup
- automatically replace blocking functions to non-blocking
- support IPv4/IPv6/UnixSocket/TCP/UDP
- support SSL/TLS encrypted transmission

Documentation: https://rawgit.com/tchiotludo/swoole-ide-helper/english/docs/

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       %{name} developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -q -c

# Don't install/register tests, install examples as doc
sed \
   -e '/Makefile/s/role="doc"/role="src"/' \
   -e '/samples/s/role="doc"/role="src"/' \
   -e '/name="library/s/role="doc"/role="src"/' \
   -e '/LICENSE/s/role="doc"/role="src"/' \
   -e '/COPYING/s/role="doc"/role="src"/' \
   -i package.xml


cd %{sources}
cp -p thirdparty/hiredis/COPYING hiredis-COPYING
%if %{with nghttpd2}
rm -r thirdparty/nghttp2
%else
cp -p thirdparty/nghttp2/COPYING nghttp2-COPYING
%endif

# Sanity check, really often broken
extver=$(sed -n '/#define SWOOLE_VERSION /{s/.* "//;s/".*$//;p}' include/swoole_version.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
cd ..

mkdir NTS
%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
mkdir ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;swoole.enable_coroutine = On
;swoole.enable_library = On
;swoole.enable_fiber_mock = Off
;swoole.enable_preemptive_scheduler = Off
;swoole.display_errors = On
:swoole.use_shortname = On
;swoole.unixsock_buffer_size = 8388608
EOF


%build
%{?dtsenable}

peclbuild() {
%configure \
    --enable-swoole \
    --enable-sockets \
    --enable-trace-log \
    --enable-openssl \
    --enable-mysqlnd \
%if %{with pgsql}
    --enable-swoole-pgsql \
%endif
%if %{with curl}
    --enable-swoole-curl \
%endif
    --enable-swoole-coro-time \
%if %{with cares}
    --enable-cares \
%endif
%if %{with brotli}
    --enable-brotli \
%else
    --disable-brotli \
%endif
%if %{with zstd}
    --enable-zstd \
%else
    --disable-zstd \
%endif
%if %{with nghttpd2}
    --with-nghttp2-dir=%{_root_prefix} \
%endif
%if %{with uring}
    --enable-iouring \
%endif
%if %{with oracle}
    --with-swoole-oracle=instantclient,%{_root_prefix}/lib/oracle/%{oracledir}/client64/lib \
%endif
    --with-swoole-odbc=unixodbc,%{_root_prefix} \
    --enable-swoole-sqlite \
    --with-libdir=%{_lib} \
    --with-php-config=$*

# See https://bugzilla.redhat.com/show_bug.cgi?id=2345743
sed -e 's:-Wl,-rpath,/usr/usr/lib64 -L/usr/usr/lib64::' -i Makefile

%make_build
}

cd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global

cd ../NTS
peclbuild %{__phpconfig}

%if %{with_zts}
cd ../ZTS
peclbuild %{__ztsphpconfig} --enable-swoole-thread
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

# Test and Documentation
cd %{sources}
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done

# code not compatible with Python 3
rm %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/swoole_process/echo.py
rm %{buildroot}%{pecl_docdir}/%{pecl_name}/examples/process/echo.py


%check
OPT="--no-php-ini"
[ -f %{php_extdir}/curl.so ]    && OPT="$OPT -d extension=curl"
[ -f %{php_extdir}/sockets.so ] && OPT="$OPT -d extension=sockets"
[ -f %{php_extdir}/mysqlnd.so ] && OPT="$OPT -d extension=mysqlnd"
[ -f %{php_extdir}/pdo.so ]     && OPT="$OPT -d extension=pdo"

cd NTS
: Minimal load test for NTS extension
%{__php} $OPT \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif


%files
%license %{sources}/LICENSE
%license %{sources}/*-COPYING
%doc %{pecl_docdir}/%{pecl_name}/*md
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%doc %{pecl_docdir}/%{pecl_name}/core-tests
%doc %{pecl_docdir}/%{pecl_name}/docs
%doc %{pecl_docdir}/%{pecl_name}/examples
%doc %{pecl_docdir}/%{pecl_name}/gdbinit
%doc %{pecl_docdir}/%{pecl_name}/thirdparty
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Fri Feb 14 2025 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1
- drop patch merged upstream
- provide php-pie(swoole/swoole)

* Mon Dec 16 2024 Remi Collet <remi@remirepo.net> - 6.0.0-5
- update to 6.0.0 GA
- enable zstd support
- re-license spec file to CECILL-2.1
- drop patch merged upstream
- fix cpu affinity check using patch from
  https://github.com/swoole/swoole-src/pull/5624

* Thu Nov 21 2024 Remi Collet <remi@remirepo.net> - 6.0.0-4
- update to 6.0.0RC1
- use 6.0.0-4 to workaround https://github.com/swoole/swoole-src/issues/5531
- drop patch merged upstream
- fix https://github.com/swoole/swoole-src/issues/5577 build with liburing < 2.6
  using patch from https://github.com/swoole/swoole-src/pull/5579

* Tue Oct 22 2024 Remi Collet <remi@remirepo.net> - 6.0.0-3
- add fix for PHP 8.4 from
  https://github.com/swoole/swoole-src/pull/5537

* Tue Oct 22 2024 Remi Collet <remi@remirepo.net> - 6.0.0-2
- update to 6.0.0beta

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 6.0.0-1
- update to 6.0.0alpha
- rename to php-pecl-swoole6
- raise dependency on PHP 8.1

* Thu Jun  6 2024 Remi Collet <remi@remirepo.net> - 5.1.3-1
- update to 5.1.3
- fix build warnings (errors with GCC 14) using patch from
  https://github.com/swoole/swoole-src/pull/5363

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 5.1.2-2
- refresh sources
- drop patch merged upstream

* Wed Jan 24 2024 Remi Collet <remi@remirepo.net> - 5.1.2-1
- update to 5.1.2
- fix out of sources tree build using patch from
  https://github.com/swoole/swoole-src/pull/5239

* Mon Nov 27 2023 Remi Collet <remi@remirepo.net> - 5.1.1-1
- update to 5.1.1

* Fri Sep 29 2023 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0
- add dependency on pdo extension
- new coroutine_odbc enabled
- new coroutine_sqlite enabled
- new coroutine_oracle disabled

* Mon Sep  4 2023 Remi Collet <remi@remirepo.net> - 5.0.3-2
- add upstream patch for PHP 8.3

* Wed Apr 26 2023 Remi Collet <remi@remirepo.net> - 5.0.3-1
- update to 5.0.3
- use system libnghttp2
- drop patch merged upstream
- fix use of system headers with system libnghttp2 using patch from
  https://github.com/swoole/swoole-src/pull/5038
- build out of sources tree

* Fri Feb 17 2023 Remi Collet <remi@remirepo.net> - 5.0.2-2
- fix GCC 13 build using patch from
  https://github.com/swoole/swoole-src/pull/4985

* Mon Feb  6 2023 Remi Collet <remi@remirepo.net> - 5.0.2-1
- update to 5.0.2

* Mon Nov  7 2022 Remi Collet <remi@remirepo.net> - 5.0.1-1
- update to 5.0.1

* Tue Aug  2 2022 Remi Collet <remi@remirepo.net> - 5.0.0-1
- update to 5.0.0
- rename to php-pecl-swoole5
- raise dependency on PHP 8.0
- add postgresql support on Fedora, EL-8 and EL-9
- remove curl support on EL-7

* Tue Jul 12 2022 Remi Collet <remi@remirepo.net> - 4.8.11-1
- update to 4.8.11

* Wed Jun 22 2022 Remi Collet <remi@remirepo.net> - 4.8.10-1
- update to 4.8.10

* Mon Apr 18 2022 Remi Collet <remi@remirepo.net> - 4.8.9-1
- update to 4.8.9
- add workaround to build failure reported as
  https://github.com/swoole/swoole-src/issues/4693

* Wed Mar 16 2022 Remi Collet <remi@remirepo.net> - 4.8.8-1
- update to 4.8.8

* Thu Feb 24 2022 Remi Collet <remi@remirepo.net> - 4.8.7-1
- update to 4.8.7

* Thu Jan 13 2022 Remi Collet <remi@remirepo.net> - 4.8.6-1
- update to 4.8.6

* Sat Dec 25 2021 Remi Collet <remi@remirepo.net> - 4.8.5-1
- update to 4.8.5

* Sat Dec 18 2021 Remi Collet <remi@remirepo.net> - 4.8.4-1
- update to 4.8.4

* Wed Dec  1 2021 Remi Collet <remi@remirepo.net> - 4.8.3-1
- update to 4.8.3

* Thu Nov 18 2021 Remi Collet <remi@remirepo.net> - 4.8.2-1
- update to 4.8.2

* Sat Oct 30 2021 Remi Collet <remi@remirepo.net> - 4.8.1-1
- update to 4.8.1
- open https://github.com/swoole/swoole-src/pull/4457
  add LICENSE file for thirdparty/nlohmann

* Fri Oct 15 2021 Remi Collet <remi@remirepo.net> - 4.8.0-1
- update to 4.8.0

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 4.7.1-2
- rebuild for 8.1.0RC1

* Thu Aug 26 2021 Remi Collet <remi@remirepo.net> - 4.7.1-1
- update to 4.7.1
- drop patch merged upstream

* Fri Jul 23 2021 Remi Collet <remi@remirepo.net> - 4.7.0-2
- add patch for PHP 8.1.0beta1 from
  https://github.com/swoole/swoole-src/pull/4335

* Mon Jul 19 2021 Remi Collet <remi@remirepo.net> - 4.7.0-1
- update to 4.7.0

* Sun May 16 2021 Remi Collet <remi@remirepo.net> - 4.6.7-1
- update to 4.6.7

* Thu Apr 22 2021 Remi Collet <remi@remirepo.net> - 4.6.6-1
- update to 4.6.6

* Fri Apr  9 2021 Remi Collet <remi@remirepo.net> - 4.6.5-1
- update to 4.6.5

* Thu Mar 11 2021 Remi Collet <remi@remirepo.net> - 4.6.4-1
- update to 4.6.4

* Tue Feb  9 2021 Remi Collet <remi@remirepo.net> - 4.6.3-1
- update to 4.6.3

* Mon Jan 25 2021 Remi Collet <remi@remirepo.net> - 4.6.2-1
- update to 4.6.2

* Mon Jan 11 2021 Remi Collet <remi@remirepo.net> - 4.6.1-1
- update to 4.6.1

* Wed Jan  6 2021 Remi Collet <remi@remirepo.net> - 4.6.0-1
- update to 4.6.0
- enable curl support
- raise dependency on PHP 7.2

* Wed Dec 23 2020 Remi Collet <remi@remirepo.net> - 4.5.10-1
- update to 4.5.10

* Fri Nov 27 2020 Remi Collet <remi@remirepo.net> - 4.5.9-1
- update to 4.5.9

* Mon Nov 23 2020 Remi Collet <remi@remirepo.net> - 4.5.8-2
- add upstream patch for PHP 8

* Sat Nov 21 2020 Remi Collet <remi@remirepo.net> - 4.5.8-1
- update to 4.5.8

* Mon Nov  9 2020 Remi Collet <remi@remirepo.net> - 4.5.7-1
- update to 4.5.7

* Fri Oct 30 2020 Remi Collet <remi@remirepo.net> - 4.5.6-1
- update to 4.5.6
- raise dependency on openssl 1.0.2 (drop EL-6 support)
- add dependency on json extension

* Thu Oct 15 2020 Remi Collet <remi@remirepo.net> - 4.5.5-1
- update to 4.5.5
- drop patches merged upstream

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 4.5.4-3
- rebuild for PHP 8.0.0RC1
- add patch from https://github.com/swoole/swoole-src/pull/3713

* Sun Sep 20 2020 Remi Collet <remi@remirepo.net> - 4.5.4-2
- add upstream patch for EL-6 and for PHP 8
- add patch for EL-6 from
  https://github.com/swoole/swoole-src/pull/3686

* Sun Sep 20 2020 Remi Collet <remi@remirepo.net> - 4.5.4-1
- update to 4.5.4
- open https://github.com/swoole/swoole-src/issues/3681 broken build on EL-6
- open https://github.com/swoole/swoole-src/issues/3683 broken build on PHP 8

* Sun Aug 30 2020 Remi Collet <remi@remirepo.net> - 4.5.3-1
- update to 4.5.3

* Thu May 28 2020 Remi Collet <remi@remirepo.net> - 4.5.2-1
- update to 4.5.2

* Mon May 11 2020 Remi Collet <remi@remirepo.net> - 4.5.1-1
- update to 4.5.1

* Mon Apr 27 2020 Remi Collet <remi@remirepo.net> - 4.5.0-2
- add upstream patch to fix 32-bit and old GCC builds

* Mon Apr 27 2020 Remi Collet <remi@remirepo.net> - 4.5.0-1
- update to 4.5.0
- open https://github.com/swoole/swoole-src/issues/3276
  broken 32-bit build

* Sun Apr 26 2020 Remi Collet <remi@remirepo.net> - 4.4.18-1
- update to 4.4.18
- open https://github.com/swoole/swoole-src/issues/3274
  missing libstdc++ in link

* Wed Apr  1 2020 Remi Collet <remi@remirepo.net> - 4.4.17-1
- update to 4.4.17

* Wed Feb 19 2020 Remi Collet <remi@remirepo.net> - 4.4.16-1
- update to 4.4.16

* Wed Jan 15 2020 Remi Collet <remi@remirepo.net> - 4.4.15-1
- update to 4.4.15

* Thu Dec 26 2019 Remi Collet <remi@remirepo.net> - 4.4.14-1
- update to 4.4.14

* Wed Dec 18 2019 Remi Collet <remi@remirepo.net> - 4.4.13-1
- update to 4.4.13

* Wed Dec 11 2019 Remi Collet <remi@remirepo.net> - 4.4.13~RC2-1
- update to 4.4.13RC2

* Thu Dec  5 2019 Remi Collet <remi@remirepo.net> - 4.4.13~RC1-1
- update to 4.4.13RC1

* Mon Nov  4 2019 Remi Collet <remi@remirepo.net> - 4.4.12-1
- update to 4.4.12

* Thu Oct 31 2019 Remi Collet <remi@remirepo.net> - 4.4.10-1
- update to 4.4.10

* Wed Oct 30 2019 Remi Collet <remi@remirepo.net> - 4.4.9-1
- update to 4.4.9
- open https://github.com/swoole/swoole-src/issues/2925
  undefined symbol: BrotliDecoderDecompress

* Tue Oct 15 2019 Remi Collet <remi@remirepo.net> - 4.4.8-1
- update to 4.4.8

* Wed Sep 25 2019 Remi Collet <remi@remirepo.net> - 4.4.7-1
- update to 4.4.7

* Thu Sep 19 2019 Remi Collet <remi@remirepo.net> - 4.4.6-1
- update to 4.4.6

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 4.4.5-2
- rebuild for 7.4.0RC1

* Fri Aug 30 2019 Remi Collet <remi@remirepo.net> - 4.4.5-1
- update to 4.4.5

* Fri Aug 23 2019 Remi Collet <remi@remirepo.net> - 4.4.4-2
- drop echo.py which is python 2 only

* Sun Aug 18 2019 Remi Collet <remi@remirepo.net> - 4.4.4-1
- update to 4.4.4

* Sat Aug  3 2019 Remi Collet <remi@remirepo.net> - 4.4.3-1
- update to 4.4.3

* Fri Jul 26 2019 Remi Collet <remi@remirepo.net> - 4.4.2-1
- update to 4.4.2
- drop patch merged upstream

* Tue Jul 23 2019 Remi Collet <remi@remirepo.net> - 4.4.1-2
- rebuild for 7.4.0beta1
- add patch from https://github.com/swoole/swoole-src/pull/2707

* Tue Jul 16 2019 Remi Collet <remi@remirepo.net> - 4.4.1-1
- update to 4.4.1

* Sun Jul  7 2019 Remi Collet <remi@remirepo.net> - 4.4.0-1
- update to 4.4.0
- raise dependency on PHP 7.1
- drop `Serialize` module
- drop `PostgreSQL` module

* Fri Jun 14 2019 Remi Collet <remi@remirepo.net> - 4.3.5-1
- update to 4.3.5

* Fri May 17 2019 Remi Collet <remi@remirepo.net> - 4.3.4-1
- update to 4.3.4

* Tue Apr 23 2019 Remi Collet <remi@remirepo.net> - 4.3.3-1
- update to 4.3.3

* Mon Apr 15 2019 Remi Collet <remi@remirepo.net> - 4.3.2-1
- update to 4.3.2

* Wed Mar 13 2019 Remi Collet <remi@remirepo.net> - 4.3.1-1
- update to 4.3.1

* Mon Mar 11 2019 Remi Collet <remi@remirepo.net> - 4.3.0-2
- test build for upstream patch

* Thu Mar  7 2019 Remi Collet <remi@remirepo.net> - 4.3.0-1
- update to 4.3.0
- drop dependencies on libnghttp2 and c-ares
- open https://github.com/swoole/swoole-src/issues/2411 32-bit broken
- remove the --enable-trace-log build option on 32-bit

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 4.2.13-1
- update to 4.2.13

* Sun Jan  6 2019 Remi Collet <remi@remirepo.net> - 4.2.12-1
- update to 4.2.12
- use --enable-cares build option
- swoole.aio_thread_num configuration option removed

* Fri Dec 28 2018 Remi Collet <remi@remirepo.net> - 4.2.11-1
- update to 4.2.11

* Thu Dec 20 2018 Remi Collet <remi@remirepo.net> - 4.2.10-1
- update to 4.2.10

* Mon Nov 26 2018 Remi Collet <remi@remirepo.net> - 4.2.9-1
- update to 4.2.9

* Mon Nov 19 2018 Remi Collet <remi@remirepo.net> - 4.2.8-1
- update to 4.2.8

* Sat Nov 10 2018 Remi Collet <remi@remirepo.net> - 4.2.7-1
- update to 4.2.7

* Mon Nov  5 2018 Remi Collet <remi@remirepo.net> - 4.2.6-1
- update to 4.2.6
- use hiredis bundled library
- open https://github.com/swoole/swoole-src/issues/2089 borken with PHP 7.3
- open https://github.com/php/php-src/pull/3652 fix for C++

* Sun Oct 28 2018 Remi Collet <remi@remirepo.net> - 4.2.5-1
- update to 4.2.5

* Fri Oct 26 2018 Remi Collet <remi@remirepo.net> - 4.2.4-1
- update to 4.2.4

* Tue Oct 16 2018 Remi Collet <remi@remirepo.net> - 4.2.3-1
- update to 4.2.3

* Mon Oct 15 2018 Remi Collet <remi@remirepo.net> - 4.2.2-1
- update to 4.2.2
- open https://github.com/swoole/swoole-src/issues/2038 bad version

* Wed Sep 19 2018 Remi Collet <remi@remirepo.net> - 4.2.1-1
- update to 4.2.1

* Tue Sep 18 2018 Remi Collet <remi@remirepo.net> - 4.2.0-1
- update to 4.2.0
- open https://github.com/swoole/swoole-src/issues/1982
  undefined symbol: zif_time_nanosleep
- open https://github.com/swoole/swoole-src/issues/1983
  undefined symbol: php_stream_mode_sanitize_fdopen_fopencookie
- open https://github.com/swoole/swoole-src/issues/1986
  ZTS build is broken: undefined symbol: _Z14virtual_unlinkPKc
- open https://github.com/swoole/swoole-src/pull/1985
  zif_handler to save function pointer

* Wed Sep  5 2018 Remi Collet <remi@remirepo.net> - 4.1.2-1
- update to 4.1.2

* Fri Aug 31 2018 Remi Collet <remi@remirepo.net> - 4.1.1-1
- update to 4.1.1 (no change)

* Fri Aug 31 2018 Remi Collet <remi@remirepo.net> - 4.1.0-1
- update to 4.1.0
- add dependency on brotli library (Fedora)
- open https://github.com/swoole/swoole-src/issues/1931 missing files

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 4.0.4-2
- rebuild for 7.3.0beta2 new ABI

* Sat Aug 11 2018 Remi Collet <remi@remirepo.net> - 4.0.4-1
- update to 4.0.4

* Fri Jul 20 2018 Remi Collet <remi@remirepo.net> - 4.0.3-1
- update to 4.0.3

* Wed Jul 18 2018 Remi Collet <remi@remirepo.net> - 4.0.2-2
- rebuild for 7.3.0alpha4 new ABI

* Fri Jul 13 2018 Remi Collet <remi@remirepo.net> - 4.0.2-1
- update to 4.0.2

* Fri Jun 29 2018 Remi Collet <remi@remirepo.net> - 4.0.1-2
- osboletes old versions on F29+, EL-8+ and PHP 7.3+

* Thu Jun 21 2018 Remi Collet <remi@remirepo.net> - 4.0.1-1
- update to 4.0.1

* Thu Jun 14 2018 Remi Collet <remi@remirepo.net> - 4.0.0-1
- update to 4.0.0
- rename to php-pecl-swoole4
- raise dependency on PHP 7.1
- add patch to ensure g++ is used a linktime from
  https://github.com/swoole/swoole-src/pull/1717

* Wed May 23 2018 Remi Collet <remi@remirepo.net> - 2.2.0-1
- update to 2.2.0

* Mon Apr 16 2018 Remi Collet <remi@remirepo.net> - 2.1.3-1
- update to 2.1.3

* Tue Apr 10 2018 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2
- add PostgreSQL coroutine client on Fedora 24+
- enable trace log
- open https://github.com/swoole/swoole-src/issues/1558
  broken build with PHP 7.0

* Wed Mar  7 2018 Remi Collet <remi@remirepo.net> - 2.1.1-1
- update to 2.1.1

* Fri Feb  9 2018 Remi Collet <remi@remirepo.net> - 2.1.0-1
- Update to 2.1.0
- add swoole.use_shortname option in provided configuration

* Fri Dec 29 2017 Remi Collet <remi@remirepo.net> - 2.0.12-1
- Update to 2.0.12 (stable)
- drop PHP 5 support

* Thu Dec 28 2017 Remi Collet <remi@remirepo.net> - 2.0.11-1
- Update to 2.0.11 (stable)
- add upstream patch to fix broken build with PHP 5.x
  https://github.com/swoole/swoole-src/issues/1433

* Thu Dec 14 2017 Remi Collet <remi@remirepo.net> - 2.0.10-1
- Update to 2.0.10 (stable)

* Thu Aug 31 2017 Remi Collet <remi@remirepo.net> - 2.0.9-1
- Update to 2.0.9 (beta)

* Fri Aug  4 2017 Remi Collet <remi@remirepo.net> - 2.0.8-1
- Update to 2.0.8 (beta)
- add devel sub-package

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 2.0.7-3
- rebuild for PHP 7.2.0beta1 new API

* Fri Mar 17 2017 Remi Collet <remi@remirepo.net> - 2.0.7-2
- fix release

* Fri Mar 17 2017 Remi Collet <remi@remirepo.net> - 2.0.7-1
- Update to 2.0.7 (beta)
- rename to php-pecl-swoole2

* Mon Mar  6 2017 Remi Collet <remi@remirepo.net> - 2.0.6-3
- add upstream patch for
  https://github.com/swoole/swoole-src/issues/1118
- open https://github.com/swoole/swoole-src/issues/1119

* Fri Feb 24 2017 Remi Collet <remi@remirepo.net> - 2.0.6-2
- use --enable-ringbuffer, --enable-thread and --enable-mysqlnd

* Tue Jan 24 2017 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6 (beta)

* Fri Dec 30 2016 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5 (beta)
- raise dependency on PHP 5.5
- add ZTS patch from https://github.com/swoole/swoole-src/pull/992

* Fri Dec 30 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4 (beta)
- open https://github.com/swoole/swoole-src/issues/987 - Options
- open https://github.com/swoole/swoole-src/issues/989 - ZTS build
- disable ZTS extension for now
- open https://github.com/swoole/swoole-src/issues/990 - PHP 5.4

* Fri Dec 23 2016 Remi Collet <remi@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3

* Mon Dec 19 2016 Remi Collet <remi@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2

* Wed Dec  7 2016 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.9.0-2
- rebuild with PHP 7.1.0 GA

* Tue Nov 22 2016 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0

* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.8.13-1
- Update to 1.8.13

* Fri Sep 30 2016 Remi Collet <remi@fedoraproject.org> - 1.8.12-1
- Update to 1.8.12

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.8.11-2
- rebuild for PHP 7.1 new API version

* Fri Sep 09 2016 Remi Collet <remi@fedoraproject.org> - 1.8.11-1
- Update to 1.8.11

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.10-1
- Update to 1.8.10

* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.9-1
- Update to 1.8.9

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.8.8-2
- add upstream patch and add back --enable-http2 build option

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 1.8.8-1
- Update to 1.8.8
- drop --enable-http2 build option (broken)
  open https://github.com/swoole/swoole-src/issues/787

* Fri Jul 01 2016 Remi Collet <remi@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7

* Thu Jun 16 2016 Remi Collet <remi@fedoraproject.org> - 1.8.6-1
- Update to 1.8.6
- drop --enable-async-mysql and --enable-async-httpclient
  removed upstream

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> - 1.8.5-1
- Update to 1.8.5

* Wed Apr 13 2016 Remi Collet <remi@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4 (stable)

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 1.8.3-1
- Update to 1.8.3 (stable)

* Wed Mar 02 2016 Remi Collet <remi@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2 (stable)
- add --enable-openssl, --enable-async-httpclient
  --enable-http2 and --enable-async-redis to build options

* Thu Feb  4 2016 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1 (stable)

* Wed Jan 27 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0 (stable)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.22-2
- Update to 1.7.22 (new sources)

* Thu Dec 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.22-1
- Update to 1.7.22
- add patch to fix PHP 7 build
  open https://github.com/swoole/swoole-src/pull/462
  open https://github.com/swoole/swoole-src/issues/461

* Tue Dec 01 2015 Remi Collet <remi@fedoraproject.org> - 1.7.21-1
- Update to 1.7.21

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.7.20-1
- Update to 1.7.20

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-4
- rebuild for PHP 7.0.0RC5 new API version

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-3
- F23 rebuild with rh_layout

* Thu Sep  3 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-2
- allow build against rh-php56 (as more-php56)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.7.19-1
- Update to 1.7.19

* Thu Jul 23 2015 Remi Collet <remi@fedoraproject.org> - 1.7.18-1
- Update to 1.7.18

* Mon Jun 01 2015 Remi Collet <remi@fedoraproject.org> - 1.7.17-1
- Update to 1.7.17

* Fri May 08 2015 Remi Collet <remi@fedoraproject.org> - 1.7.16-1
- Update to 1.7.16

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 1.7.15-1
- Update to 1.7.15

* Thu Mar 26 2015 Remi Collet <remi@fedoraproject.org> - 1.7.14-1
- Update to 1.7.14

* Wed Mar 18 2015 Remi Collet <remi@fedoraproject.org> - 1.7.13-1
- Update to 1.7.13

* Thu Mar 12 2015 Remi Collet <remi@fedoraproject.org> - 1.7.12-1
- Update to 1.7.12

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 1.7.11-2
- rebuild with new sources

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 1.7.11-1
- Update to 1.7.11

* Sun Feb 15 2015 Remi Collet <remi@fedoraproject.org> - 1.7.10-1
- Update to 1.7.10
- drop runtime dependency on pear, new scriptlets

* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.7.8-1.1
- Fedora 21 SCL mass rebuild

* Wed Nov 26 2014 Remi Collet <remi@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8 (stable)

* Tue Oct 28 2014 Remi Collet <remi@fedoraproject.org> - 1.7.7-1
- Update to 1.7.7 (stable)

* Fri Oct 10 2014 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6 (stable)

* Wed Sep 10 2014 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- Update to 1.7.5 (stable)

* Tue Aug 26 2014 Remi Collet <rcollet@redhat.com> - 1.7.4-2
- improve SCL build

* Tue Jul 15 2014 Remi Collet <remi@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4 (stable)

* Fri Jun 20 2014 Remi Collet <remi@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3 (stable)

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2 (stable)
- open https://github.com/matyhtf/swoole/pull/67 (fix EL5 build)

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1 (stable)

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sun Apr 13 2014 Remi Collet <remi@fedoraproject.org> - 1.6.12-1
- Update to 1.6.12

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 1.6.11-2
- no --enable-async-mysql with php 5.3

* Thu Feb 27 2014 Remi Collet <remi@fedoraproject.org> - 1.6.11-1
- Update to 1.6.11

* Sun Jan 26 2014 Remi Collet <remi@fedoraproject.org> - 1.6.10-1
- Update to 1.6.10

* Thu Jan 02 2014 Remi Collet <remi@fedoraproject.org> - 1.6.9-1
- Update to 1.6.9 (stable)

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 1.6.8-1
- Update to 1.6.8 (stable)

* Tue Dec 24 2013 Remi Collet <rcollet@redhat.com> - 1.6.7-1
- initial package, version 1.6.7 (stable)
- open https://github.com/matyhtf/swoole/issues/14 - archive
- open https://github.com/matyhtf/swoole/issues/15 - php 5.5
