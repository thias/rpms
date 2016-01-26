# Generated from semantic_puppet-0.1.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name semantic_puppet

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 1%{?dist}
Summary: Useful tools for working with Semantic Versions
Group: Development/Languages
License: Apache-2.0
URL: https://github.com/puppetlabs/semantic_puppet-gem
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.7
# BuildRequires: rubygem(rspec)
# BuildRequires: rubygem(simplecov)
# BuildRequires: rubygem(cane)
# BuildRequires: rubygem(yard)
# BuildRequires: rubygem(redcarpet)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Tools used by Puppet to parse, validate, and compare Semantic Versions and
Version Ranges and to query and resolve module dependencies.


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
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/semantic_puppet.gemspec
%{gem_instdir}/spec

%changelog
* Tue Jan 26 2016 Matthias Saou <matthias@saou.eu> - 0.1.1-1
- Initial package

