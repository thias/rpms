%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_name   ConsoleTools
%global channel     components.ez.no

Name:           php-ezc-ConsoleTools
Version:        1.6.1
Release:        8%{?dist}
Summary:        A set of classes to do different actions with the console

Group:          Development/Libraries
License:        BSD
URL:            http://ezcomponents.org/
Source0:        http://components.ez.no/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.1
Requires:       php-pear(%{channel}/Base) >= 1.8
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
The ConsoleTools component provides several useful tools to build applications
that run on a computer console (sometimes also called shell or command line).


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}

# This are really doc, not data, not used in the code
sed -e '/design/s/role="data"/role="doc"/' \
    -i %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/ezc/%{pear_name}
%{pear_phpdir}/ezc/autoload/console_autoload.php


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 01 2013 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-7
- Fix metadata location, FTBFS #914339

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.6.1-5
- move data to doc (not used in the code, really doc)
- doc in /usr/share/doc/pear

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Mar 27 2010 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-1
- Upstream 1.6.1

* Thu Dec 24 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6-1
- Upstream 1.6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.5.2-1
- Upstream 1.5.2

* Tue May 12 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.5.1-1
- Upstream 1.5.1

* Sun Feb 08 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.5-1
- Initial packaging
