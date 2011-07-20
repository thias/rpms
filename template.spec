Summary: 
Name: 
Version: 
Release: 1%{?dist}
License: GPLv2+
Group: 
URL: 
Source0: 
Source1: 
Patch0: 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: 
BuildRequires: 

%description


%package devel
Summary: 
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add xx
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service xx stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xx
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service xx condrestart >/dev/null 2>&1 || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*
%{_mandir}/man?/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%exclude %{_libdir}/*.la
%{_libdir}/*.so


%changelog
* Thu Jul  1 2004 Matthias Saou <matthias@saou.eu> 0-1
- Initial RPM release.

