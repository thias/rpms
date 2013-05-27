%{!?ruby_sitedir: %define ruby_sitedir %(ruby -rrbconfig -e "puts RbConfig::CONFIG['sitedir']")}
%global         _name rgen

Name:           ruby-%{_name}
Version:        0.6.2
Release:        1%{?dist}
Summary:        Ruby Modeling and Generator Framework
Group:          Development/Languages

License:        MIT
URL:            https://rubygems.org/gems/%{_name}
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby >= 1.8
Requires:       ruby >= 1.8
BuildArch:      noarch

%description
RGen is a framework for Model Driven Software Development (MDSD) in Ruby. This
means that it helps you build Metamodels, instantiate Models, modify and
transform Models and finally generate arbitrary textual content from it.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -d -m0755 %{buildroot}%{ruby_sitedir}
cp -pr lib/* %{buildroot}%{ruby_sitedir}
ls %{buildroot}%{ruby_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG README.rdoc MIT-LICENSE Rakefile
%{ruby_sitedir}/ea_support/*
%{ruby_sitedir}/metamodels/*
%{ruby_sitedir}/mmgen/*
%{ruby_sitedir}/rgen/*
%{ruby_sitedir}/transformers/*


%changelog
* Fri Apr 12 2013 Moses Mendoza <msoes@puppetlabs.com> - 0.6.2-1
- Package rgen as a library. The tarball is created from a `gem unpack`
- of rubygem-rgen and tarring up the resulting contents.
