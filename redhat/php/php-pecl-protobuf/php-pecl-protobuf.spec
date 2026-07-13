# remirepo spec file for php-pecl-protobuf
#
# SPDX-FileCopyrightText:  Copyright 2016-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%{?scl:%scl_package      php-pecl-protobuf}

%global pecl_name        protobuf
%global with_zts         0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name         40-%{pecl_name}.ini
%global library_version  35.1
%global upstream_version 5.%{library_version}
#global upstream_prever  rc2
%global sources          php/ext/google/protobuf
%global _configure       ../%{sources}/configure

# Github forge
%global gh_vend          protocolbuffers
%global gh_proj          protobuf
%global forgeurl         https://github.com/%{gh_vend}/%{gh_proj}
%global tag              v%{library_version}%{?upstream_prever:-%{upstream_prever}}
# for EL-8 to avoid TAG usage
%global archivename      %{gh_proj}-%{library_version}%{?upstream_prever:-%{upstream_prever}}

Name:          %{?scl_prefix}php-pecl-%{pecl_name}
Summary:       Mechanism for serializing structured data
# protobuf extension is BSD
# third_party/utf8_range is MIT
License:       BSD-3-Clause and MIT
Version:       %{upstream_version}%{?upstream_prever:~%{upstream_prever}}
Release:       1%{?dist}
%forgemeta
URL:           %{forgeurl}
Source0:       %{forgesource}

BuildRequires: make
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel >= 8.2

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

# Extension
Provides:      %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
# PECL
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:      %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
# No PIE for now


%description
Google's language-neutral, platform-neutral, extensible mechanism for
serializing structured data.

See: https://developers.google.com/protocol-buffers/

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%prep
%forgesetup
cp third_party/utf8_range/LICENSE LICENSE.utf8_range

