%global realname puppetdb
%global realversion 2.3.0
%global rpmversion 2.3.0
%global puppetminversion 3.5.1
%global facterminversion 1.7.0

%define __jar_repack 0

%if 0%{?suse_version} >= 1220
%global open_jdk          java-1_7_0-openjdk
%else
%global open_jdk          java-1.7.0-openjdk
%endif

# On FOSS releases for platforms with ruby 1.9, puppet uses vendorlibdir instead of sitelibdir
# On PE, we use sitelibdir
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global puppet_libdir     %(ruby -rrbconfig -e "puts RbConfig::CONFIG['vendorlibdir']")
%else
%global puppet_libdir     %(ruby -rrbconfig -e "puts RbConfig::CONFIG['sitelibdir']")
%endif
%global puppet_4_libdir   /opt/puppetlabs/puppet/lib/ruby/vendor_ruby

# Fedora 17 and later and EL > 7 use systemd
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global _with_systemd 1
%else
%global _with_systemd 0
%endif

# These macros are not always defined on much older rpm-based systems
%global  _sharedstatedir /var/lib
%global  _realsysconfdir /etc
%if 0%{?suse_version}
%global  _initddir       %{_realsysconfdir}/init.d
%else
%global  _initddir       %{_realsysconfdir}/rc.d/init.d
%endif
%global  _rundir         /var/run


Name:          puppetdb
Version:       2.3.0
Release:       1%{?dist}
BuildRoot:     %{_tmppath}/%{realname}-%{version}-%{release}-root-%(%{__id_u} -n)

Summary:       Puppet Centralized Storage Daemon
%if 0%{?suse_version}
License:       Apache-2.0
%else
License:       ASL 2.0
%endif

URL:           http://github.com/puppetlabs/puppetdb
Source0:       http://downloads.puppetlabs.com/puppetdb/%{realname}-%{realversion}.tar.gz

%if 0%{?suse_version}
Group:         System/Daemons
%else
Group:         System Environment/Daemons
%endif

BuildRequires: facter >= %{facterminversion}
BuildRequires: puppet >= %{puppetminversion}
BuildRequires: rubygem-rake
BuildRequires: ruby
Requires:      puppet >= %{puppetminversion}
Requires:      facter >= %{facterminversion}
BuildArch:     noarch
%if 0%{?suse_version}
BuildRequires: aaa_base
BuildRequires: unzip
BuildRequires: sles-release
Requires:      aaa_base
Requires:      pwdutils
Requires:      logrotate
Requires:      procps
%else
BuildRequires: /usr/sbin/useradd
%if 0%{?_with_systemd}
# Required for %%post, %%preun, %%postun
Requires:       systemd
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires:  systemd
%else
BuildRequires:  systemd-units
%endif
%else
# Required for %%post and %%preun
Requires:       chkconfig
%endif
%endif
BuildRequires: %{open_jdk}
Requires:      %{open_jdk}

%description
Puppet Centralized Storage.

%package terminus
Summary: Puppet terminus files to connect to PuppetDB
%if 0%{?suse_version}
Group: System/Libraries
%else
Group: Development/Libraries
%endif
Requires: puppet >= %{puppetminversion}
Requires: rubygem-json

%description terminus
Connect Puppet to PuppetDB by setting up a terminus for PuppetDB.

%prep
%setup -q -n %{realname}-%{realversion}

%build

%install
%if 0%{?suse_version}
export NO_BRP_CHECK_BYTECODE_VERSION=true
%endif

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_initddir}

# Explicitly set environment variable LANG,
# because otherwise it gets set to 'C' and that
# is wrong, wrong, wrong. There may be a better
# way to handle this, so this may change.
export LANG=en_US.UTF-8

rake install PARAMS_FILE= DESTDIR=$RPM_BUILD_ROOT
rake terminus PARAMS_FILE= DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_rundir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/%{name}
touch  $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/%{name}.log

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7 || 0%{?sles_version} >= 12
sed -i '/notifempty/a\    su puppetdb puppetdb' $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/%{name}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Here we'll do a little bit of cleanup just in case something went horribly
# awry during a previous install/uninstall:
if [ -f "/usr/share/puppetdb/start_service_after_upgrade" ] ; then
   rm /usr/share/puppetdb/start_service_after_upgrade
