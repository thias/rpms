# remirepo spec file for php-pecl-grpc
#
# SPDX-FileCopyrightText:  Copyright 2017-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%scl_package php-pecl-grpc
%else
%global _root_prefix %{_prefix}
%endif

## TODO: not suitable for Fedora, tons of bundled libraries
## use mock with --cleanup-after

## TODO: cleanup --with-openssl-dir, needed for PHP < 7.4
%bcond_without           openssl

%global pecl_name        grpc
%global pie_vend         grpc
%global pie_proj         grpc-php-ext
%global with_zts         0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name         40-%{pecl_name}.ini
%global upstream_version 1.82.1
#global upstream_prever  RC1
# Github forge
%global gh_vend          %{pie_vend}
%global gh_proj          %{pie_proj}
%global forgeurl         https://github.com/%{gh_vend}/%{gh_proj}
%global tag              v%{upstream_version}%{?upstream_prever}
# for EL-8 to avoid TAG usage
%global archivename      %{gh_proj}-%{upstream_version}%{?upstream_prever}
%global _configure       ../configure
# Disable LTO (erratic crash during build)
%define _lto_cflags      %{nil}

Name:           %{?scl_prefix}php-pecl-%{pecl_name}
Summary:        General RPC framework
License:        Apache-2.0
Version:        %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:        1%{?dist}
%forgemeta
URL:            %{forgeurl}
Source0:        %{forgesource}

Patch0:         %{pecl_name}-build.patch
Patch2:         %{pecl_name}-workaround.patch
Patch3:         %{pecl_name}-openssl.patch

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc >= 7.0
BuildRequires:  %{?dtsprefix}gcc-c++
BuildRequires:  %{?scl_prefix}php-devel >= 7.0
BuildRequires:  zlib-devel
%if %{with openssl}
BuildRequires:  openssl-devel
%if 0%{?fedora} >= 41
BuildRequires:  openssl-devel-engine
%endif
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

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
Remote Procedure Calls (RPCs) provide a useful abstraction for building
distributed applications and services. The libraries in this repository
provide a concrete implementation of the gRPC protocol, layered over HTTP/2.
These libraries enable communication between clients and servers using
any combination of the supported languages

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%forgesetup

%patch -P0 -p1 -b .rpm
%patch -P2 -p1 -b .nolog
%if %{with openssl}
%patch -P3 -p1 -b .openssl
sed -e '/boringssl-with-bazel/d' -i config.m4
rm -r third_party/boringssl-with-bazel
%endif

#sed -e '/PHP_GRPC_VERSION/s/RC3/RC2/' -i src/php/ext/grpc/version.h
# Sanity check, really often broken
extver=$(sed -n '/PHP_GRPC_VERSION/{s/.* "//;s/".*$//;p}' src/php/ext/grpc/version.h)
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}
   exit 1
fi

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

# Create configuration file
cat << 'EOF' | tee %{ini_name}
; Enable "%{summary}" extension module
extension=%{pecl_name}.so

; Configuration
;grpc.enable_fork_support = 0
;grpc.poll_strategy = ''
;grpc.grpc_verbosity = ''
;grpc.grpc_trace = ''
EOF


%build
%{?dtsenable}

%{__phpize}
[ -f Makefile.global ] && GLOBAL=Makefile.global || GLOBAL=build/Makefile.global
sed -e 's/INSTALL_ROOT/DESTDIR/' -i $GLOBAL

cd NTS
%configure \
    --enable-grpc \
    --with-openssl-dir=%{_root_prefix} \
    --with-libdir=%{_lib} \
    --with-php-config=%{__phpconfig}

%make_build

%if %{with_zts}
cd ../ZTS
%configure \
    --enable-grpc \
    --with-openssl-dir=%{_root_prefix} \
    --with-libdir=%{_lib} \
    --with-php-config=%{__ztsphpconfig}

%make_build
%endif


%install
%{?dtsenable}

%make_install -C NTS

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
%make_install -C ZTS

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
cd NTS
%{__php} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
: Minimal load test for ZTS extension
cd ../ZTS
%{__ztsphp} --no-php-ini \
    --define extension=modules/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif


