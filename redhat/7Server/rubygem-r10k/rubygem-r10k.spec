%global gem_name r10k

Summary: Puppet environment and module deployment
Name: rubygem-%{gem_name}
Version: 2.1.1
Release: 1%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://github.com/puppetlabs/r10k
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: rubygem(colored) >= 1.2
Requires: rubygem(cri) >= 2.6.0
Requires: rubygem(log4r) >= 1.1.10
Requires: rubygem(multi_json) >= 1.10
Requires: rubygem(puppet_forge) >= 2.1.1
Requires: rubygem(faraday) >= 0.9.0
Requires: rubygem(faraday_middleware) >= 0.9.0
Requires: rubygem(faraday_middleware-multi_json) >= 0.0.6
Requires: rubygem(semantic_puppet) >= 0.1.0
Requires: rubygem(minitar)
Requires: rubygem(multipart-post) >= 1.2
Requires: rubygem(multipart-post) < 3
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
# BuildRequires: rubygem(rspec) => 3.1
# BuildRequires: rubygem(rspec) < 4
# BuildRequires: rubygem(yard) => 0.8.7.3
# BuildRequires: rubygem(yard) < 0.8.8
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
R10K provides a general purpose toolset for deploying Puppet environments
and modules. It implements the Puppetfile format and provides a native
implementation of Puppet dynamic environments.


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

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


%check
pushd .%{gem_instdir}

popd


%files
%dir %{gem_instdir}
%{_bindir}/r10k
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_instdir}/integration
%{gem_libdir}
%{gem_instdir}/r10k.yaml.example
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.mkd
%doc %{gem_instdir}/CONTRIBUTING.mkd
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.mkd
%doc %{gem_instdir}/doc
%{gem_instdir}/r10k.gemspec
%{gem_instdir}/spec


%changelog
* Tue Jan 26 2016 Matthias Saou <matthias@saou.eu> - 2.1.1-1
- Update to 2.1.1 for RHEL7.

* Thu Jun  5 2014 Matthias Saou <matthias@saou.eu> - 1.2.1-1
- Update to 1.2.1.
- Update rubygem(cri) requirement.

* Mon Mar 10 2014 Matthias Saou <matthias@saou.eu> - 1.2.0-1
- Update to 1.2.0.

* Tue Feb  4 2014 Matthias Saou <matthias@saou.eu> - 1.1.3-1
- Update to 1.1.3.

* Thu Oct 17 2013 Matthias Saou <matthias@saou.eu> - 1.1.0-1
- Initial package, using gem2rpm.

