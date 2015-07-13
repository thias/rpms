%global _hardened_build 1

Name:          libwebp
Version:       0.4.3
Release:       3%{?dist}
Group:         Development/Libraries
URL:           http://webmproject.org/
Summary:       Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:       BSD
Source0:       http://downloads.webmproject.org/releases/webp/%{name}-%{version}.tar.gz
Source1:       libwebp_jni_example.java

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: giflib-devel
BuildRequires: libtiff-devel
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: swig
BuildRequires: autoconf automake libtool
BuildRequires: freeglut-devel

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package tools
Group:         Development/Tools
Summary:       The WebP command line tools

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package devel
Group:         Development/Libraries
Summary:       Development files for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%ifnarch ppc64
%package java
Group:         Development/Libraries
Summary:       Java bindings for libwebp, a library for the WebP format
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      java
Requires:      jpackage-utils

%description java
Java bindings for libwebp.
%endif

%prep
%setup -q

%build
autoreconf -vif
%ifarch aarch64
export CFLAGS="%{optflags} -frename-registers"
%endif
%configure --disable-static --enable-libwebpmux \
           --enable-libwebpdemux --enable-libwebpdecoder

make %{?_smp_mflags}

%ifnarch ppc64
# swig generated Java bindings
cp %{SOURCE1} .
cd swig
rm -rf libwebp.jar libwebp_java_wrap.c
mkdir -p java/com/google/webp
swig -ignoremissing -I../src -java \
    -package com.google.webp  \
    -outdir java/com/google/webp \
    -o libwebp_java_wrap.c libwebp.swig

gcc %{optflags} -fPIC -shared \
    -I/usr/lib/jvm/java/include \
    -I/usr/lib/jvm/java/include/linux \
    -I../src \
    -L../src/.libs -lwebp libwebp_java_wrap.c \
    -o libwebp_jni.so

cd java
javac com/google/webp/libwebp.java
jar cvf ../libwebp.jar com/google/webp/*.class
%endif

%install
%make_install
find "%{buildroot}/%{_libdir}" -type f -name "*.la" -delete

%ifnarch ppc64
# swig generated Java bindings
mkdir -p %{buildroot}/%{_libdir}/%{name}-java
cp swig/*.jar swig/*.so %{buildroot}/%{_libdir}/%{name}-java/
%endif

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/webpmux
%{_bindir}/vwebp
%{_mandir}/man*/*

%files -n %{name}
%doc README PATENTS NEWS AUTHORS
%doc COPYING
%{_libdir}/%{name}.so.5*
%{_libdir}/%{name}decoder.so.1*
%{_libdir}/%{name}demux.so.1*
%{_libdir}/%{name}mux.so.1*

%files devel
%{_libdir}/%{name}*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%ifnarch ppc64
%files java
%doc libwebp_jni_example.java
%{_libdir}/%{name}-java/
%endif

%changelog
* Thu Apr 02 2015 Sandro Mani <manisandro@gmail.com> - 0.4.3-3
- Requires: java-headless -> Requires: java

* Fri Mar 27 2015 Sandro Mani <manisandro@gmail.com> - 0.4.3-2
- Add BuildRequires: freeglut-devel to build vwebp

* Thu Mar 12 2015 Sandro Mani <manisandro@gmail.com> - 0.4.3-1
- upstream release 0.4.3

* Fri Oct 17 2014 Sandro Mani <manisandro@gmail.com> - 0.4.2-1
- upstream release 0.4.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.1-2
- Use frename-registers cflag to fix FTBFS on aarch64

* Tue Aug 05 2014 Sandro Mani <manisandro@gmail.com> - 0.4.1-1
- upstream release 0.4.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Jaromir Capik <jcapik@redhat.com> - 0.4.0-3
- Fixing endian checks (#962091)
- Fixing FTPBS caused by rpath presence

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.4.0-2
- Use Requires: java-headless rebuild (#1067528)

* Thu Jan 02 2014 Sandro Mani <manisandro@gmail.com> - 0.4.0-1
- upstream release 0.4.0

* Wed Oct 02 2013 Sandro Mani <manisandro@gmail.com> - 0.3.1-2
- enable webpdemux

* Sun Aug 04 2013 Sandro Mani <manisandro@gmail.com> - 0.3.1-1
- upstream release 0.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.0-1
- upstream release 0.3.0
- enable gif2webp
- add build requires on giflib-devel and libtiff-devel
- use make_install and hardened macros
- list binaries explicitly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.2.1-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.1-1
- new upstream release 0.2.1

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.1.3-3
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.3-1
- Several spec improvements by Scott Tsai <scottt.tw@gmail.com>

* Wed May 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.2-1
- Initial spec. Based on openSUSE one

