%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define channel components.ez.no

Name:           php-channel-ezc
Version:        1
Release:        7%{?dist}
Summary:        Adds eZ Components channel to PEAR

Group:          Development/Libraries
License:        BSD
URL:            http://ezcomponents.org/
Source0:        http://components.ez.no/channel.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear(PEAR)
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-channel(ezc)
Provides:       php-channel(%{channel})


%description
This package adds the eZ Components channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -qcT


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
install -d %{buildroot}%{pear_xmldir}
install -p -m 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


%post
if [ $1 -eq  1 ] ; then
    %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
    %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} channel-delete %{channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jan 25 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1-1
- Initial packaging
