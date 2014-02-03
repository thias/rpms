%global gemname colored

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Add some color to your life
Name: rubygem-%{gemname}
Version: 1.2
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/defunkt/colored
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby(rubygems) 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
>> puts "this is red".red
>> puts "this is red with a blue background (read: ugly)".red_on_blue
>> puts "this is red with an underline".red.underline
>> puts "this is really bold and really blue".bold.blue
>> logger.debug "hey this is broken!".red_on_yellow     # in rails
>> puts Color.red "This is red" # but this part is mostly untested


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


%changelog
* Thu Oct 17 2013 Matthias Saou <matthias@saou.eu> - 1.2-1
- Initial package, using gem2rpm.

