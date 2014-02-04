%global gemname r10k

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Puppet environment and module deployment
Name: rubygem-%{gemname}
Version: 1.1.3
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/adrienthebo/r10k
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: rubygem(colored) >= 1.2
Requires: rubygem(cri) => 2.4.0
Requires: rubygem(cri) < 2.5
Requires: rubygem(systemu) => 2.5.2
Requires: rubygem(systemu) < 2.6
Requires: rubygem(log4r) >= 1.1.10
Requires: rubygem(json_pure) 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
R10K provides a general purpose toolset for deploying Puppet environments
and modules. It implements the Puppetfile format and provides a native
implementation of Puppet dynamic environments.


%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -pa .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x


%files
%dir %{geminstdir}
%doc %{gemdir}/doc/%{gemname}-%{version}
%{_bindir}/r10k
%{geminstdir}/
%exclude %{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Tue Feb  4 2014 Matthias Saou <matthias@saou.eu> - 1.1.3-1
- Update to 1.1.3.

* Thu Oct 17 2013 Matthias Saou <matthias@saou.eu> - 1.1.0-1
- Initial package, using gem2rpm.

