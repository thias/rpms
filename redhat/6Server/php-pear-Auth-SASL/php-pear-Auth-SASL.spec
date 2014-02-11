%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}

%global pear_name Auth_SASL

Summary:     Abstraction of various SASL mechanism responses
Summary(fr): Abstraction de différents mécanismes de réponse SASL
Name:        php-pear-Auth-SASL
Version:     1.0.6
Release:     6%{?dist}
License:     BSD
Group:       Development/Libraries
URL:         http://pear.php.net/package/Auth_SASL
Source:      http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear >= 1:1.4.9-1.2

Requires:         php-pear(PEAR) >= 1.4.9
Requires(post):   %{__pear}
Requires(postun): %{__pear}
Provides:         php-pear(%{pear_name}) = %{version}

%description
Provides code to generate responses to common SASL mechanisms, including:
o Digest-MD5
o CramMD5
o Plain
o Anonymous
o Login (Pseudo mechanism)

%description -l fr
Fournit le code pour répondre aux mécanismes SASL commun, comprenant :
o Digest-MD5 (secret partagé)
o CramMD5 (secret partagé)
o Plain (en clair)
o Anonymous (anonyme)
o Login (Pseudo-mécanisme)


%prep
%setup -c -q
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section


%install
rm -rf %{buildroot}

cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
# Sanity check
lst=$(find %{buildroot}%{pear_phpdir} -exec grep -q %{buildroot} {} \; -print)
[ ! -z "$lst" ] && echo "Reference to BUILDROOT in $lst" && exit 1;


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
# if refcount = 0 then package has been removed (not upgraded)
if [ "$1" -eq "0" ]; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only  %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_phpdir}/Auth
%{pear_xmldir}/%{name}.xml


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Remi Collet <remi@fedoraproject.org> - 1.0.6-5
- fix metadata location

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Remi Collet  <remi@fedoraproject.org> 1.0.6-1
- update to 1.0.6 (API 1.0.3) - QA release

* Wed Sep 14 2011 Remi Collet <Fedora@FamilleCollet.com> 1.0.5-1
- update to 1.0.5 - QA release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 08 2010 Remi Collet <Fedora@FamilleCollet.com> 1.0.4-1
- update to 1.0.4

* Sat Aug 08 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.3-1
- update to 1.0.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-6
- remove PEAR from sumnary
- remove php (httpd) dependency
- spec clean up

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 07 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-4
- last template.spec

* Sun Sep 03 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-3
- new and simpler %%prep and %%install

* Sun Jul 23 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-2
- use new macros from /etc/rpm/macros.pear
- own /usr/share/pear/Auth

* Sun May 21 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.2-1
- update to new 1.0.2

* Sat May 20 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-2
- Require pear >= 1.4.9
- use --packagingroot (instead of -R)
- check from install to check (as in php-pear)

* Sat May 06 2006 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- spec for extras
- use %%{_datadir}/pear/.pkgxml for XML (Bug #190252)

* Thu Apr 06 2006 Remi Collet <rpms@FamilleCollet.com> 1.0.1-2.fc{3,4,5}.remi
- change /var/lib/pear to %%{_libdir}/php/pear for XML (as in extras for FC5)
- spec cleanning

* Sat Mar 04 2006 Remi Collet <RPMS@FamilleCollet.com> 1.0.1-1.fc{3,4}.remi
- initial RPM of 1.0.1