%files
%license LICENSE
%doc composer.json
%doc *.md

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Sat Jul 11 2026 Remi Collet <remi@remirepo.net> - 1.82.1-1
- update to 1.82.1
- drop pear/pecl dependency
- sources from github
- add pie virtual provides
- report PIE vs PECL minimal PHP version inconsistency
  as https://github.com/grpc/grpc/issues/42798

* Fri Jul  3 2026 Remi Collet <remi@remirepo.net> - 1.82.0-1
- update to 1.82.0

* Tue Jun  2 2026 Remi Collet <remi@remirepo.net> - 1.81.0-1
- update to 1.81.0

* Mon May 18 2026 Remi Collet <remi@remirepo.net> - 1.81.0~RC1-1
- update to 1.81.0RC1

* Tue Mar 31 2026 Remi Collet <remi@remirepo.net> - 1.80.0-1
- update to 1.80.0

* Wed Mar 18 2026 Remi Collet <remi@remirepo.net> - 1.80.0~RC1-1
- update to 1.80.0RC1

* Fri Feb  6 2026 Remi Collet <remi@remirepo.net> - 1.78.0-1
- update to 1.78.0

* Mon Jan 19 2026 Remi Collet <remi@remirepo.net> - 1.78.0~RC2-1
- update to 1.78.0RC2

* Tue Jan  6 2026 Remi Collet <remi@remirepo.net> - 1.78.0~RC1-1
- update to 1.78.0RC1

* Fri Oct 24 2025 Remi Collet <remi@remirepo.net> - 1.76.0-1
- update to 1.76.0

* Sun Oct  5 2025 Remi Collet <remi@remirepo.net> - 1.76.0~RC1-1
- update to 1.76.0RC1

* Tue Sep 16 2025 Remi Collet <remi@remirepo.net> - 1.75.0-1
- update to 1.75.0

* Tue Sep  9 2025 Remi Collet <remi@remirepo.net> - 1.75.0~RC1-1
- update to 1.75.0RC1

* Fri Jul 25 2025 Remi Collet <remi@remirepo.net> - 1.74.0-1
- update to 1.74.0

* Fri Jul 18 2025 Remi Collet <remi@remirepo.net> - 1.74.0~RC2-1
- update to 1.74.0RC2

* Thu Jul 17 2025 Remi Collet <remi@remirepo.net> - 1.73.0-2
- fix build with PHP 8.5.0alpha2 using private patch
  reported as https://github.com/zeromq/php-zmq/pull/240

* Wed Jun 18 2025 Remi Collet <remi@remirepo.net> - 1.73.0-1
- update to 1.73.0

* Tue Jun  3 2025 Remi Collet <remi@remirepo.net> - 1.73.0~RC2-1
- update to 1.73.0RC2

* Tue Apr 29 2025 Remi Collet <remi@remirepo.net> - 1.72.0-1
- update to 1.72.0

* Wed Apr  9 2025 Remi Collet <remi@remirepo.net> - 1.72.0~RC1-1
- update to 1.72.0RC1

* Wed Mar 12 2025 Remi Collet <remi@remirepo.net> - 1.71.0-1
- update to 1.71.0

* Wed Feb 26 2025 Remi Collet <remi@remirepo.net> - 1.71.0~RC2-1
- update to 1.71.0RC2

* Fri Jan 31 2025 Remi Collet <remi@remirepo.net> - 1.70.0-1
- update to 1.70.0

* Thu Jan 16 2025 Remi Collet <remi@remirepo.net> - 1.70.0~RC1-1
- update to 1.70.0RC1

* Tue Jan  7 2025 Remi Collet <remi@remirepo.net> - 1.69.0-1
- update to 1.69.0

* Tue Dec 17 2024 Remi Collet <remi@remirepo.net> - 1.69.0~RC1-1
- update to 1.69.0RC1
- re-license spec file to CECILL-2.1

* Tue Nov 19 2024 Remi Collet <remi@remirepo.net> - 1.68.0-1
- update to 1.68.0

* Thu Oct 17 2024 Remi Collet <remi@remirepo.net> - 1.67.0-1
- update to 1.67.0

* Mon Aug 26 2024 Remi Collet <remi@remirepo.net> - 1.66.0-1
- update to 1.66.0

