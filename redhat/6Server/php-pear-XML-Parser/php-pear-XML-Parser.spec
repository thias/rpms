# spec file for php-pear-XML-Parser
#
# Copyright (c) 2006-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   XML_Parser
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

Name:         php-pear-XML-Parser
Version:      1.3.4
Release:      10%{?dist}
Summary:      XML parsing class based on PHP's bundled expat
Summary(fr):  Une classe d'analyse XML utilisant l'extension expat de PHP
License:      BSD

Group:        Development/Libraries
URL:          http://pear.php.net/package/XML_Parser
Source0:      http://pear.php.net/get/%{pear_name}-%{version}.tgz
Source2:      xml2changelog

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear
%if %{with_tests}
# For tests
BuildRequires:    php-mbstring
BuildRequires:    php-pear(XML_RSS)
%endif

Requires(post):   %{__pear}
Requires(postun): %{__pear}
Requires:         php-pear(PEAR) >= 1.4.9

Provides:         php-pear(%{pear_name}) = %{version}


%description
This is an XML parser based on PHPs built-in xml extension.
It supports two basic modes of operation: "func" and "event".  
In "func" mode, it will look for a function named after each element 
(xmltag_ELEMENT for start tags and xmltag_ELEMENT_ for end tags), 
and in "event" mode it uses a set of generic callbacks.

Since version 1.2.0 there's a new XML_Parser_Simple class that makes 
parsing of most XML documents easier, by automatically providing a stack 
for the elements. Furthermore its now possible to split the parser from 
the handler object, so you do not have to extend XML_Parser anymore in 
order to parse a document with it.

%description -l fr
Une analyseur XML utilisant l'extension xml intégrée à PHP.
Il supporte deux simples modes de fonctionnement : "func" et "event".
Dans le mode "func", il cherche une fonction nommée après chaque élément
(xmltag_ELEMENT pour le drapeau de début et xmltag_ELEMENT_ pour celui
de fin), et dans le mode "event" il utilise en ensemble de fonctions
"callbacks" génériques.

Depuis la version 1.2.0, la nouvelle classe XML_Parser_Simple simplifie
l'analyse de la plupart des documents XML, en fournissant automatiquement
une pile pour les éléments. De plus il est désormais possible de séparer
l'analyseur du gestionnaire d'objets, il n'est donc plus nécessaire d'étendre
XML_Parser pour analyser un document.


%prep
%setup -q -c
%{_bindir}/php -n %{SOURCE2} package.xml | tee CHANGELOG | head -n 10

cd %{pear_name}-%{version}
# package.xml is V2
mv ../package.xml %{name}.xml


%build
# Empty build section


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}

%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
%{__mkdir_p} %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Fic documentation
for file in  %{buildroot}%{pear_docdir}/%{pear_name}/examples/*; do
  %{__sed} -i -e 's/\r//' $file
done


%check
%if %{with_tests}
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} \
   run-tests \
   -i "-d include_path=%{buildroot}%{pear_phpdir}:%{pear_phpdir}" \
   tests | tee ../testslog
grep "FAILED TESTS" ../testslog && exit 1
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ "$1" -eq "0" ]; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc CHANGELOG
%doc %{pear_docdir}/%{pear_name}
%{pear_phpdir}/XML/Parser
%{pear_phpdir}/XML/Parser.php
%{pear_testdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml


%changelog
* Fri Jan 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-10
- run tests only when build with --with tests (circular dep.)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Remi Collet <remi@fedoraproject.org> - 1.3.4-8
- fix metadata location

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.3.4-6
- rebuilt for new pear_testdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 30 2011 Remi Collet <Fedora@FamilleCollet.com> 1.3.4-3
- doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Remi Collet <Fedora@FamilleCollet.com> 1.3.4-1
- Version 1.3.4 (stable) - API 1.3.0 (stable)
- define timezone during build
- run tests in %%check

* Sat May 22 2010 Remi Collet <Fedora@FamilleCollet.com> 1.3.2-4
- spec cleanup
- rename XML_Parser.xml to php-pear-XML-Parser.xml

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Remi Collet <Fedora@FamilleCollet.com> 1.3.2-1
- update to 1.3.2

* Tue Sep 30 2008 Remi Collet <Fedora@FamilleCollet.com> 1.3.1-1
- update to 1.3.1
- fix in package.xml (license)

* Fri Aug 29 2008 Remi Collet <Fedora@FamilleCollet.com> 1.3.0-1
- update to 1.3.0
- Switched license to BSD License

* Fri Aug 24 2007 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-2
- Fix License

* Sat Dec 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.8-1
- update to 1.2.8
- remove PEAR from sumnary
- don't own %%{pear_phpdir}/XML
- spec cleanning (new template)

* Fri Sep 08 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.7-4
- last template.spec

* Sun Sep 03 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.7-3
- new and simpler %%prep and %%install

* Sat Sep 02 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.7-2
- use new macros from /etc/rpm/macros.pear
- own /usr/share/pear/XML
- require php >= 4.2.0

* Sun May 21 2006 Remi Collet <Fedora@FamilleCollet.com> 1.2.7-1
- spec for extras
- add french description & sumnary
