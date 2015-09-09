Name:           perl-Math-Int128
Version:        0.22
Release:        1%{?dist}
Summary:        Manipulate 128 bits integers in Perl
License:        (GPL+ or Artistic) and Public Domain and BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Math-Int128/
Source0:        http://www.cpan.org/modules/by-module/Math/Math-Int128-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Math::Int64)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Test::More)
Requires:       perl(Exporter)
Requires:       perl(Math::Int64)
Requires:       perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module adds support for 128 bit integers, signed and unsigned, to Perl.

%prep
%setup -q -n Math-Int128-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README.md
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Math*
%{_mandir}/man3/*

%changelog
* Wed Sep  9 2015 Matthias Saou <matthias@saou.eu> 0.22-1
- Initial RPM release, based on perl-Math-Int64 spec.

