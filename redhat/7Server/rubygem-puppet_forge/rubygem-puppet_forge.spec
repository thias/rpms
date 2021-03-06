# Generated from puppet_forge-2.1.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name puppet_forge

Name: rubygem-%{gem_name}
Version: 2.1.3
Release: 1%{?dist}
Summary: Access the Puppet Forge API from Ruby for resource information and to download releases
Group: Development/Languages
License: Apache-2.0
URL: https://github.com/puppetlabs/forge-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
# BuildRequires: rubygem(rspec) => 3.0
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(simplecov)
# BuildRequires: rubygem(cane)
# BuildRequires: rubygem(yard)
# BuildRequires: rubygem(redcarpet)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Tools that can be used to access Forge API information on Modules, Users, and
Releases. As well as download, unpack, and install Releases to a directory.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/




# Run the test suite
%check
pushd .%{gem_instdir}

popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gitignore
%license %{gem_instdir}/LICENSE.txt
%{gem_instdir}/MAINTAINERS
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/puppet_forge.gemspec
%{gem_instdir}/spec

%changelog
* Tue Jan 26 2016 Matthias Saou <matthias@saou.eu> - 2.1.3-1
- Initial package

