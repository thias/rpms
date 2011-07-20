Summary: Freshrpms.net release file and package configuration
Name: freshrpms-release
Version: 1.2
Release: 1
License: GPL
Group: System Environment/Base
Source0: GPL
Source1: RPM-GPG-KEY-freshrpms
Source2: freshrpms.repo
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: rpmfusion-free-release
Requires: rpmfusion-nonfree-release

%description
Freshrpms.net release file. This package also contains yum configuration to
use the freshrpms.net provided rpm packages, as well as the public gpg key
used to sign them.


%prep


%build


%install
%{__rm} -rf %{buildroot}
# Install license to be included in the docs and gpg key as pubkey
%{__cp} -a %{SOURCE0} %{SOURCE1} .
# Install gpg public key
%{__install} -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-freshrpms
# Install yum repo file
%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/yum.repos.d/freshrpms.repo


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%doc GPL
%pubkey RPM-GPG-KEY-freshrpms
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-freshrpms
%config(noreplace) %{_sysconfdir}/yum.repos.d/freshrpms.repo


%changelog
* Tue Nov 25 2008 Matthias Saou <http://freshrpms.net/> 1.2-1
- No longer automatically import the gpg key, as yum has been interactive about
  this for a while already.
- Require rpmfusion free and nonfree release packages, for transparent
  migration from freshrpms to rpmfusion.

* Tue Jun 28 2005 Matthias Saou <http://freshrpms.net/> 1.1-1
- Put gpg public key in /etc/pki/rpm-gpg and add gpgkey line to yum file.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 1-1
- Initial RPM release, inspired by fedora-release.
- No /etc/freshrpms-release (for now at least), as it's basically useless :-)

