# remirepo spec file for php-pecl-swoole4
#
# Copyright (c) 2013-2021 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

# we don't want -z defs linker flag
%undefine _strict_symbol_defs_build

%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%scl_package       php-pecl-swoole4
%endif

%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global pecl_name  swoole
# After 20-sockets, 20-json and 20-mysqlnd
%global ini_name    40-%{pecl_name}.ini

%global with_nghttpd2 1
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 8
%global with_brotli   1
%else
%global with_brotli   0
%endif

%global upstream_version 4.6.6
#global upstream_prever  RC2


Summary:        PHP's asynchronous concurrent distributed networking framework
Name:           %{?sub_prefix}php-pecl-%{pecl_name}4
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
# Extension is ASL 2.0
# Hiredis is BSD
License:        ASL 2.0 and BSD
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{pecl_name}-%{upstream_version}%{?upstream_prever}.tgz

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?dtsprefix}gcc-c++
BuildRequires:  %{?scl_prefix}php-devel >= 7.2
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-curl
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  %{?scl_prefix}php-sockets
BuildRequires:  %{?scl_prefix}php-mysqlnd
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel >= 1.0.2
BuildRequires:  zlib-devel
BuildRequires:  libcurl-devel
%if %{with_brotli}
BuildRequires:  brotli-devel
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
Requires:       %{?scl_prefix}php-sockets%{?_isa}
Requires:       %{?scl_prefix}php-mysqlnd%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}4         = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}4%{?_isa} = %{version}-%{release}
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}  < 2
Conflicts:      %{?scl_prefix}php-pecl-%{pecl_name}2 < 4
%endif

%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8 || "%{php_version}" > "7.3"
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}          < 4
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
Obsoletes:     %{?scl_prefix}php-pecl-%{pecl_name}2         < 4
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2         = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}2%{?_isa} = %{version}-%{release}
%else
# Single version can be installed
Conflicts:      %{?sub_prefix}php-pecl-%{pecl_name}  < 4
Conflicts:      %{?sub_prefix}php-pecl-%{pecl_name}2 < 4
%endif

%if "%{?packager}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
%if "%{php_version}" > "7.3"
Obsoletes:      php73-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.4"
Obsoletes:      php74-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "8.0"
Obsoletes:      php80-pecl-%{pecl_name} <= %{version}
%endif
%endif


%description
Event-driven asynchronous and concurrent networking engine with
high performance for PHP.
- event-driven
- asynchronous non-blocking
- multi-thread reactor
- multi-process worker
- multi-protocol
- millisecond timer
- async mysql client
- built-in http/websocket/http2 server
- async http/websocket client
- async redis client
- async task
- async read/write file system
- async dns lookup
- support IPv4/IPv6/UnixSocket/TCP/UDP
- support SSL/TLS encrypted transmission

Documentation: https://rawgit.com/tchiotludo/swoole-ide-helper/english/docs/

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       %{name} developer files (header)
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}-devel = %{version}-%{release}
Provides:      %{?scl_prefix}php-pecl-%{pecl_name}-devel%{?_isa} = %{version}-%{release}
%endif

%description devel
These are the files needed to compile programs using %{name}.


%prep
%setup -q -c
mv %{pecl_name}-%{upstream_version}%{?upstream_prever} NTS


# Don't install/register tests, install examples as doc
sed \
   -e '/Makefile/s/role="doc"/role="src"/' \
   -e '/samples/s/role="doc"/role="src"/' \
   -e '/name="library/s/role="doc"/role="src"/' \
   %{?_licensedir: -e '/LICENSE/s/role="doc"/role="src"/' } \
   %{?_licensedir: -e '/COPYING/s/role="doc"/role="src"/' } \
   -i package.xml


cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define SWOOLE_VERSION /{s/.* "//;s/".*$//;p}' include/swoole_version.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Configuration
;swoole.enable_coroutine = On
;swoole.enable_library = On
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
    --enable-http2 \
    --enable-mysqlnd \
    --enable-swoole-json \
    --enable-swoole-curl \
    --with-libdir=%{_lib} \
    --with-php-config=$1

make %{?_smp_mflags}
}

cd NTS
%{_bindir}/phpize
peclbuild %{_bindir}/php-config

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
peclbuild %{_bindir}/zts-php-config
%endif


%install
%{?dtsenable}

make -C NTS \
     install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS \
     install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test and Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done

# code not compatible with Python 3
rm %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/swoole_process/echo.py
rm %{buildroot}%{pecl_docdir}/%{pecl_name}/examples/process/echo.py


%if 0%{?fedora} < 24 && 0%{?rhel} < 8
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
OPT="--no-php-ini"
[ -f %{php_extdir}/curl.so ]    && OPT="$OPT -d extension=curl.so"
[ -f %{php_extdir}/json.so ]    && OPT="$OPT -d extension=json.so"
[ -f %{php_extdir}/sockets.so ] && OPT="$OPT -d extension=sockets.so"
[ -f %{php_extdir}/mysqlnd.so ] && OPT="$OPT -d extension=mysqlnd.so"

cd NTS
: Minimal load test for NTS extension
%{__php} $OPT \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} $OPT \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%{?_licensedir:%license NTS/thirdparty/hiredis/COPYING}
%{!?_licensedir:%{pecl_docdir}/%{pecl_name}/LICENSE}
%{!?_licensedir:%{pecl_docdir}/%{pecl_name}/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}/*md
%doc %{pecl_docdir}/%{pecl_name}/CREDITS
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%doc %{pecl_docdir}/%{pecl_name}/examples
%doc %{pecl_docdir}/%{pecl_name}/gdbinit
%doc %{pecl_docdir}/%{pecl_name}/thirdparty
%doc %{pecl_docdir}/%{pecl_name}/travis
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
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
