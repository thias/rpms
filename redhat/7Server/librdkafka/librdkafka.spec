# remirepo/fedora spec file for librdkafka
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global libname      librdkafka
%global gh_commit    0d540ab4e78a3e3661fe07ee328e2f61fb77f2c3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     edenhill
%global gh_project   %{libname}

Name:    %{libname}
Version: 0.9.5
Release: 1%{?dist}
Group:   System Environment/Libraries
Summary: Apache Kafka C/C++ client library

# librdkafka is BSD-2, pycrc is MIT, snappy is BSD-3
License: BSD and MIT
URL:     https://github.com/%{gh_owner}/%{gh_project}
Source0: https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

BuildRequires:  openssl-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  zlib-devel
BuildRequires:  libstdc++-devel
BuildRequires:  lz4-devel
BuildRequires:  gcc-c++
BuildRequires:  python


%description
librdkafka is a C library implementation of the Apache Kafka protocol,
containing both Producer and Consumer support.

It was designed with message delivery reliability and high performance
in mind, current figures exceed 800000 msgs/second for the producer
and 3 million msgs/second for the consumer.


%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -qn %{gh_project}-%{gh_commit}

mkdir rpmdocs
cp -pr examples rpmdocs/examples


%build
%configure \
    --enable-lz4 \
    --enable-ssl \
    --enable-sasl

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm %{buildroot}%{_libdir}/*.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%{_libdir}/%{libname}.so.1
%{_libdir}/%{libname}++.so.1

%files devel
%doc *md
%doc rpmdocs/examples
%{_includedir}/%{libname}/
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}++.so
%{_libdir}/pkgconfig/rdkafka.pc
%{_libdir}/pkgconfig/rdkafka++.pc


%changelog
* Fri Apr 21 2017 Remi Collet <remi@remirepo.net> - 0.9.5-1
- update to 0.9.5 (no change since RC2)

* Wed Apr 12 2017 Remi Collet <remi@remirepo.net> - 0.9.5~RC2-1
- update to 0.9.5-RC2

* Mon Apr 10 2017 Remi Collet <remi@remirepo.net> - 0.9.5~RC1-1
- update to 0.9.5-RC1

* Mon Feb 27 2017 Remi Collet <remi@remirepo.net> - 0.9.4-1
- update to 0.9.4

* Fri Feb 24 2017 Remi Collet <remi@remirepo.net> - 0.9.4-0.3.RC2
- update to 0.9.4RC2 for test

* Fri Feb 17 2017 Remi Collet <remi@remirepo.net> - 0.9.4-0.2.RC1
- enable lz4

* Thu Feb 16 2017 Remi Collet <remi@remirepo.net> - 0.9.4-0.1.RC1
- update to 0.9.4RC1 for test

* Mon Jan 23 2017 Remi Collet <remi@fedoraproject.org> - 0.9.3-1
- update to 0.9.3

* Wed Nov  9 2016 Remi Collet <remi@fedoraproject.org> - 0.9.2-1
- update to 0.9.2

* Sun May 29 2016 Remi Collet <remi@fedoraproject.org> - 0.9.1-1
- update to 0.9.1

* Sat Jan  9 2016 Remi Collet <remi@fedoraproject.org> - 0.9.0-1
- update to 0.9.0
- add upstream patch for old glibc (RHEL-5)

* Thu May 14 2015 Remi Collet <remi@fedoraproject.org> - 0.8.6-1
- initial package
