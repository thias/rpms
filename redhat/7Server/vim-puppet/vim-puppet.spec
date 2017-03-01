%global vimfiles_root %{_datadir}/vim/vimfiles

Name:           vim-puppet
Version:        0.0
Release:        1%{?dist}
Summary:        Puppet Vim syntax highlighting and other enhancements
Group:          Applications/Editors
License:        n/a
URL:            https://github.com/rodjek/vim-puppet
Source0:        https://github.com/rodjek/vim-puppet/archive/master.tar.gz
Patch0:         vim-puppet-master-disable-puppet_align_hashes.patch
Requires:       vim-common
Requires(post): vim
Requires(postun): vim
BuildArch:      noarch

%description
Make vim more Puppet friendly! Provides formatting based on the latest
Puppetlabs Style Guide, sntax highlighting compatible with puppet 4.x,
automatic => alignment.


%prep
%setup -q -n %{name}-master
%patch0 -p1


%build


%install
mkdir -p %{buildroot}%{vimfiles_root}
cp -ar {after,autoload,ftdetect,ftplugin,indent,syntax} \
    %{buildroot}%{vimfiles_root}


%files
%doc README.md
%{vimfiles_root}/after/*
%{vimfiles_root}/autoload/*
%{vimfiles_root}/ftdetect/*
%{vimfiles_root}/ftplugin/*
%{vimfiles_root}/indent/*
%{vimfiles_root}/syntax/*


%changelog
* Wed Mar  1 2017 Matthias Saou <matthias@saou.eu> 0.0-0
- Quick 'n dirty RPM package to complement AIO puppet-agent.