pushd %{sources}
ln -s ../../../../third_party

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_PROTOBUF_VERSION/{s/.* "//;s/".*$//;p}' protobuf.h | tr '[:upper:]' '[:lower:]')
if test "x${extver}" != "x%{upstream_version}%{?upstream_prever}"; then
   : Error: Upstream extension version is ${extver}, expecting %{upstream_version}%{?upstream_prever}.
   exit 1
fi
popd

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif

# Drop in the bit of configuration
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; Configuration
;protobuf.keep_descriptor_pool_after_request = 0
EOF


%build
%{?dtsenable}

pushd %{sources}
%{__phpize}
sed -e 's/INSTALL_ROOT/DESTDIR/' -i build/Makefile.global
popd

cd NTS
%configure \
    --enable-protobuf  \
    --with-php-config=%{__phpconfig}

%make_build

%if %{with_zts}
cd ../ZTS
%configure \
    --enable-protobuf  \
    --with-php-config=%{__ztsphpconfig}

%make_build
%endif


%install
%{?dtsenable}

# Install the NTS stuff
%make_install -C NTS
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
%make_install -C ZTS
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%endif


%files
%license LICENSE*

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Fri Jun 12 2026 Remi Collet <remi@remirepo.net> - 5.35.1-1
- update to 5.35.1

* Wed May 20 2026 Remi Collet <remi@remirepo.net> - 5.35.0-1
- update to 5.35.0

* Thu May  7 2026 Remi Collet <remi@remirepo.net> - 5.35.0~rc2-1
- update to 5.35.0RC2

* Tue Apr 21 2026 Remi Collet <remi@remirepo.net> - 5.35.0~rc1-1
- update to 5.35.0RC1

* Fri Mar 20 2026 Remi Collet <remi@remirepo.net> - 5.34.1-1
- update to 5.34.1 (no change)
- drop pear/pecl dependency
- sources from github

* Fri Feb 27 2026 Remi Collet <remi@remirepo.net> - 5.34.0-1
- update to 5.34.0

* Fri Jan 23 2026 Remi Collet <remi@remirepo.net> - 5.34.0~RC1-1
- update to 5.34.0RC1
- raise dependency on PHP 8.2

* Tue Jan 13 2026 Remi Collet <remi@remirepo.net> - 4.33.4-1
- update to 4.33.4 (no change)

* Mon Jan 12 2026 Remi Collet <remi@remirepo.net> - 4.33.3-1
- update to 4.33.3

* Sat Dec  6 2025 Remi Collet <remi@remirepo.net> - 4.33.2-1
- update to 4.33.2

* Fri Nov 14 2025 Remi Collet <remi@remirepo.net> - 4.33.1-1
- update to 4.33.1 (no change)

* Thu Oct 16 2025 Remi Collet <remi@remirepo.net> - 4.33.0-1
- update to 4.33.0

* Fri Oct 10 2025 Remi Collet <remi@remirepo.net> - 4.33.0~RC2-1
- update to 4.33.0RC2 (no change)

* Thu Oct  2 2025 Remi Collet <remi@remirepo.net> - 4.33.0~RC1-1
- update to 4.33.0RC1

* Fri Sep 12 2025 Remi Collet <remi@remirepo.net> - 4.32.1-1
- update to 4.32.1 (no change)

* Sat Aug 16 2025 Remi Collet <remi@remirepo.net> - 4.32.0-1
- update to 4.32.0

* Wed Aug  6 2025 Remi Collet <remi@remirepo.net> - 4.32.0~RC2-1
- update to 4.32.0RC2

* Tue Jul 22 2025 Remi Collet <remi@remirepo.net> - 4.32.0~RC1-1
- update to 4.32.0RC1

* Thu May 29 2025 Remi Collet <remi@remirepo.net> - 4.31.1-1
- update to 4.31.1 (no change)

* Thu May 15 2025 Remi Collet <remi@remirepo.net> - 4.31.0-1
- update to 4.31.0

* Mon May  5 2025 Remi Collet <remi@remirepo.net> - 4.31.0~RC2-1
- update to 4.31.0RC2

* Tue Apr 22 2025 Remi Collet <remi@remirepo.net> - 4.31.0~RC1-1
- update to 4.31.0RC1

* Thu Mar 27 2025 Remi Collet <remi@remirepo.net> - 4.30.2-1
- update to 4.30.2 (no change)

* Fri Mar 14 2025 Remi Collet <remi@remirepo.net> - 4.30.1-1
- update to 4.30.1 (no change)

* Wed Mar  5 2025 Remi Collet <remi@remirepo.net> - 4.30.0-1
- update to 4.30.0

* Thu Feb 27 2025 Remi Collet <remi@remirepo.net> - 4.30.0~RC2-1
- update to 4.30.0RC2

* Wed Feb  5 2025 Remi Collet <remi@remirepo.net> - 4.30.0~RC1-1
- update to 4.30.0RC1

* Thu Jan  9 2025 Remi Collet <remi@remirepo.net> - 4.29.3-1
- update to 4.29.3 (no change)

* Wed Dec 18 2024 Remi Collet <remi@remirepo.net> - 4.29.2-1
- update to 4.29.2 (no change)
- re-license spec file to CECILL-2.1

* Thu Dec  5 2024 Remi Collet <remi@remirepo.net> - 4.29.1-1
- update to 4.29.1 (no change)

* Thu Nov 28 2024 Remi Collet <remi@remirepo.net> - 4.29.0-1
- update to 4.29.0

* Tue Nov 19 2024 Remi Collet <remi@remirepo.net> - 4.29.0~RC3-1
- update to 4.29.0RC3

* Thu Oct 24 2024 Remi Collet <remi@remirepo.net> - 4.29.0~RC2-1
- update to 4.29.0RC2 (no change)

* Tue Oct  1 2024 Remi Collet <remi@remirepo.net> - 4.29.0~RC1-1
- update to 4.29.0RC1

* Thu Sep 19 2024 Remi Collet <remi@remirepo.net> - 4.28.2-1
- update to 4.28.2 (no change)

* Thu Sep 12 2024 Remi Collet <remi@remirepo.net> - 4.28.1-1
- update to 4.28.1

* Thu Aug 29 2024 Remi Collet <remi@remirepo.net> - 4.28.0-1
- update to 4.28.0

* Mon Aug 26 2024 Remi Collet <remi@remirepo.net> - 4.28.0~RC3-1
- update to 4.28.0RC3 (no change)

* Fri Aug  9 2024 Remi Collet <remi@remirepo.net> - 4.28.0~RC2-1
- update to 4.28.0RC2 (no change)

* Fri Jul 12 2024 Remi Collet <remi@remirepo.net> - 4.28.0~RC1-1
- update to 4.28.0RC1

* Mon Jul  1 2024 Remi Collet <remi@remirepo.net> - 4.27.2-1
- update to 4.27.2

* Thu Jun  6 2024 Remi Collet <remi@remirepo.net> - 4.27.1-1
- update to 4.27.1 (no change)

* Fri May 24 2024 Remi Collet <remi@remirepo.net> - 4.27.0-1
- update to 4.27.0

* Wed May 15 2024 Remi Collet <remi@remirepo.net> - 4.27.0~RC3-1
- update to 4.27.0RC3

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 4.27.0~RC2-1
- update to 4.27.0RC2 (no change)

* Fri Apr 19 2024 Remi Collet <remi@remirepo.net> - 4.27.0~RC1-1
- update to 4.27.0RC1

* Thu Mar 28 2024 Remi Collet <remi@remirepo.net> - 4.26.1-1
- update to 4.26.1 (no change)

* Thu Mar 14 2024 Remi Collet <remi@remirepo.net> - 4.26.0-1
- update to 4.26.0

* Thu Feb 29 2024 Remi Collet <remi@remirepo.net> - 4.26.0~RC3-1
- update to 4.26.0RC3

* Wed Feb  7 2024 Remi Collet <remi@remirepo.net> - 4.26.0~RC2-1
- update to 4.26.0RC2

* Tue Jan 30 2024 Remi Collet <remi@remirepo.net> - 4.26.0~RC1-1
- update to 4.26.0RC1

* Wed Jan 10 2024 Remi Collet <remi@remirepo.net> - 3.25.2-1
- update to 3.25.2 (no change)

* Thu Nov 16 2023 Remi Collet <remi@remirepo.net> - 3.25.1-1
- update to 3.25.1 (no change)

* Thu Nov  2 2023 Remi Collet <remi@remirepo.net> - 3.25.0-1
- update to 3.25.0

* Thu Oct 19 2023 Remi Collet <remi@remirepo.net> - 3.25.0~RC2-1
- update to 3.25.0RC2 (no change)

* Tue Oct 17 2023 Remi Collet <remi@remirepo.net> - 3.25.0~RC1-1
- update to 3.25.0RC1
- open https://github.com/protocolbuffers/protobuf/issues/14436
  build broken with PHP 7.x
- raise dependency on PHP 8.0

* Thu Oct  5 2023 Remi Collet <remi@remirepo.net> - 3.24.4-1
- update to 3.24.4 (no change)

* Fri Sep  8 2023 Remi Collet <remi@remirepo.net> - 3.24.3-1
- update to 3.24.3 (no change)

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 3.24.2-2
- rebuild for PHP 8.3.0RC1

* Mon Aug 28 2023 Remi Collet <remi@remirepo.net> - 3.24.2-1
- update to 3.24.2 (no change)

* Sat Aug 19 2023 Remi Collet <remi@remirepo.net> - 3.24.1-1
- update to 3.24.1 (no change)

* Thu Aug 17 2023 Remi Collet <remi@remirepo.net> - 3.24.0-1
- update to 3.24.0

* Wed Aug  2 2023 Remi Collet <remi@remirepo.net> - 3.24.0~RC3-1
- update to 3.24.0RC3 (no change)

* Wed Jul 19 2023 Remi Collet <remi@remirepo.net> - 3.24.0~RC2-1
- update to 3.24.0RC2

* Mon Jul 17 2023 Remi Collet <remi@remirepo.net> - 3.24.0~RC1-2
- enable ZTS build

* Wed Jul 12 2023 Remi Collet <remi@remirepo.net> - 3.24.0~RC1-1
- update to 3.24.0RC1

* Fri Jul  7 2023 Remi Collet <remi@remirepo.net> - 3.23.4-1
- update to 3.23.4 (no change)

* Thu Jun 15 2023 Remi Collet <remi@remirepo.net> - 3.23.3-1
- update to 3.23.3

* Sun May 28 2023 Remi Collet <remi@remirepo.net> - 3.23.2-1
- update to 3.23.2 (no change)
- build out of sources tree

* Fri May 19 2023 Remi Collet <remi@remirepo.net> - 3.23.1-1
- update to 3.23.1 (no change)

* Tue May  9 2023 Remi Collet <remi@remirepo.net> - 3.23.0-1
- update to 3.23.0

* Fri May  5 2023 Remi Collet <remi@remirepo.net> - 3.22.4-1
- update to 3.22.4 (no change)

* Tue May  2 2023 Remi Collet <remi@remirepo.net> - 3.23.0~RC2-1
- update to 3.23.0RC2

* Thu Apr 13 2023 Remi Collet <remi@remirepo.net> - 3.22.3-1
- update to 3.22.3 (no change)

* Wed Mar  8 2023 Remi Collet <remi@remirepo.net> - 3.22.1-1
- update to 3.22.1

* Fri Feb 17 2023 Remi Collet <remi@remirepo.net> - 3.22.0-1
- update to 3.22.0

* Mon Feb 13 2023 Remi Collet <remi@remirepo.net> - 3.22.0~RC3-1
- update to 3.22.0RC3

* Fri Feb  3 2023 Remi Collet <remi@remirepo.net> - 3.22.0~RC2-1
- update to 3.22.0RC2

* Tue Jan 31 2023 Remi Collet <remi@remirepo.net> - 3.22.0~RC1-1
- update to 3.22.0RC1

* Wed Dec 14 2022 Remi Collet <remi@remirepo.net> - 3.21.12-1
- update to 3.21.12

* Thu Dec  8 2022 Remi Collet <remi@remirepo.net> - 3.21.11-1
- update to 3.21.11

* Thu Dec  1 2022 Remi Collet <remi@remirepo.net> - 3.21.10-1
- update to 3.21.10

* Thu Oct 27 2022 Remi Collet <remi@remirepo.net> - 3.21.9-1
- update to 3.21.9 (no change)

* Wed Oct 19 2022 Remi Collet <remi@remirepo.net> - 3.21.8-1
- update to 3.21.8 (no change)

* Fri Sep 30 2022 Remi Collet <remi@remirepo.net> - 3.21.7-1
- update to 3.21.7 (no change)

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 3.21.6-1
- update to 3.21.6 (no change)

* Wed Aug 10 2022 Remi Collet <remi@remirepo.net> - 3.21.5-1
- update to 3.21.5

* Tue Jul 26 2022 Remi Collet <remi@remirepo.net> - 3.21.4-1
- update to 3.21.4 (no change)

* Fri Jul 22 2022 Remi Collet <remi@remirepo.net> - 3.21.3-1
- update to 3.21.3

* Mon Jun 27 2022 Remi Collet <remi@remirepo.net> - 3.21.2-1
- update to 3.21.2 (no change)

* Sat May 28 2022 Remi Collet <remi@remirepo.net> - 3.21.1-1
- update to 3.21.1 (no change)

* Thu May 26 2022 Remi Collet <remi@remirepo.net> - 3.21.0-1
- update to 3.21.0

* Mon May 23 2022 Remi Collet <remi@remirepo.net> - 3.21.0~RC2-1
- update to 3.21.0RC2

* Thu May 12 2022 Remi Collet <remi@remirepo.net> - 3.21.0~RC1-1
- update to 3.21.0RC1

* Mon Apr 25 2022 Remi Collet <remi@remirepo.net> - 3.20.1-1
- update to 3.20.1

* Thu Apr  7 2022 Remi Collet <remi@remirepo.net> - 3.20.1~RC1-1
- update to 3.20.1RC1

* Sun Apr  3 2022 Remi Collet <remi@remirepo.net> - 3.20.0-1
- update to 3.20.0
- add MIT License

* Mon Mar 21 2022 Remi Collet <remi@remirepo.net> - 3.20.0~RC2-1
- update to 3.20.0RC2

* Mon Mar  7 2022 Remi Collet <remi@remirepo.net> - 3.20.0~RC1-1
- update to 3.20.0RC1

* Mon Jan 31 2022 Remi Collet <remi@remirepo.net> - 3.19.4-1
- update to 3.19.4

* Wed Jan 12 2022 Remi Collet <remi@remirepo.net> - 3.19.3-1
- update to 3.19.3 (no change)

* Thu Jan  6 2022 Remi Collet <remi@remirepo.net> - 3.19.2-1
- update to 3.19.2 (no change)

* Fri Oct 29 2021 Remi Collet <remi@remirepo.net> - 3.19.1-1
- update to 3.19.1 (no change)

* Thu Oct 21 2021 Remi Collet <remi@remirepo.net> - 3.19.0-1
- update to 3.19.0

* Wed Oct 20 2021 Remi Collet <remi@remirepo.net> - 3.19.0~RC2-1
- update to 3.19.0RC2

* Mon Oct 18 2021 Remi Collet <remi@remirepo.net> - 3.19.0~RC1-1
- update to 3.19.0RC1

* Wed Oct  6 2021 Remi Collet <remi@remirepo.net> - 3.18.1-1
- update to 3.18.1

* Sat Sep 18 2021 Remi Collet <remi@remirepo.net> - 3.18.0-1
- update to 3.18.0

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 3.17.3-2
- rebuild for 8.1.0RC1

* Tue Jun  8 2021 Remi Collet <remi@remirepo.net> - 3.17.3-1
- update to 3.17.3
- add patch for PHP 8.1 from
  https://github.com/protocolbuffers/protobuf/pull/8710

* Thu Jun  3 2021 Remi Collet <remi@remirepo.net> - 3.17.2-1
- update to 3.17.2 (no change)

* Tue May 25 2021 Remi Collet <remi@remirepo.net> - 3.17.1-1
- update to 3.17.1

* Thu May 13 2021 Remi Collet <remi@remirepo.net> - 3.17.0-1
- update to 3.17.0 (no change)

* Wed May 12 2021 Remi Collet <remi@remirepo.net> - 3.17.0~RC2-1
- update to 3.17.0RC2 (no change)

* Fri May  7 2021 Remi Collet <remi@remirepo.net> - 3.16.0-1
- update to 3.16.0 (no change)

* Thu May  6 2021 Remi Collet <remi@remirepo.net> - 3.16.0~RC2-1
- update to 3.16.0RC2 (no change)

* Wed Apr  7 2021 Remi Collet <remi@remirepo.net> - 3.16.0~RC1-1
- update to 3.16.0RC1 (no change)

* Sat Apr  3 2021 Remi Collet <remi@remirepo.net> - 3.15.7-1
- update to 3.15.7 (no change)

* Fri Mar 12 2021 Remi Collet <remi@remirepo.net> - 3.15.6-1
- update to 3.15.6 (no change)

* Fri Mar  5 2021 Remi Collet <remi@remirepo.net> - 3.15.5-1
- update to 3.15.5

* Thu Mar  4 2021 Remi Collet <remi@remirepo.net> - 3.15.4-1
- update to 3.15.4

* Fri Feb 26 2021 Remi Collet <remi@remirepo.net> - 3.15.3-1
- update to 3.15.3 (no change)

* Wed Feb 24 2021 Remi Collet <remi@remirepo.net> - 3.15.2-1
- update to 3.15.2 (no change)

* Sat Feb 20 2021 Remi Collet <remi@remirepo.net> - 3.15.1-1
- update to 3.15.1 (no change)

* Fri Feb 19 2021 Remi Collet <remi@remirepo.net> - 3.15.0-1
- update to 3.15.0

* Wed Feb 10 2021 Remi Collet <remi@remirepo.net> - 3.15.0~RC1-1
- update to 3.15.0RC1

* Sat Nov 14 2020 Remi Collet <remi@remirepo.net> - 3.14.0-1
- update to 3.14.0

* Fri Nov 13 2020 Remi Collet <remi@remirepo.net> - 3.14.0~RC3-1
- update to 3.14.0RC3 (no change)

* Wed Nov 11 2020 Remi Collet <remi@remirepo.net> - 3.14.0~RC2-1
- update to 3.14.0RC2

* Mon Nov  9 2020 Remi Collet <remi@remirepo.net> - 3.14.0~RC1-1
- update to 3.14.0RC1
- open https://github.com/protocolbuffers/protobuf/issues/8016
  missing files in pecl package
- open https://github.com/protocolbuffers/protobuf/issues/8017
  bad version reported
- open https://github.com/protocolbuffers/protobuf/issues/8019
  strange changes

* Fri Oct  9 2020 Remi Collet <remi@remirepo.net> - 3.13.0.1-1
- update to 3.13.0.1

* Sat Aug 15 2020 Remi Collet <remi@remirepo.net> - 3.13.0-1
- update to 3.13.0
- raise dependency on PHP 7
- open https://github.com/protocolbuffers/protobuf/issues/7812

* Wed Jul 29 2020 Remi Collet <remi@remirepo.net> - 3.12.4-1
- update to 3.12.4 (no change)

* Thu Jul 16 2020 Remi Collet <remi@remirepo.net> - 3.12.3-1
- update to 3.12.3 (no change)

* Thu May 28 2020 Remi Collet <remi@remirepo.net> - 3.12.2-1
- update to 3.12.2 (no change)

* Thu May 21 2020 Remi Collet <remi@remirepo.net> - 3.12.1-1
- update to 3.12.1

* Mon May 18 2020 Remi Collet <remi@remirepo.net> - 3.12.0-1
- update to 3.12.0

* Wed May 13 2020 Remi Collet <remi@remirepo.net> - 3.12.0~RC2-1
- update to 3.12.0RC1

* Tue May  5 2020 Remi Collet <remi@remirepo.net> - 3.12.0~RC1-1
- update to 3.12.0RC1

* Sat Feb 15 2020 Remi Collet <remi@remirepo.net> - 3.11.4-1
- update to 3.11.4

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 3.11.3-1
- update to 3.11.3

* Sat Dec 14 2019 Remi Collet <remi@remirepo.net> - 3.11.2-1
- update to 3.11.2

* Tue Dec  3 2019 Remi Collet <remi@remirepo.net> - 3.11.1-1
- update to 3.11.1
- add patches for PHP 7.4 from
  https://github.com/protocolbuffers/protobuf/pull/6968

* Tue Nov 26 2019 Remi Collet <remi@remirepo.net> - 3.11.0-1
- update to 3.11.0

* Sat Nov 23 2019 Remi Collet <remi@remirepo.net> - 3.11.0~RC2-1
- update to 3.11.0RC2

* Thu Nov 21 2019 Remi Collet <remi@remirepo.net> - 3.11.0~RC1-1
- update to 3.11.0RC1
  https://github.com/protocolbuffers/protobuf/issues/6918

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 3.10.0-1
- update to 3.10.0

* Fri Sep  6 2019 Remi Collet <remi@remirepo.net> - 3.10.0~RC1-1
- update to 3.10.0RC1
- see https://github.com/protocolbuffers/protobuf/issues/6624
  broken extension with 7.4.0RC1

* Wed Aug  7 2019 Remi Collet <remi@remirepo.net> - 3.9.1-1
- update to 3.9.1 (no change)

* Fri Jul 12 2019 Remi Collet <remi@remirepo.net> - 3.9.0-1
- update to 3.9.0

* Thu Jun 27 2019 Remi Collet <remi@remirepo.net> - 3.9.0~RC1-1
- update to 3.9.0RC1

* Wed May 29 2019 Remi Collet <remi@remirepo.net> - 3.8.0-1
- update to 3.8.0
- open https://github.com/protocolbuffers/protobuf/issues/6180
  PHP 7.4 support

* Tue May  7 2019 Remi Collet <remi@remirepo.net> - 3.8.0~RC1-1
- update to 3.8.0RC1
- open https://github.com/protocolbuffers/protobuf/issues/6108
  missing file in pecl archive

* Wed Mar 27 2019 Remi Collet <remi@remirepo.net> - 3.7.1-1
- update to 3.7.1

* Fri Mar  1 2019 Remi Collet <remi@remirepo.net> - 3.7.0-1
- update to 3.7.0 (GA)

* Tue Feb 26 2019 Remi Collet <remi@remirepo.net> - 3.7.0~RC3-1
- update to 3.7.0RC3

* Mon Feb  4 2019 Remi Collet <remi@remirepo.net> - 3.7.0~RC2-1
- update to 3.7.0RC2
- open https://github.com/protocolbuffers/protobuf/issues/5672
  please clarify stability state

* Sat Aug 11 2018 Remi Collet <remi@remirepo.net> - 3.6.1-1
- update to 3.6.1
- drop patch merged upstream

* Wed Jul 18 2018 Remi Collet <remi@remirepo.net> - 3.6.0-3
- rebuild for 7.3.0alpha4 new ABI

* Fri Jul  6 2018 Remi Collet <remi@remirepo.net> - 3.6.0-2
- add patch for PHP 7.3 from
  https://github.com/google/protobuf/pull/4873

* Thu Jun  7 2018 Remi Collet <remi@remirepo.net> - 3.6.0-1
- update to 3.6.0

* Mon Jan  8 2018 Remi Collet <remi@remirepo.net> - 3.5.1.1-1
- Update to 3.5.1.1

* Thu Dec 21 2017 Remi Collet <remi@remirepo.net> - 3.5.1-1
- Update to 3.5.1

* Thu Dec 14 2017 Remi Collet <remi@remirepo.net> - 3.5.0.1-1
- add upstream patch to drop timelib_update_ts need

* Thu Dec  7 2017 Remi Collet <remi@remirepo.net> - 3.5.0.1-1
- Update to 3.5.0.1 (still broken)

* Tue Nov 21 2017 Remi Collet <remi@remirepo.net> - 3.5.0-1
- Update to 3.5.0
- open https://github.com/google/protobuf/issues/3929
  undefined symbol timelib_update_ts

* Thu Aug 17 2017 Remi Collet <remi@remirepo.net> - 3.4.0-1
- Update to 3.4.0

* Tue Jul 18 2017 Remi Collet <remi@remirepo.net> - 3.3.2-2
- rebuild for PHP 7.2.0beta1 new API

* Fri Jun 23 2017 Remi Collet <remi@remirepo.net> - 3.3.2-1
- Update to 3.3.2

* Fri May  5 2017 Remi Collet <remi@fedoraproject.org> - 3.3.0-1
- update to 3.3.0
- open https://github.com/google/protobuf/issues/3058 - PHP 7.1

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 3.1.0-0.1.a1
- initial package, version 3.1.0a1 (alpha)
- open https://github.com/google/protobuf/issues/2185 - License
- open https://github.com/google/protobuf/issues/2185 - ZTS build
- open https://github.com/google/protobuf/issues/2185 - PHP 7

