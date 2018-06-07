%define debug_package %{nil}

Summary: LSI MegaRAID StorCLI
Name: storcli
Version: 7.6
Release: 1
License: Proprietary
Group: System Environment/Base
URL: https://www.broadcom.com/
Source0: https://docs.broadcom.com/docs-and-downloads/raid-controllers/raid-controllers-common-files/007.0606.0000.0000_Unified_StorCLI.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: dos2unix
ExclusiveArch: %{ix86} x86_64

%description
LSI (Avago) MegaRAID StorCLI.


%prep
%setup -q -c
# We have rpms inside a zip inside a zip inside a zip...
unzip MR_SAS_Unified_StorCLI_%{version}-*.zip
unzip versionChangeSet/univ_viva_cli_rel/Unified_storcli_all_os.zip
# Convert from iso8859-1/dos to utf-8/unix
for txt in *_StorCLI.txt Unified_storcli_all_os/Linux/*.txt; do
  iconv -f iso8859-1 -t utf-8 -o tmp ${txt}
  dos2unix tmp
  touch -r ${txt} tmp
  mv tmp ${txt}
done
# Extract the 'noarch' rpm
rpm2cpio Unified_storcli_all_os/Linux/storcli-*.noarch.rpm | cpio -dim


%build


%install
rm -rf %{buildroot}
%ifarch %{ix86}
install -p -D -m 0755 opt/MegaRAID/storcli/storcli \
  %{buildroot}%{_sbindir}/storcli
%endif
%ifarch x86_64
install -p -D -m 0755 opt/MegaRAID/storcli/storcli64 \
  %{buildroot}%{_sbindir}/storcli
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%license Unified_storcli_all_os/Linux/license.txt
%doc *_StorCLI.txt Unified_storcli_all_os/Linux/LINUX_Readme.txt
%{_sbindir}/storcli


%changelog
* Thu Jun  7 2018 Matthias Saou <matthias@saou.eu> 7.6-1
- Update to 7.6.

* Tue Sep 29 2015 Matthias Saou <matthias@saou.eu> 1.16.06-2
- Initial RPM release.