fi
# If this is an upgrade (as opposed to an install) then we need to check
#  and see if the service is running.  If it is, we need to stop it.
#  we want to shut down and disable the service.
if [ "$1" = "2" ] ; then
%if 0%{?_with_systemd}
    # We test to see if the systemd service file exists because in upgrades from < 1.6.0,
    # puppetdb may still be using sysv and in that case we need to use the sysv tools.
    if [ -f %{_unitdir}/%{name}.service ]; then
      if /usr/bin/systemctl status %{name}.service > /dev/null; then
        # If we need to restart the service after the upgrade
        #  is finished, we will touch a temp file so that
        #  we can detect that state
        touch /usr/share/puppetdb/start_service_after_upgrade
        /usr/bin/systemctl stop %{name}.service >/dev/null 2>&1
      fi
    elif [ -f %{_initddir}/%{name} ]; then
      if /sbin/service %{name} status > /dev/null ; then
        # If we need to restart the service after the upgrade
        #  is finished, we will touch a temp file so that
        #  we can detect that state
        touch /usr/share/puppetdb/start_service_after_upgrade
        /sbin/service %{name} stop >/dev/null 2>&1
      fi
    fi
%else
    if /sbin/service %{name} status > /dev/null ; then
        # If we need to restart the service after the upgrade
        #  is finished, we will touch a temp file so that
        #  we can detect that state
        touch /usr/share/puppetdb/start_service_after_upgrade
        /sbin/service %{name} stop >/dev/null 2>&1
    fi
%endif
fi
# Add PuppetDB user
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
useradd -r -g %{name} -d /usr/share/puppetdb -s /sbin/nologin \
     -c "PuppetDB daemon"  %{name}

%post
%if 0%{?_with_systemd}
# Always reload the .service files if using systemd, in case they have changed.
/usr/bin/systemctl daemon-reload
%else
# If this is an install (as opposed to an upgrade)...
if [ "$1" = "1" ]; then
  # Register the puppetDB service
  /sbin/chkconfig --add %{name}
fi
%endif

/usr/sbin/puppetdb ssl-setup