* Mon Aug 19 2024 Remi Collet <remi@remirepo.net> - 1.66.0~RC5-1
- update to 1.66.0RC5

* Tue Aug 13 2024 Remi Collet <remi@remirepo.net> - 1.66.0~RC3-2
- use system openssl

* Tue Aug 13 2024 Remi Collet <remi@remirepo.net> - 1.66.0~RC3-1
- update to 1.66.0RC3

* Mon Jul 29 2024 Remi Collet <remi@remirepo.net> - 1.65.2-1
- update to 1.65.2

* Wed Jul 17 2024 Remi Collet <remi@remirepo.net> - 1.65.1-2
- better fix for https://github.com/grpc/grpc/issues/37178
  from https://github.com/abseil/abseil-cpp/pull/1718

* Wed Jul 17 2024 Remi Collet <remi@remirepo.net> - 1.65.1-1
- update to 1.65.1
- add patch to workaround to https://github.com/grpc/grpc/issues/37178

* Tue Jul  9 2024 Remi Collet <remi@remirepo.net> - 1.65.0-1
- update to 1.65.0

* Mon Jul  8 2024 Remi Collet <remi@remirepo.net> - 1.65.0~RC2-1
- update to 1.65.0RC2
- report https://github.com/grpc/grpc/issues/37178 unwanted log output

* Mon Jun  3 2024 Remi Collet <remi@remirepo.net> - 1.64.1-1
- update to 1.64.1

* Thu May 30 2024 Remi Collet <remi@remirepo.net> - 1.64.0~RC2-1
- update to 1.64.0RC2

* Fri May 17 2024 Remi Collet <remi@remirepo.net> - 1.63.0-2
- add boringssl upstream patch for GCC 14

* Wed May  1 2024 Remi Collet <remi@remirepo.net> - 1.63.0-1
- update to 1.63.0

* Wed Apr 17 2024 Remi Collet <remi@remirepo.net> - 1.63.0~RC1-1
- update to 1.63.0RC1

* Thu Feb 22 2024 Remi Collet <remi@remirepo.net> - 1.62.0-1
- update to 1.62.0

* Tue Feb 20 2024 Remi Collet <remi@remirepo.net> - 1.62.0~RC1-1
- update to 1.62.0RC1
- report broken build using GCC 14 on Fedora 40
  https://github.com/grpc/grpc/issues/35945

* Tue Feb  6 2024 Remi Collet <remi@remirepo.net> - 1.61.0-1
- update to 1.61.0

* Fri Dec  1 2023 Remi Collet <remi@remirepo.net> - 1.60.0-1
- update to 1.60.0

* Fri Nov 17 2023 Remi Collet <remi@remirepo.net> - 1.60.0~RC1-1
- update to 1.60.0RC1

* Tue Oct 17 2023 Remi Collet <remi@remirepo.net> - 1.59.1-1
- update to 1.59.1

* Thu Sep 28 2023 Remi Collet <remi@remirepo.net> - 1.59.0~RC1-1
- update to 1.59.0RC1

* Thu Sep  7 2023 Remi Collet <remi@remirepo.net> - 1.58.0-1
- update to 1.58.0

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 1.57.0-2
- rebuild for PHP 8.3.0RC1

* Sat Aug 19 2023 Remi Collet <remi@remirepo.net> - 1.57.0-1
- update to 1.57.0
- build out of sources tree

* Mon Jun 19 2023 Remi Collet <remi@remirepo.net> - 1.56.0-1
- update to 1.56.0

* Mon Jun  5 2023 Remi Collet <remi@remirepo.net> - 1.56.0~RC1-1
- update to 1.56.0RC1

* Tue May 23 2023 Remi Collet <remi@remirepo.net> - 1.55.0-1
- update to 1.55.0

* Tue May  2 2023 Remi Collet <remi@remirepo.net> - 1.55.0~RC1-1
- update to 1.55.0RC1

* Tue Apr 18 2023 Remi Collet <remi@remirepo.net> - 1.54.0-1
- update to 1.54.0

* Mon Mar 27 2023 Remi Collet <remi@remirepo.net> - 1.53.0-1
- update to 1.53.0

* Tue Mar 14 2023 Remi Collet <remi@remirepo.net> - 1.53.0~RC2-1
- update to 1.53.0RC2

