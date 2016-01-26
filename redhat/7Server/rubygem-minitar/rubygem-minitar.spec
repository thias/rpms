# Generated from minitar-0.5.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name minitar

Name: rubygem-%{gem_name}
Version: 0.5.4
Release: 1%{?dist}
Summary: Provides POSIX tarchive management from Ruby programs
Group: Development/Languages
License: MIT
URL: http://www.github.com/atoulme/minitar
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.8.2
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Archive::Tar::Minitar is a pure-Ruby library and command-line utility that
provides the ability to deal with POSIX tar(1) archive files. The
implementation is based heavily on Mauricio Ferna'ndez's implementation in
rpa-base, but has been reorganised to promote reuse in other projects. Antoine
Toulme forked the original project on rubyforge to place it on github, under
http://www.github.com/atoulme/minitar.


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

# Run the test suite
%check
pushd .%{gem_instdir}

popd

%files
%dir %{gem_instdir}
%{_bindir}/minitar
%{gem_instdir}/Install
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/README
%{gem_instdir}/Rakefile
%{gem_instdir}/tests

%changelog
* Tue Jan 26 2016 Matthias Saou <matthias@saou.eu> - 0.5.4-1
- Initial package
