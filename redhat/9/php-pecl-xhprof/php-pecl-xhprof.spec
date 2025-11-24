# remirepo spec file for php-pecl-xhprof
# with SCL compatibility
#
# Fedora spec file for php-pecl-xhprof
#
# Copyright (c) 2012-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%bcond_without     tests

%if 0%{?scl:1}
%scl_package             php-pecl-xhprof
%else
%global _root_bindir     %{_bindir}
%global _root_sysconfdir %{_sysconfdir}
%endif

%global pecl_name  xhprof
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name   40-%{pecl_name}.ini
%global sources    %{pecl_name}-%{version}
%global _configure ../extension/configure

Name:           %{?scl_prefix}php-pecl-xhprof
Version:        2.3.10
Release:        1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}

Summary:        PHP extension for XHProf, a Hierarchical Profiler
License:        Apache-2.0
URL:            https://pecl.php.net/package/%{pecl_name}
Source0:        https://pecl.php.net/get/%{sources}.tgz

# https://bugs.php.net/61262
ExclusiveArch:  %{ix86} x86_64 aarch64

BuildRequires:  make
BuildRequires:  %{?dtsprefix}gcc
BuildRequires:  %{?scl_prefix}php-devel >= 7.0
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}


%description
XHProf is a function-level hierarchical profiler for PHP.

This package provides the raw data collection component,
implemented in C (as a PHP extension).

The HTML based navigational interface is provided in the "xhprof" package.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package -n %{?scl_prefix}xhprof
Summary:       A Hierarchical Profiler for PHP - Web interface
Group:         Development/Tools
BuildArch:     noarch

Requires:      %{name} = %{version}-%{release}
Requires:      %{_root_bindir}/dot

%description -n %{?scl_prefix}xhprof
XHProf is a function-level hierarchical profiler for PHP and has a simple HTML
based navigational interface.

The raw data collection component, implemented in C (as a PHP extension,
provided by the "php-pecl-xhprof" package).

The reporting/UI layer is all in PHP. It is capable of reporting function-level
inclusive and exclusive wall times, memory usage, CPU times and number of calls
for each function.

Additionally, it supports ability to compare two runs (hierarchical DIFF
reports), or aggregate results from multiple runs.

Documentation: %{pecl_docdir}/%{pecl_name}/xhprof_html/docs/index.html


%prep
%setup -c -q

# Mark "php" files as "src" to avoid registration in pear file list
# xhprof_html should be web, but www_dir is /var/www/html
# xhprof_lib  should be php, really a lib
sed -e 's/role="php"/role="src"/' \
    -e '/LICENSE/s/role="doc"/role="src"/' \
    -i package.xml

