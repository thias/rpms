Name:       libmaxminddb
Version:    1.3.1
Release:    1%{?dist}
Summary:    Library for the MaxMind DB file format
Group:      System Environment/Libraries
License:    ASL 2.0
URL:        https://github.com/maxmind/libmaxminddb
Source0:    https://github.com/maxmind/libmaxminddb/releases/download/%{version}/libmaxminddb-%{version}.tar.gz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
The libmaxminddb library provides a C library for reading MaxMind DB files,
including the GeoIP2 databases from MaxMind. This is a custom binary format
designed to facilitate fast look ups of IP addresses while allowing for great
flexibility in the type of data associated with an address.


%package devel
Summary:    Development files for the %{name} library
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the %{name} library.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/mmdblookup
%{_libdir}/libmaxminddb.so.*
%{_mandir}/man1/mmdblookup.1*

%files devel
%defattr(-,root,root,-)
%doc doc/libmaxminddb.md
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_libdir}/libmaxminddb.so
%{_includedir}/maxminddb*.h
%exclude %{_libdir}/libmaxminddb.a
%exclude %{_libdir}/libmaxminddb.la
%{_mandir}/man3/*.3*


%changelog
* Tue Jan  9 2018 Matthias Saou <matthias@saou.eu> 1.3.1-1
- Update to 1.3.1.

* Tue May 16 2017 Matthias Saou <matthias@saou.eu> 1.2.1-1
- Update to 1.2.1.

* Wed Feb  8 2017 Matthias Saou <matthias@saou.eu> 1.2.0-1
- Update to 1.2.0.

* Tue Feb  9 2016 Matthias Saou <matthias@saou.eu> 1.1.4-1
- Update to 1.1.4.
- Include new pkgconfig file.

* Mon Jan 12 2015 Matthias Saou <matthias@saou.eu> 1.0.4-1
- Update to 1.0.4.

* Tue Aug 26 2014 Matthias Saou <matthias@saou.eu> 0.5.6-1
- Initial RPM release.

