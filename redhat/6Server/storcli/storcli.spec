%define debug_package %{nil}

Summary: LSI MegaRAID StorCLI
Name: storcli
Version: 1.16.06
Release: 2
License: Proprietary
Group: System Environment/Base
URL: http://www.lsi.com/
Source0: http://docs.avagotech.com/docs-and-downloads/raid-controllers/raid-controllers-common-files/MR_SAS_StorCLI_1-16-06.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: dos2unix
ExclusiveArch: %{ix86} x86_64

%description
LSI (Avago) MegaRAID StorCLI.


%prep
%setup -q -c
# We have rpms inside a zip inside a zip...
unzip storcli_all_os.zip
# Convert from iso8859-1/dos to utf-8/unix
for txt in %{version}_StorCLI.txt storcli_all_os/Linux/*.txt; do
  iconv -f iso8859-1 -t utf-8 -o tmp ${txt}
  dos2unix tmp
  touch -r ${txt} tmp
  mv tmp ${txt}
done
# Extract the 'noarch' rpm
rpm2cpio storcli_all_os/Linux/storcli-%{version}-1.noarch.rpm | cpio -dim


%build


%install
rm -rf %{buildroot}
# No idea what the libstorelibir-2.so.14.07-0 64bit shared lib is for, so skip
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
%doc %{version}_StorCLI.txt storcli_all_os/Linux/*.txt
%{_sbindir}/storcli


%changelog
* Tue Sep 29 2015 Matthias Saou <matthias@saou.eu> 1.16.06-2
- Initial RPM release.