pushd %{sources}/extension
# sed -e '/XHPROF_VERSION/s/2.3.5/%{version}/' -i php_xhprof.h
# Sanity check, really often broken
extver=$(sed -n '/#define XHPROF_VERSION/{s/.* "//;s/".*$//;p}' php_xhprof.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
popd

# Extension configuration file
cat >%{ini_name} <<EOF
; Enable %{pecl_name} extension module
extension = xhprof.so

; You can either pass the directory location as an argument to the constructor
; for XHProfRuns_Default() or set xhprof.output_dir ini param.
;xhprof.output_dir = ''
;xhprof.collect_additional_info = 0
;xhprof.sampling_interval = 100000
;xhprof.sampling_depth = 0x7fffffff
EOF

# Apache configuration file
cat >httpd.conf <<EOF
Alias /xhprof %{_datadir}/xhprof/xhprof_html

<Directory %{_datadir}/xhprof/xhprof_html>
   # For security reason, the web interface
   # is only allowed from the server

   Require local
</Directory>
EOF

cd %{sources}
chmod -x extension/*.{c,h}

mkdir NTS
%if %{with_zts}
mkdir ZTS
%endif


%build
%{?dtsenable}

cd %{sources}/extension
%{__phpize}

cd ../NTS
%configure \
    --with-php-config=%{__phpconfig}
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%configure \
    --with-php-config=%{__ztsphpconfig}
make %{?_smp_mflags}
%endif


%install
%{?dtsenable}

make install -C %{sources}/NTS  INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make install -C %{sources}/ZTS    INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Install the Apache configuration
install -D -m 644 httpd.conf %{buildroot}%{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}xhprof.conf

# Install the web interface
mkdir -p %{buildroot}%{_datadir}/xhprof
cp -pr %{sources}/xhprof_html %{buildroot}%{_datadir}/xhprof/xhprof_html
cp -pr %{sources}/xhprof_lib  %{buildroot}%{_datadir}/xhprof/xhprof_lib
rm -r %{buildroot}%{_datadir}/xhprof/xhprof_html/docs

# Test & Documentation
cd %{sources}
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: simple module load TEST for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'

%if %{with tests}
cd %{sources}/extension
: Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php -q --show-diff
%endif

%if %{with_zts}
: simple module load TEST for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep '^%{pecl_name}$'
%endif


%files
%license %{sources}/LICENSE
%doc %{pecl_docdir}/%{pecl_name}
%exclude %{pecl_docdir}/%{pecl_name}/examples
%exclude %{pecl_docdir}/%{pecl_name}/xhprof_html
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files -n %{?scl_prefix}xhprof
%doc %{pecl_docdir}/%{pecl_name}/examples
%doc %{pecl_docdir}/%{pecl_name}/xhprof_html
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{_root_sysconfdir}/httpd/conf.d/%{?scl_prefix}xhprof.conf
%{_datadir}/xhprof


%changelog
* Thu Jul 11 2024 Remi Collet <remi@remirepo.net> - 2.3.10-1
- update to 2.3.10
- drop patch merged upstream

* Fri Jul  5 2024 Remi Collet <remi@remirepo.net> - 2.3.9-4
- fix build with 8.4 using patch from
  https://github.com/longxinH/xhprof/pull/87

* Wed Aug 30 2023 Remi Collet <remi@remirepo.net> - 2.3.9-3
- rebuild for PHP 8.3.0RC1

* Wed Jul 19 2023 Remi Collet <remi@remirepo.net> - 2.3.9-2
- build out of sources tree

* Wed Dec 14 2022 Remi Collet <remi@remirepo.net> - 2.3.9-1
- update to 2.3.9
- use SPDX license id

* Mon Nov  7 2022 Remi Collet <remi@remirepo.net> - 2.3.8-1
- update to 2.3.8

* Tue Sep  6 2022 Remi Collet <remi@remirepo.net> - 2.3.7-1
- update to 2.3.7 (no change)

* Mon Sep  5 2022 Remi Collet <remi@remirepo.net> - 2.3.6-1
- update to 2.3.6

* Sun Sep  5 2021 Remi Collet <remi@remirepo.net> - 2.3.5-1
- update to 2.3.5

* Wed Sep 01 2021 Remi Collet <remi@remirepo.net> - 2.3.4-2
- rebuild for 8.1.0RC1

* Wed Aug  4 2021 Remi Collet <remi@remirepo.net> - 2.3.4-1
- update to 2.3.4
- drop patch merged upstream

* Mon Jul  5 2021 Remi Collet <remi@remirepo.net> - 2.3.3-1
- update to 2.3.3
- add patch for PHP 8.1 from
  https://github.com/longxinH/xhprof/pull/61

* Fri May  7 2021 Remi Collet <remi@remirepo.net> - 2.3.2-1
- update to 2.3.2 (stable)

* Sat May  1 2021 Remi Collet <remi@remirepo.net> - 2.3.1-1
- update to 2.3.1 (beta)

* Thu Apr  1 2021 Remi Collet <remi@remirepo.net> - 2.3.0-1
- update to 2.3.0 (beta)

* Fri Nov 27 2020 Remi Collet <remi@remirepo.net> - 2.2.3-1
- update to 2.2.3 (stable)

* Fri Oct  9 2020 Remi Collet <remi@remirepo.net> - 2.2.2-1
- update to 2.2.2 (beta)

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 2.2.1-2
- rebuild for PHP 8.0.0RC1

* Sat Sep 19 2020 Remi Collet <remi@remirepo.net> - 2.2.1-1
- update to 2.2.1 (beta)
- enable upstream test suite

* Sat Apr 11 2020 Remi Collet <remi@remirepo.net> - 2.2.0-1
- update to 2.2.0

* Tue Dec 17 2019 Remi Collet <remi@remirepo.net> - 2.1.4-1
- update to 2.1.4

* Wed Dec 11 2019 Remi Collet <remi@remirepo.net> - 2.1.3-1
- update to 2.1.3

* Fri Dec  6 2019 Remi Collet <remi@remirepo.net> - 2.1.2-1
- update to 2.1.2
- raise dependency on PHP 7

* Mon Jan 21 2019 Remi Collet <remi@remirepo.net> - 0.9.4-8
- cleanup for EL-8

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> - 0.9.4-7
- adapt for F24

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> - 0.9.4-6
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-5.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 0.9.4-5
- improve SCL build

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-4
- add numerical prefix to extension configuration file (php 5.6)

* Wed Mar 19 2014 Remi Collet <rcollet@redhat.com> - 0.9.4-3
- allow SCL build

* Sat Mar 15 2014 Remi Collet <remi@fedoraproject.org> - 0.9.4-2
- install doc in pecl_docdir
- install test in pecl_testdir

* Tue Oct  1 2013 Remi Collet <remi@fedoraproject.org> - 0.9.4-1
- update to 0.9.4

* Tue Aug 6 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-3
- fix doc path in package description #994038

* Mon May 20 2013 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- update to 0.9.3

* Fri Jan  4 2013 Remi Collet <remi@fedoraproject.org> - 0.9.2-8.gitb8c76ac5ab
- git snapshot + php 5.5 fix
  https://github.com/facebook/xhprof/pull/15
- also provides php-xhprof
- cleanups

* Tue May 22 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-6
- move from ExcludeArch: ppc64
  to ExclusiveArch: %%{ix86} x86_64 because of cycle_timer()

* Sun May 06 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-5
- make configuration file compatible with apache 2.2 / 2.4

* Mon Mar 05 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-4
- rename patches
- install html and lib under /usr/share/xhprof

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 0.9.2-3
- prepare for review
- make ZTS build conditionnal (for PHP 5.3)
- add xhprof.output_dir in configuration file
- open https://bugs.php.net/61262 for ppc64

* Thu Mar 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-2
- split web interace in xhprof sub-package

* Thu Mar 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.9.2-1
- Initial RPM package

