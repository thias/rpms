Summary: Neighbor Proxy Daemon for IPv6
Name: npd6
Version: 1.1.0
Release: 1%{?dist}
License: GPLv3+
Group: System Environment/Daemons
URL: http://npd6.github.io/npd6/
Source0: https://github.com/npd6/npd6/archive/%{version}.tar.gz
Source1: npd6.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
A daemon to provide a proxy service for IPv6 Neighbor Solicitations received
by a gateway routing device. 


%prep
%setup -q


%build
# The -c is required or the build fails, taken from the Makefile
make %{?_smp_mflags} CFLAGS="-c %{optflags}" 


%install
rm -rf %{buildroot}
make install INSTALL_PREFIX=%{_prefix} DESTDIR=%{buildroot}
# Put the sample entirely into place
mv %{buildroot}%{_sysconfdir}/npd6.conf.sample \
   %{buildroot}%{_sysconfdir}/npd6.conf
# Replace the Debian init script with our own
install -p -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/npd6


%clean
rm -rf %{buildroot}


%post
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add npd6
fi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service npd6 stop &>/dev/null || :
    /sbin/chkconfig --del npd6
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service npd6 condrestart &>/dev/null || :
fi


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/npd6.conf
%attr(0755,root,root) %{_sysconfdir}/init.d/npd6
%{_bindir}/npd6
%{_mandir}/man5/npd6.conf.5*
%{_mandir}/man8/npd6.8*


%changelog
* Tue Jul 14 2015 Matthias Saou <matthias@saou.eu> 1.1.0-1
- Update to 1.1.0.

* Tue Jul 17 2012 Matthias Saou <matthias@saou.eu> 0.4.6-1
- Initial RPM release.

