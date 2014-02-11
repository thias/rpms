%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name XML_Beautifier

# Test cannot be run with PHP 5 because the XML tag 
# is not being included in the output.

Name:           php-pear-XML-Beautifier
Version:        1.2.2
Release:        9%{?dist}
Summary:        Class to format XML documents

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/XML_Beautifier
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear

Requires:       php-pear(PEAR) 
Requires:       php-pear(XML_Util) >= 0.5
Requires:       php-pear(XML_Parser) >= 1.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
XML_Beautifier is a package, that helps you making XML documents easier to
read for human beings.

It is able to add line-breaks, indentation, sorts attributes, convert tag
cases and wraps long comments. It recognizes tags, character data, comments,
XML declarations, processing instructions and external entities and is able
to format these tokens nicely.

The document is split into these tokens using the XML_Beautifier_Tokenizer
class and the expat parser. Then a renderer is used to create the string
representation of the document and formats it using the specified options.

Currently only one renderer is available, but as XML_Beautifier uses a
driver-based architecture, other renderers (like syntax-highlighting)
will follow soon. 


%prep
%setup -qc
%{_bindir}/php -n %{SOURCE2} package.xml | tee CHANGELOG | head -n 10

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


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
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


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
%{pear_phpdir}/XML/Beautifier*
%{pear_testdir}/%{pear_name}


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-8
- fix metadata location

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-6
- rebuilt for new pear_testdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 30 2011 Remi Collet <Fedora@FamilleCollet.com> 1.2.2-3
- doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)
- add generated Changelog

* Mon Aug 23 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-4
- clean define
- rename XML_Beautifier.xml to php-pear-XML-Beautifier.xml
- set date.timezone during build

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Christohper Stone <chris.stone@gmail.com> 1.2.0-1
- Upstream sync
- Update license to BSD

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-3
- fix license tag

* Sun Jan 14 2007 Christopher Stone <chris.stone@gmail.com> 1.1-2
- Add license to %%files

* Sat Oct 14 2006 Christopher Stone <chris.stone@gmail.com> 1.1-1
- Initial release
