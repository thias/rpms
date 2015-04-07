%global realname puppetserver
%global realversion 1.0.8
%global rpmversion 1.0.8

%global open_jdk          java-1.7.0-openjdk

%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global rubylibdir        %(ruby -rrbconfig -e "puts Config::CONFIG['vendorlibdir']")
%else
%global rubylibdir        %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
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
Version:          1.0.8
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
# net-tools is required for netstat usage in service unit file
# See: https://tickets.puppetlabs.com/browse/SERVER-338
Requires:         net-tools

Requires:         puppet >= 3.7.3

Requires:         puppet < 4.0.0

Requires:         java-1.7.0-openjdk


%description
Puppet Server (puppetserver 1.0.8,trapperkeeper-webserver-jetty9 1.3.0)

%prep
%setup -q -n %{name}-%{realversion}

%build

%install

rm -rf $RPM_BUILD_ROOT

env DESTDIR=%{buildroot} prefix=%{_prefix} confdir=%{_sysconfdir} bindir=%{_bindir} rundir=%{_rundir}/puppetserver localstatedir=%{_localstatedir} rubylibdir=%{rubylibdir} bash install.sh install_redhat
%if %{_with_systemd}
env DESTDIR=%{buildroot} prefix=%{_prefix} confdir=%{_sysconfdir} bindir=%{_bindir} rundir=%{_rundir}/puppetserver defaultsdir=%{_sysconfdir}/sysconfig unitdir=%{_unitdir} bash install.sh systemd_redhat
%else
env DESTDIR=%{buildroot} prefix=%{_prefix} confdir=%{_sysconfdir} bindir=%{_bindir} rundir=%{_rundir}/puppetserver defaultsdir=%{_sysconfdir}/sysconfig initdir=%{_initrddir} bash install.sh sysv_init_redhat
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7 || 0%{?sles_version} >= 12
env DESTDIR=%{buildroot} confdir=%{_sysconfdir} bash install.sh logrotate
%else
env DESTDIR=%{buildroot} confdir=%{_sysconfdir} bash install.sh logrotate_legacy
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Note: changes to this section of the spec may require synchronisation with the
# install.sh source based installation methodology.
#
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
%{_datadir}/%{realname}/scripts/install.sh postinst_redhat

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
* Sat Mar 28 2015 Puppet Labs Release <info@puppetlabs.com> -  1.0.8-1
- Build for 1.0.8
