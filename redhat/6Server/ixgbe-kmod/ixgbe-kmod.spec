# Define the kmod package name here.
%define kmod_name ixgbe

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 2.6.32-431.29.2.el6.%{_target_cpu}}

Name:    %{kmod_name}-kmod
Version: 3.22.3
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: %{kmod_name} kernel module(s)
URL:     http://www.intel.com/

BuildRequires: redhat-rpm-config
BuildRequires: kernel-devel
ExclusiveArch: i686 x86_64

# Sources.
Source0:  %{kmod_name}-%{version}.tar.gz
Source5:  GPL-v2.0.txt
Source10: kmodtool-%{kmod_name}-el6.sh

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n %{kmod_name}-%{version}
%{__gzip} %{kmod_name}.7
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
pushd src >/dev/null
%{__make} KSRC=%{_usrsrc}/kernels/%{kversion}
popd >/dev/null

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} src/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} pci.updates %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} README %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -d %{buildroot}%{_mandir}/man7/
%{__install} %{kmod_name}.7.gz %{buildroot}%{_mandir}/man7/
# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;
# Remove the unrequired files.
%{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*

%clean
%{__rm} -rf %{buildroot}

%changelog
* Tue Sep 23 2014 Matthias Saou <matthias@saou.eu> - 3.22.3-1
- Updated version to 3.22.3.
* Thu May 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.21.2-1
- Updated version to 3.21.2

* Sat Mar 01 2014 Alan Bartlett <ajb@elrepo.org> - 3.19.1-1
- Updated version to 3.19.1

* Mon Nov 11 2013 Alan Bartlett <ajb@elrepo.org> - 3.18.7-1
- Updated version to 3.18.7

* Fri Aug 02 2013 Alan Bartlett <ajb@elrepo.org> - 3.17.3-1
- Updated version to 3.17.3

* Mon Jul 01 2013 Alan Bartlett <ajb@elrepo.org> - 3.15.1-1
- Updated version to 3.15.1

* Sat Apr 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.14.5-1
- Updated version to 3.14.5

* Sat Mar 02 2013 Alan Bartlett <ajb@elrepo.org> - 3.13.10-1
- Updated version to 3.13.10

* Sat Jan 05 2013 Alan Bartlett <ajb@elrepo.org> - 3.12.6-1
- Updated version to 3.12.6

* Sat Oct 20 2012 Alan Bartlett <ajb@elrepo.org> - 3.11.33-1
- Updated version to 3.11.33

* Mon Sep 17 2012 Alan Bartlett <ajb@elrepo.org> - 3.10.17-1
- Updated version to 3.10.17

* Sat Jul 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.9.17-1
- Updated version to 3.9.17

* Wed May 02 2012 Alan Bartlett <ajb@elrepo.org> - 3.9.15-1
- Initial el6 build of the kmod package.