* Thu Mar  2 2023 Remi Collet <remi@remirepo.net> - 1.53.0~RC1-1
- update to 1.53.0RC1
- use GCC 7 on EL-7 with PHP <= 7.2

* Mon Feb 27 2023 Remi Collet <remi@remirepo.net> - 1.52.1-1
- update to 1.52.1

* Thu Jan 26 2023 Remi Collet <remi@remirepo.net> - 1.52.0~RC1-1
- update to 1.52.0RC1

* Wed Nov 30 2022 Remi Collet <remi@remirepo.net> - 1.51.1-1
- update to 1.51.1

* Tue Oct 18 2022 Remi Collet <remi@remirepo.net> - 1.50.0-1
- update to 1.50.0

* Tue Oct  4 2022 Remi Collet <remi@remirepo.net> - 1.50.0~RC1-1
- update to 1.50.0RC1

* Wed Sep 21 2022 Remi Collet <remi@remirepo.net> - 1.49.0-1
- update to 1.49.0

* Wed Sep  7 2022 Remi Collet <remi@remirepo.net> - 1.48.1-1
- update to 1.48.1

* Thu Jul 21 2022 Remi Collet <remi@remirepo.net> - 1.48.0-1
- update to 1.48.0

* Thu Jul  7 2022 Remi Collet <remi@remirepo.net> - 1.47.0-1
- update to 1.47.0

* Thu May 26 2022 Remi Collet <remi@remirepo.net> - 1.46.3-1
- update to 1.46.3

* Wed May 25 2022 Remi Collet <remi@remirepo.net> - 1.46.1-1
- update to 1.46.1

* Mon Mar 28 2022 Remi Collet <remi@remirepo.net> - 1.45.0-1
- update to 1.45.0

* Thu Feb 24 2022 Remi Collet <remi@remirepo.net> - 1.44.0-1
- update to 1.44.0

* Mon Jan 31 2022 Remi Collet <remi@remirepo.net> - 1.44.0~RC2-1
- update to 1.44.0RC2

* Fri Jan  7 2022 Remi Collet <remi@remirepo.net> - 1.43.0-1
- update to 1.43.0

* Thu Dec  9 2021 Remi Collet <remi@remirepo.net> - 1.43.0~RC1-1
- update to 1.43.0RC1

* Fri Nov 19 2021 Remi Collet <remi@remirepo.net> - 1.42.0-1
- update to 1.42.0

* Tue Nov  9 2021 Remi Collet <remi@remirepo.net> - 1.42.0~RC1-1
- update to 1.42.0RC1

* Tue Sep 28 2021 Remi Collet <remi@remirepo.net> - 1.41.0-1
- update to 1.41.0

* Sat Sep 18 2021 Remi Collet <remi@remirepo.net> - 1.40.0-1
- update to 1.40.0

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 1.39.0-2
- rebuild for 8.1.0RC1

* Sun Jul 25 2021 Remi Collet <remi@remirepo.net> - 1.39.0-1
- update to 1.39.0

* Tue May 25 2021 Remi Collet <remi@remirepo.net> - 1.38.0-1
- update to 1.38.0

* Wed May 12 2021 Remi Collet <remi@remirepo.net> - 1.38.0~RC1-1
- update to 1.38.0RC1

* Sat May  1 2021 Remi Collet <remi@remirepo.net> - 1.37.1-1
- update to 1.37.1

* Fri Apr  9 2021 Remi Collet <remi@remirepo.net> - 1.37.0-1
- update to 1.37.0

* Wed Apr  7 2021 Remi Collet <remi@remirepo.net> - 1.37.0~RC1-1
- update to 1.37.0RC1

* Tue Mar  2 2021 Remi Collet <remi@remirepo.net> - 1.36.0-1
- update to 1.36.0

* Thu Jan 21 2021 Remi Collet <remi@remirepo.net> - 1.35.0-1
- update to 1.35.0

* Fri Jan  8 2021 Remi Collet <remi@remirepo.net> - 1.35.0~RC1-1
- update to 1.35.0RC1

* Thu Dec  3 2020 Remi Collet <remi@remirepo.net> - 1.34.0-1
- update to 1.34.0

