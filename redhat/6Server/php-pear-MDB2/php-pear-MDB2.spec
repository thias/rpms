%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name MDB2
%global prever    b5

Name:           php-pear-MDB2
Version:        2.5.0
%if 0%{?prever:1}
Release:        0.10.%{?prever}%{?dist}
%else
Release:        6%{?dist}
%endif
Summary:        Database Abstraction Layer

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/MDB2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1

Requires:       php-common >= 5.2.0
Requires:       php-pear(PEAR) >= 1.9.1
# phpci detected required extension
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{pear_name}) = %{version}%{?prever}


%description
PEAR::MDB2 is a merge of the PEAR::DB and Metabase php database abstraction
layers.

It provides a common API for all supported RDBMS. The main difference to most
other DB abstraction packages is that MDB2 goes much further to ensure
portability.


%prep
%setup -qc
cd %{pear_name}-%{version}%{?prever}
# package.xml is V2
sed -e '/LICENSE/s/role="data"/role="doc"/' <../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null ||:

%postun
if [ "$1" -eq "0" ]; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null ||:
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/%{pear_name}
%{pear_phpdir}/MDB2.php


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-0.10.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-0.9.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-0.8.b5
- update to 2.5.0b5

* Wed Oct 24 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-0.7.b4
- update to 2.5.0b4

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 2.5.0-0.6.b3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-0.5.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-0.4.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> 2.5.0-0.3.b3
- doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-0.2.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 31 2010 Remi Collet <Fedora@FamilleCollet.com> - 2.5.0-0.1.b3
- update to 2.5.0b3
- move MDB2.xml to php-pear-MDB2.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 13 2007 Christopher Stone <chris.stone@gmail.com> 2.4.1-2
- Add LOB security patch (bz #379081)

* Sat May 05 2007 Christopher Stone <chris.stone@gmail.com> 2.4.1-1
- Upstream sync

* Tue Mar 13 2007 Christopher Stone <chris.stone@gmail.com> 2.4.0-1
- Upstream sync

* Tue Nov 21 2006 Christopher Stone <chris.stone@gmail.com> 2.3.0-1
- Upstream sync
- Move LICENSE file from %%{pear_datadir} to %%doc

* Thu Sep 07 2006 Christopher Stone <chris.stone@gmail.com> 2.2.2-2
- Sync up with latest pear template

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 2.2.2-1
- Upstream sync
- Update spec to latest template

* Sun Sep 03 2006 Christopher Stone <chris.stone@gmail.com> 2.1.0-4
- Update to latest template

* Thu Jun 29 2006 Christopher Stone <chris.stone@gmail.com> 2.1.0-3
- Remove some hacks, clean up spec file

* Wed Jun 28 2006 Christopher Stone <chris.stone@gmail.com> 2.1.0-2
- Remove %%build section since it is not used

* Mon Jun 26 2006 Christopher Stone <chris.stone@gmail.com> 2.1.0-1
- Initial Release
