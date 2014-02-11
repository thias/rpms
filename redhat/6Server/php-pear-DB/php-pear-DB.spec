%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name DB

# run rpmbuild --with sqlite if sqlite extension available
%global with_sqlite %{?_with_sqlite:1}%{!?_with_sqlite:0}

Name:           php-pear-DB
Version:        1.7.14
Release:        8%{?dist}
Summary:        PEAR: Database Abstraction Layer

Group:          Development/Libraries
License:        PHP
URL:            http://pear.php.net/package/DB
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog

# E_ALL include E_STRICT in PHP 5.4
# See https://pear.php.net/bugs/19544
Patch0:         %{pear_name}-tests.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear
%if %{with_sqlite}
BuildRequires:  php-sqlite
%endif
# for xml2changelog
BuildRequires:  php-simplexml

Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}
Requires:       php-pear(PEAR)

%description
DB is a database abstraction layer providing:
* an OO-style query API
* portability features that make programs written for one DBMS work with
  other DBMS's
* a DSN (data source name) format for specifying database servers
* prepare/execute (bind) emulation for databases that don't support it natively
* a result object for each query response
* portable error codes
* sequence emulation
* sequential and non-sequential row fetching as well as bulk fetching
* formats fetched rows as associative arrays, ordered arrays or objects
* row limit support
* transactions support
* table information interface
* DocBook and phpDocumentor API documentation

DB layers itself on top of PHP's existing database extensions.

%prep
%setup -q -c
%{_bindir}/php %{SOURCE2} package.xml >CHANGELOG

cd %{pear_name}-%{version}
# Package is V2
mv ../package.xml %{name}.xml

%patch0 -p1 -b .testfix

# update run test suite
sed -e 's@^ *DB_TEST_RUN_TESTS=.*$@[ -d /usr/lib64 ] \&\& DB_TEST_RUN_TESTS=/usr/lib64/php/build/run-tests.php || DB_TEST_RUN_TESTS=/usr/lib/php/build/run-tests.php@' \
    -e 's@^ *DB_TEST_DIR=.*$@DB_TEST_DIR=%{pear_testdir}/DB/tests@' \
    -e 's@^ *TEST_PHP_EXECUTABLE=.*$@TEST_PHP_EXECUTABLE=%{_bindir}/php@' \
    tests/run.cvs >tests/run

sed -e 's@^ *DB_TEST_RUN_TESTS=.*$@[ -d /usr/lib64 ] \&\& DB_TEST_RUN_TESTS=/usr/lib64/php/build/run-tests.php || DB_TEST_RUN_TESTS=/usr/lib/php/build/run-tests.php@' \
    -e 's@^ *DB_TEST_DIR=.*$@DB_TEST_DIR=%{pear_testdir}/DB/tests/driver@' \
    -e 's@^ *TEST_PHP_EXECUTABLE=.*$@TEST_PHP_EXECUTABLE=%{_bindir}/php@' \
    tests/driver/run.cvs >tests/driver/run


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

# Install new test suite
install -pm 755 tests/run $RPM_BUILD_ROOT%{pear_testdir}/DB/tests/
install -pm 755 tests/driver/run $RPM_BUILD_ROOT%{pear_testdir}/DB/tests/driver/

mv $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/doc/TESTERS .
iconv -f ISO-8859-1 -t UTF-8  TESTERS \
   -o $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/doc/TESTERS
touch -r TESTERS $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/doc/TESTERS


%clean
rm -rf $RPM_BUILD_ROOT


%check
top=$PWD
cd %{pear_name}-%{version}/tests
%{__pear} \
   run-tests \
   -i "-d include_path=%{buildroot}%{pear_phpdir}:%{pear_phpdir}" \
   . | tee $top/tests.log

cd driver
%if %{with_sqlite}
%{__pear} \
   run-tests \
   -i "-d include_path=%{buildroot}%{pear_phpdir}:%{pear_phpdir}" \
   . | tee -a $top/tests.log
%else
echo "Driver test skipped (need sqlite extension)"
%endif

grep "FAILED TESTS" $top/tests.log && exit 1


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/DB*
%{pear_testdir}/DB
%exclude %{pear_testdir}/DB/tests/run.cvs
%exclude %{pear_testdir}/DB/tests/driver/*.cvs


%changelog
* Mon Aug  5 2013 Remi Collet <remi@fedoraproject.org> - 1.7.14-8
- xml2changelog need simplexml

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 1.7.14-6
- fix metadata location, FTBFS #914358

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.7.14-4
- rebuilt for new pear_testdir

* Sat Aug 04 2012 Remi Collet <remi@fedoraproject.org> 1.7.14-3
- disable E_STRICT in tests, fix FTBFS

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 27 2011 Remi Collet <remi@fedoraproject.org> 1.7.14-1
- update to 1.7.14

* Wed Apr 13 2011 Remi Collet <Fedora@FamilleCollet.com> 1.7.13-5
- doc in /usr/share/doc/pear
- define timezone during build
- rename DB.xml to php-pear-DB.xml
- fix libdir in provided tests (%%{_libdir} have no value for noarch package)
- run tests in %%check (no driver as no sqlite extension)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 21 2007 Remi Collet <Fedora@FamilleCollet.com> 1.7.13-1
- update to 1.7.13
- fix TEXTERS encoding

* Thu Aug 23 2007 Remi Collet <Fedora@FamilleCollet.com> 1.7.12-2
- Fix License

* Mon Jul 23 2007 Remi Collet <Fedora@FamilleCollet.com> 1.7.12-1
- update to 1.7.12
- change requires from php to php-common
- update test suite to run (but only after install)
- add %%check, only for documentation purpose

* Mon Apr 30 2007 Remi Collet <Fedora@FamilleCollet.com> 1.7.11-1
- update to 1.7.11
- add generated CHANGELOG

* Sun Sep 10 2006 Tim Jackson <rpm@timj.co.uk> 1.7.6-7
- Update spec to new conventions (#198706)

* Wed Jun 28 2006 Tim Jackson <rpm@timj.co.uk> 1.7.6-6
- Move tests to peardir/test instead of peardir/tests (bug #196764)

* Wed May 17 2006 Tim Jackson <rpm@timj.co.uk> 1.7.6-5
- Moved package XML file to %%{peardir}/.pkgxml (see bug #190252)
- Abstracted package XML directory
- Removed some "-f"s on rm's to avoid masking possible errors

* Tue Jan 24 2006 Tim Jackson <rpm@timj.co.uk> 1.7.6-4
- Move package XML file to _libdir/php/pear rather than _var/lib/pear

* Tue Jan 24 2006 Tim Jackson <rpm@timj.co.uk> 1.7.6-3
- Requires(post,postun) php-pear

* Sat Dec 31 2005 Tim Jackson <rpm@timj.co.uk> 1.7.6-2
- Rearranged so it makes more sense
- Remove external license file
- peardir definition now comes from "pear config-get"
- BR php-pear
- shorten description
- be explicit about the files in the package
- use macro for /var
- remove versioning from pear(PEAR) dep; 1.0b1 is very old

* Sat Dec 31 2005 Tim Jackson <rpm@timj.co.uk> 1.7.6-1
- First RPM build
