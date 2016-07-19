%define patchlevel adsecure6

Summary:    Headless WebKit with JavaScript API
Name:       phantomjs
Version:    2.0.0
Release:    6%{?dist}.%{patchlevel}
License:    BSD
Group:      Applications/Internet
Source:     https://bitbucket.org/ariya/phantomjs/downloads/%{name}-%{version}-source.zip
Patch0:     phantomjs-2.0.0-%{patchlevel}.patch

BuildRequires: flex
BuildRequires: bison
BuildRequires: gperf
BuildRequires: ruby
BuildRequires: python
BuildRequires: openssl-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: libicu-devel
BuildRequires: sqlite-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and native
support for various web standards: DOM handling, CSS selector, JSON,
Canvas, and SVG. PhantomJS is created by Ariya Hidayat.


%prep
%setup -q
%patch0 -p0


%build
./build.sh --confirm


%install
install -D -p -m 0755 bin/phantomjs %{buildroot}%{_bindir}/phantomjs


%files
%defattr(-,root,root,0755)
%doc CONTRIBUTING.md ChangeLog LICENSE.BSD README.md examples
%{_bindir}/phantomjs


%changelog
* Wed Mar 23 2016 Matthias Saou <matthias@saou.eu> 2.0.0-6
- Update patch to adsecure2.

* Wed Mar  9 2016 Matthias Saou <matthias@saou.eu> 2.0.0-5
- Update patch, now renamed to 'adsecure' and include that in the release.

* Tue Feb 16 2016 Matthias Saou <matthias@saou.eu> 2.0.0-4
- Update save patch.

* Tue Feb  9 2016 Matthias Saou <matthias@saou.eu> 2.0.0-3
- Include save patch.

* Mon Aug 10 2015 Matthias Saou <matthias@saou.eu> 2.0.0-2
- Spec file cleanup.

* Sat May 9 2015 Frankie Dintino <fdintino@gmail.com>
- updated to version 2.0, added BuildRequires directives

* Fri Apr 18 2014 Eric Heydenberk <heydenberk@gmail.com>
- add missing filenames for examples to files section

* Tue Apr 30 2013 Eric Heydenberk <heydenberk@gmail.com>
- add missing filenames for examples to files section

* Wed Apr 24 2013 Robin Helgelin <lobbin@gmail.com>
- updated to version 1.9

* Thu Jan 24 2013 Matthew Barr <mbarr@snap-interactive.com>
- updated to version 1.8

* Thu Nov 15 2012 Jan Schaumann <jschauma@etsy.com>
- first rpm version
