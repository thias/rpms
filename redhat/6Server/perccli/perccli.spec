%define debug_package %{nil}

Summary: Dell PERC LSI MegaRAID StorCLI fork
Name: perccli
Version: 7.1
Release: 1
License: Proprietary
Group: System Environment/Base
URL: http://www.dell.com/
Source0: https://downloads.dell.com/FOLDER04470715M/1/perccli_7.1-007.0127_linux.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: dos2unix
ExclusiveArch: %{ix86} x86_64

%description
Dell PERC LSI (Avago, Broadcom) MegaRAID StorCLI fork.


%prep
%setup -q -c
# Extract the 'noarch' rpm
rpm2cpio Linux/perccli-*.noarch.rpm | cpio -dim
# Convert from iso8859-1/dos to utf-8/unix
for txt in *.txt; do
  iconv -f iso8859-1 -t utf-8 -o tmp ${txt}
  dos2unix tmp
  touch -r ${txt} tmp
  mv tmp ${txt}
done


%build


%install
rm -rf %{buildroot}
%ifarch %{ix86}
install -p -D -m 0755 opt/MegaRAID/perccli/perccli \
  %{buildroot}%{_sbindir}/perccli
%endif
%ifarch x86_64
install -p -D -m 0755 opt/MegaRAID/perccli/perccli64 \
  %{buildroot}%{_sbindir}/perccli
%endif
ln -s perccli %{buildroot}%{_sbindir}/storcli


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%license license.txt
%{_sbindir}/perccli
%{_sbindir}/storcli


%changelog
* Mon Jun 11 2018 Matthias Saou <matthias@saou.eu> 7.1-1
- Initial RPM release, based on storcli package.

