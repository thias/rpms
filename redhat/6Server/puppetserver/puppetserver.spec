%global realname puppetserver
%global realversion 1.0.2
%global rpmversion 1.0.2

%global open_jdk          java-1.7.0-openjdk

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global puppet_libdir     %(ruby -rrbconfig -e "puts Config::CONFIG['vendorlibdir']")
%else
%global puppet_libdir     %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%endif

%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%global _with_systemd 1
%else
%global _with_systemd 0
%endif

# These macros are not always defined on much older rpm-based systems
%global  _sharedstatedir /var/lib
%global  _realsysconfdir /etc
%global  _rundir         /var/run

%define __jar_repack     0

Name:             puppetserver
Version:          1.0.2
Release:          1%{?dist}
BuildRoot:        %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary:          Puppet Labs - puppetserver
License:          ASL 2.0

URL:              http://puppetlabs.com
Source0:          %{name}-%{realversion}.tar.gz

Group:            System Environment/Daemons
BuildArch:        noarch



BuildRequires:    ruby
BuildRequires:    /usr/sbin/useradd
%if %{_with_systemd}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
%else
Requires:         chkconfig
%endif

Requires:         %{open_jdk}

Requires:         puppet >= 3.7.3

Requires:         puppet < 4.0.0

Requires:         java-1.7.0-openjdk


%description
Release artifacts for puppet-server (puppet-server 1.0.2,trapperkeeper-webserver-jetty9 0.9.0)

%prep
%setup -q -n %{name}-%{realversion}

%build

%install

rm -rf $RPM_BUILD_ROOT

env DESTDIR=%{buildroot} prefix=%{_prefix} confdir=%{_sysconfdir} bindir=%{_bindir} rundir=%{_rundir}/puppetserver make -e install-puppetserver
%if %{_with_systemd}
install -d -m0755 %{buildroot}%{_unitdir}
install -m 0644 ext/redhat/puppetserver.service %{buildroot}%{_unitdir}/puppetserver.service
%else
install -d -m 0755 %{buildroot}%{_initrddir}
install -m 0755 ext/redhat/init %{buildroot}%{_initrddir}/puppetserver
%endif
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0755 ext/default %{buildroot}%{_sysconfdir}/sysconfig/puppetserver

install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7 || 0%{?sles_version} >= 12
cp -pr ext/puppetserver.logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/puppetserver
%else
cp -pr ext/puppetserver.logrotate-legacy.conf %{buildroot}%{_sysconfdir}/logrotate.d/puppetserver
%endif

install -d -m 700 %{buildroot}%{_localstatedir}/log/puppetserver

echo "os-settings: {"                         > %{buildroot}%{_sysconfdir}/%{realname}/conf.d/os-settings.conf
echo "    ruby-load-path: [%{puppet_libdir}]" >> %{buildroot}%{_sysconfdir}/%{realname}/conf.d/os-settings.conf
echo "}"                                      >> %{buildroot}%{_sysconfdir}/%{realname}/conf.d/os-settings.conf


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add puppet group
getent group puppet > /dev/null || \
  groupadd -r puppet || :
# Add puppet user
getent passwd puppet > /dev/null || \
  useradd -r -g puppet -d %{_datadir}/%{realname} -s /sbin/nologin \
     -c "puppetserver daemon"  puppet || :
install --group=puppet --owner=puppet -d /var/lib/puppet/jruby-gems
mkdir -p /etc/puppet/manifests

%post
%if %{_with_systemd}
# Reload the systemd units if this is an upgrade
if [ "$1" = "2" ]; then
    systemctl daemon-reload >/dev/null 2>&1 || :
    systemctl try-restart %{name}.service
fi
%systemd_post puppetserver.service
%else
# If this is an install (as opposed to an upgrade)...
if [ "$1" = "1" ]; then
    # Register the puppetserver service
    /sbin/chkconfig --add %{name}
# If this is an upgrade, restart if we are already running
elif [ "$1" = "2" ]; then
    if /sbin/service %{name} status > /dev/null 2>&1; then
        /sbin/service %{name} restart || :
    fi
fi
%endif

%preun
%if %{_with_systemd}
%systemd_preun puppetserver.service
%else
# If this is an uninstall (as opposed to an upgrade) then
#  we want to shut down and disable the service.
if [ "$1" = "0" ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if %{_with_systemd}
%systemd_postun_with_restart puppetserver.service
%else
# Remove the rundir if this is an uninstall (as opposed to an upgrade)...
if [ "$1" = "0" ]; then
    rm -rf %{_rundir}/%{name} || :
fi

# Only restart it if it is running
if [ "$1" = "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi
%endif

%files
%defattr(-, root, root)
%dir %attr(0700, puppet, puppet) %{_localstatedir}/log/%{name}
%{_datadir}/%{realname}
%if %{_with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/puppetserver
%ghost %attr(0755, root, root) %{_rundir}/%{name}




%changelog
* Wed Jan 14 2015 Puppet Labs Release <info@puppetlabs.com> -  1.0.2-1
- Build for 1.0.2

