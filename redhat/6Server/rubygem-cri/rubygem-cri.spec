%global gemname cri

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Library for building easy-to-use commandline tools
Name: rubygem-%{gemname}
Version: 2.4.0
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://stoneship.org/software/cri/
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: rubygem(colored) >= 1.2
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Cri allows building easy-to-use commandline interfaces with support for
subcommands.


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
%{geminstdir}/
%exclude %{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/ChangeLog
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README.md
%doc %{geminstdir}/NEWS.md


%changelog
* Thu Oct 17 2013 Matthias Saou <matthias@saou.eu> - 2.4.0-1
- Initial package, using gem2rpm.