chmod 755 /etc/puppetdb
chown -R puppetdb:puppetdb /etc/puppetdb/*
chmod -R 640 /etc/puppetdb/*
chmod -R ug+X /etc/puppetdb/*

chgrp puppetdb /var/log/puppetdb
chmod 775 /var/log/puppetdb

chown -R puppetdb:puppetdb /var/lib/puppetdb



%preun
# If this is an uninstall (as opposed to an upgrade) then
#  we want to shut down and disable the service.
if [ "$1" = "0" ] ; then
%if 0%{?_with_systemd}
    /usr/bin/systemctl stop %{name}.service
    /usr/bin/systemctl disable %{name}.service
%else
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
%endif
fi

%postun
# Remove the rundir if this is an uninstall (as opposed to an upgrade)...
if [ "$1" = "0" ]; then
    rm -rf %{_rundir}/%{name} || :
%if 0%{?_with_systemd}
    # Restart systemd after the service file is removed
    /usr/bin/systemctl daemon-reload
%endif
fi

# If this is an upgrade (as opposed to an install) then we need to check
#  and see if we stopped the service during the install (we indicate
#  this via the existence of a temp file that was created during that
#  phase).  If we did, then we need to restart it.
if [ "$1" = "1" ] ; then
    if [ -f "/usr/share/puppetdb/start_service_after_upgrade" ] ; then
        rm /usr/share/puppetdb/start_service_after_upgrade
%if 0%{?_with_systemd}
        /usr/bin/systemctl start %{name}.service >/dev/null 2>&1
%else
        /sbin/service %{name} start >/dev/null 2>&1
%endif
    fi
fi


%files
%defattr(-, root, root)
%doc *.md
%doc documentation
%if 0%{?suse_version}
%dir %{_sysconfdir}/%{realname}
%dir %{_sysconfdir}/%{realname}/conf.d
%endif
%config(noreplace)%{_sysconfdir}/%{realname}/conf.d/config.ini
%config(noreplace)%{_sysconfdir}/%{realname}/logback.xml
%config(noreplace)%{_sysconfdir}/%{realname}/conf.d/database.ini
%config(noreplace)%{_sysconfdir}/%{realname}/conf.d/jetty.ini
%config(noreplace)%{_sysconfdir}/%{realname}/conf.d/repl.ini
%config(noreplace)%{_realsysconfdir}/logrotate.d/%{name}
%config(noreplace)%{_realsysconfdir}/sysconfig/%{name}
%if 0%{?_with_systemd}
%{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif
%{_sbindir}/puppetdb-ssl-setup
%{_sbindir}/puppetdb-foreground
%{_sbindir}/puppetdb-import
%{_sbindir}/puppetdb-export
%{_sbindir}/puppetdb-anonymize
%{_sbindir}/puppetdb
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{realname}/puppetdb-ssl-setup
%{_libexecdir}/%{realname}/puppetdb-foreground
%{_libexecdir}/%{realname}/puppetdb-import
%{_libexecdir}/%{realname}/puppetdb-export
%{_libexecdir}/%{realname}/puppetdb-anonymize
%{_libexecdir}/%{realname}/%{name}.env
%{_datadir}/%{realname}
%{_sharedstatedir}/%{realname}
%{_datadir}/%{realname}/state
%dir %{_localstatedir}/log/%{name}
%ghost %{_localstatedir}/log/%{name}/%{name}.log
%ghost %{_rundir}/%{name}


%files terminus
%defattr(-, root, root)
%{puppet_libdir}/puppet/application/storeconfigs.rb
%{puppet_libdir}/puppet/face/node/deactivate.rb
%{puppet_libdir}/puppet/face/node/status.rb
%{puppet_libdir}/puppet/face/storeconfigs.rb
%{puppet_libdir}/puppet/indirector/catalog/puppetdb.rb
%{puppet_libdir}/puppet/indirector/facts/puppetdb.rb
%{puppet_libdir}/puppet/indirector/facts/puppetdb_apply.rb
%{puppet_libdir}/puppet/indirector/node/puppetdb.rb
%{puppet_libdir}/puppet/indirector/resource/puppetdb.rb
%{puppet_libdir}/puppet/reports/puppetdb.rb
%{puppet_libdir}/puppet/util/puppetdb.rb
%{puppet_libdir}/puppet/util/puppetdb/char_encoding.rb
%{puppet_libdir}/puppet/util/puppetdb/command.rb
%{puppet_libdir}/puppet/util/puppetdb/command_names.rb
%{puppet_libdir}/puppet/util/puppetdb/config.rb
%{puppet_libdir}/puppet/util/puppetdb/blacklist.rb
%{puppet_4_libdir}/puppet/application/storeconfigs.rb
%{puppet_4_libdir}/puppet/face/node/deactivate.rb
%{puppet_4_libdir}/puppet/face/node/status.rb
%{puppet_4_libdir}/puppet/face/storeconfigs.rb
%{puppet_4_libdir}/puppet/indirector/catalog/puppetdb.rb
%{puppet_4_libdir}/puppet/indirector/facts/puppetdb.rb
%{puppet_4_libdir}/puppet/indirector/facts/puppetdb_apply.rb
%{puppet_4_libdir}/puppet/indirector/node/puppetdb.rb
%{puppet_4_libdir}/puppet/indirector/resource/puppetdb.rb
%{puppet_4_libdir}/puppet/reports/puppetdb.rb
%{puppet_4_libdir}/puppet/util/puppetdb.rb
%{puppet_4_libdir}/puppet/util/puppetdb/char_encoding.rb
%{puppet_4_libdir}/puppet/util/puppetdb/command.rb
%{puppet_4_libdir}/puppet/util/puppetdb/command_names.rb
%{puppet_4_libdir}/puppet/util/puppetdb/config.rb
%{puppet_4_libdir}/puppet/util/puppetdb/blacklist.rb


%changelog
* Thu Mar 19 2015 jenkins <jenkins@grand> - 2.3.0-1
- Autobuild from Rake task

* Mon Apr 02 2012 Michael Stahnke <stahnma@puppetlabs.com> - 0.1.0-1
- Initial Packaging
