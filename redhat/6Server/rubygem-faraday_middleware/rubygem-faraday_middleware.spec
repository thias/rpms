# Generated from faraday_middleware-0.9.0.gem by gem2rpm -*- rpm-spec -*-
%global gemname faraday_middleware

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Various middleware for Faraday
Name: rubygem-%{gemname}
Version: 0.9.0
Release: 2%{?dist}
Group: Development/Languages
License: Ruby
URL: https://github.com/pengwynn/faraday_middleware
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) >= 1.3.6
Requires: rubygem(faraday) >= 0.7.4
Requires: rubygem(faraday) < 0.9
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) >= 1.3.6
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Various middleware for Faraday


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --force %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -pa .%{gemdir}/* \
        %{buildroot}%{gemdir}/


%files
%{geminstdir}/lib/*
%exclude %{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{gemdir}/gems/*

%files doc
%doc %{gemdir}/doc/%{gemname}-%{version}


%changelog
* Mon Mar 10 2014 Matthias Saou <matthias@saou.eu> - 0.9.0-1
- Initial package