* Wed Nov 25 2020 Remi Collet <remi@remirepo.net> - 1.34.0~RC2-1
- update to 1.34.0RC2

* Sat Nov 21 2020 Remi Collet <remi@remirepo.net> - 1.34.0~RC1-1
- update to 1.34.0RC1
- raise dependency on PHP 7.0

* Thu Oct 22 2020 Remi Collet <remi@remirepo.net> - 1.33.1-1
- update to 1.33.1

* Fri Oct  9 2020 Remi Collet <remi@remirepo.net> - 1.33.0~RC1-1
- update to 1.33.0RC1

* Sat Sep 12 2020 Remi Collet <remi@remirepo.net> - 1.32.0-1
- update to 1.32.0

* Wed Sep  2 2020 Remi Collet <remi@remirepo.net> - 1.32.0~RC1-1
- update to 1.32.0RC1

* Wed Aug 26 2020 Remi Collet <remi@remirepo.net> - 1.31.1-1
- update to 1.31.1

* Thu Aug  6 2020 Remi Collet <remi@remirepo.net> - 1.30.0-1
- update to 1.31.0

* Fri Jul 24 2020 Remi Collet <remi@remirepo.net> - 1.30.0~RC1-1
- update to 1.31.0RC1

* Tue Jun 23 2020 Remi Collet <remi@remirepo.net> - 1.30.0-1
- update to 1.30.0

* Mon Jun  8 2020 Remi Collet <remi@remirepo.net> - 1.30.0~RC1-1
- update to 1.30.0RC1

* Thu May 21 2020 Remi Collet <remi@remirepo.net> - 1.29.1-1
- update to 1.29.1

* Wed May 20 2020 Remi Collet <remi@remirepo.net> - 1.29.0-1
- update to 1.29.0

* Fri Apr  3 2020 Remi Collet <remi@remirepo.net> - 1.28.0-1
- Update to 1.28.0

* Wed Mar 18 2020 Remi Collet <remi@remirepo.net> - 1.28.0~RC2-1
- Update to 1.28.0RC2

* Mon Mar  2 2020 Remi Collet <remi@remirepo.net> - 1.28.0~RC1-1
- Update to 1.28.0RC1

* Tue Feb 11 2020 Pablo Greco <pgreco@centosproject.org> - 1.27.0-2
- Update armhfp patch

* Thu Feb  6 2020 Remi Collet <remi@remirepo.net> - 1.27.0-1
- Update to 1.27.0

* Fri Jan 31 2020 Remi Collet <remi@remirepo.net> - 1.27.0~RC2-1
- Update to 1.27.0RC2

* Fri Jan 24 2020 Remi Collet <remi@remirepo.net> - 1.27.0~RC1-1
- Update to 1.27.0RC1

* Fri Dec 20 2019 Remi Collet <remi@remirepo.net> - 1.26.0-1
- Update to 1.26.0

* Sat Dec  7 2019 Remi Collet <remi@remirepo.net> - 1.26.0~RC2-1
- Update to 1.26.0RC2

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 1.26.0~RC1-1
- Update to 1.26.0RC1
- open https://github.com/grpc/grpc/issues/21409 PHP 5.5

* Thu Nov  7 2019 Remi Collet <remi@remirepo.net> - 1.25.0-1
- Update to 1.25.0

* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 1.25.0~RC1-1
- Update to 1.25.0RC1

* Thu Sep 26 2019 Remi Collet <remi@remirepo.net> - 1.24.0-1
- Update to 1.24.0

* Thu Sep 12 2019 Remi Collet <remi@remirepo.net> - 1.24.0~RC1-1
- Update to 1.24.0RC1

* Tue Sep 03 2019 Remi Collet <remi@remirepo.net> - 1.23.0-3
- rebuild for 7.4.0RC1

* Sat Aug 24 2019 Remi Collet <remi@remirepo.net> - 1.23.0-2
- fix build with GCC 9.1 with upstream patch and patch from
  https://github.com/grpc/grpc/pull/20067

* Sat Aug 17 2019 Remi Collet <remi@remirepo.net> - 1.23.0-1
- Update to 1.23.0

* Sat Aug  3 2019 Remi Collet <remi@remirepo.net> - 1.23.0~RC1-1
- Update to 1.23.0RC1

* Thu Jul 18 2019 Pablo Greco <pgreco@centosproject.org> - 1.22.0-2
- Fix build on armhfp, pthread_atfork not exported

* Thu Jul  4 2019 Remi Collet <remi@remirepo.net> - 1.22.0-1
- Update to 1.22.0

* Thu Jun 27 2019 Remi Collet <remi@remirepo.net> - 1.22.0~RC1-1
- Update to 1.22.0RC1

* Tue Jun  4 2019 Remi Collet <remi@remirepo.net> - 1.21.3-1
- update to 1.21.3

* Fri May 31 2019 Remi Collet <remi@remirepo.net> - 1.21.2-1
- Update to 1.21.2

* Tue May 21 2019 Remi Collet <remi@remirepo.net> - 1.21.0~RC1-1
- Update to 1.21.0RC1

* Sat Apr 27 2019 Remi Collet <remi@remirepo.net> - 1.20.0-1
- Update to 1.20.0

* Tue Apr  9 2019 Remi Collet <remi@remirepo.net> - 1.20.0~RC3-1
- Update to 1.20.0RC3

* Tue Apr  2 2019 Remi Collet <remi@remirepo.net> - 1.20.0~RC1-1
- Update to 1.20.0RC1
- add new runtime options in provided configuration

* Wed Feb 27 2019 Remi Collet <remi@remirepo.net> - 1.19.0-1
- Update to 1.19.0

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 1.19.0~RC1-1
- Update to 1.19.0RC1

* Fri Jan 18 2019 Remi Collet <remi@remirepo.net> - 1.18.0-1
- Update to 1.18.0

* Wed Jan  9 2019 Remi Collet <remi@remirepo.net> - 1.18.0~RC1-1
- Update to 1.18.0RC1

* Wed Dec  5 2018 Remi Collet <remi@remirepo.net> - 1.17.0-1
- Update to 1.17.0

* Thu Nov 29 2018 Remi Collet <remi@remirepo.net> - 1.17.0~RC3-1
- Update to 1.17.0RC3

* Wed Nov 21 2018 Remi Collet <remi@remirepo.net> - 1.17.0~RC2-1
- Update to 1.17.0RC2
- open https://github.com/grpc/grpc/issues/17273 ZTS build is broken

* Tue Oct 23 2018 Remi Collet <remi@remirepo.net> - 1.16.0-1
- update to 1.16.0

* Thu Sep 13 2018 Remi Collet <remi@remirepo.net> - 1.15.0-1
- Update to 1.15.0

* Wed Aug 29 2018 Remi Collet <remi@remirepo.net> - 1.15.0~RC1-1
- Update to 1.15.0RC1

* Thu Aug 16 2018 Remi Collet <remi@remirepo.net> - 1.14.1-2
- rebuild for 7.3.0beta2 new ABI

* Fri Aug 10 2018 Remi Collet <remi@remirepo.net> - 1.14.1-1
- update to 1.14.1

* Wed Jul 18 2018 Remi Collet <remi@remirepo.net> - 1.13.0-2
- rebuld for 7.3.0alpha4 new ABI

* Tue Jul 10 2018 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0

* Wed Jun 27 2018 Remi Collet <remi@remirepo.net> - 1.13.0~RC3-1
- update to 1.13.0RC3

* Wed May 23 2018 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Tue Apr 17 2018 Remi Collet <remi@remirepo.net> - 1.11.0-1
- Update to 1.11.0

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 1.11.0~RC2-1
- Update to 1.11.0RC2

* Mon Apr  9 2018 Remi Collet <remi@remirepo.net> - 1.11.0~RC1-1
- Update to 1.11.0RC1

* Mon Apr  9 2018 Remi Collet <remi@remirepo.net> - 1.10.1-1
- Update to 1.10.1 (stable)

* Thu Mar 29 2018 Remi Collet <remi@remirepo.net> - 1.10.1~RC1-1
- Update to 1.10.1RC1

* Tue Mar 13 2018 Remi Collet <remi@remirepo.net> - 1.10.0-1
- Update to 1.10.0 (stable)

* Fri Mar  2 2018 Remi Collet <remi@remirepo.net> - 1.10.0~RC2-1
- Update to 1.10.0RC2

* Sun Feb  4 2018 Remi Collet <remi@remirepo.net> - 1.9.0-1
- Update to 1.9.0 (stable)

* Tue Jan 30 2018 Remi Collet <remi@remirepo.net> - 1.9.0~RC3-1
- Update to 1.9.0RC3

* Thu Jan 25 2018 Remi Collet <remi@remirepo.net> - 1.9.0~RC1-1
- Update to 1.9.0RC1

* Fri Jan 19 2018 Remi Collet <remi@remirepo.net> - 1.8.5-1
- Update to 1.8.5 (stable)

* Fri Jan  5 2018 Remi Collet <remi@remirepo.net> - 1.8.3-1
- Update to 1.8.3 (stable)

* Fri Dec 15 2017 Remi Collet <remi@remirepo.net> - 1.8.0-1
- Update to 1.8.0 (stable)

* Thu Nov 30 2017 Remi Collet <remi@remirepo.net> - 1.8.0~RC1-1
- Update to 1.8.0RC1

* Wed Nov 15 2017 Remi Collet <remi@remirepo.net> - 1.7.0-1
- Update to 1.7.0 (stable)

* Thu Oct 12 2017 Remi Collet <remi@remirepo.net> - 1.7.0~RC1-1
- Update to 1.7.0RC1

* Tue Sep 19 2017 Remi Collet <remi@remirepo.net> - 1.6.0-1
- Update to 1.6.0 (stable)

* Mon Sep  4 2017 Remi Collet <remi@remirepo.net> - 1.6.0~RC1-1
- Update to 1.6.0RC1
- License changed to Apache 2.0

* Tue Aug 22 2017 Remi Collet <remi@remirepo.net> - 1.4.6-2
- honour default RPM build options

* Thu Aug 17 2017 Remi Collet <remi@remirepo.net> - 1.4.6-1
- Update to 1.4.6 (stable)

* Wed Aug 16 2017 Remi Collet <remi@remirepo.net> - 1.4.6~RC6-1
- Update to 1.4.6RC6

* Tue Aug 15 2017 Remi Collet <remi@remirepo.net> - 1.4.6~RC5-1
- Update to 1.4.6RC5

* Tue Aug 15 2017 Remi Collet <remi@remirepo.net> - 1.4.6~RC4-1
- Update to 1.4.6RC4

* Tue Aug 15 2017 Remi Collet <remi@remirepo.net> - 1.4.6~RC2-1
- Update to 1.4.6RC2

* Wed Aug  9 2017 Remi Collet <remi@remirepo.net> - 1.4.4-1
- Update to 1.4.4

* Tue Aug  8 2017 Remi Collet <remi@remirepo.net> - 1.4.3-1
- Update to 1.4.3
- add patch for ZTS build
  from https://github.com/grpc/grpc/pull/12117

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 1.4.1-2
- rebuild for PHP 7.2.0beta1 new API

* Fri Jun 30 2017 Remi Collet <remi@remirepo.net> - 1.4.1-1
- Update to 1.4.1 (stable)

* Thu Jun 22 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0 (stable)

* Wed Jun 21 2017 Remi Collet <remi@remirepo.net> - 1.4.0~RC2-1
- rebuild for 7.2.0alpha2

* Fri Jun  2 2017 Remi Collet <remi@remirepo.net> - 1.4.0~RC2-1
- update to 1.4.0RC2 (no change)

* Thu Jun  1 2017 Remi Collet <remi@remirepo.net> - 1.4.0~RC1-1
- update to 1.4.0RC1

* Fri May 12 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2 (stable)

* Thu May 11 2017 Remi Collet <remi@remirepo.net> - 1.3.2~RC1-1
- update to 1.3.2RC1

* Sat May  6 2017 Remi Collet <remi@remirepo.net> - 1.3.1~RC1-1
- update to 1.3.1RC1

* Tue Apr 25 2017 Remi Collet <remi@remirepo.net> - 1.2.0-1
- initial package, version 1.2.0 (stable)
- open https://github.com/grpc/grpc/issues/10842 bad version
- open https://github.com/grpc/grpc/issues/10843 build fail with gcc 7
