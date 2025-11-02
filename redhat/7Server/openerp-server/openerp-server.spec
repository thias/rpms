%define __python /usr/bin/python2

Name:      openerp-server
Version:   6.0.4
Release:   2%{?dist}
License:   AGPLv3 and GPLv2 and LGPLv2+ and MIT
Group:     System Environment/Daemons
Summary:   OpenERP Server
URL:       https://www.odoo.com/
Source0:   https://nightly.odoo.com/old/openerp-6.0/%{version}/openerp-server-%{version}.tar.gz
Source1:   openerp-server.service
Patch0:    openerp-server-6.0.4-logrotate.patch
Patch1:    openerp-server-6.0.4-qr-encode-fix.patch
BuildArch:      noarch
BuildRequires:  python
BuildRequires:  python-setuptools
BuildRequires:  pygtk2-devel, libxslt-python
BuildRequires:  python2-devel
BuildRequires:  jpackage-utils
Requires:       python-lxml
Requires:       python-imaging
Requires:       python-psycopg2, python-reportlab
Requires:       pyparsing
Requires:       ghostscript
Requires:       pytz
Requires:       PyXML
# Requires: python-matplotlib
Requires:       PyYAML, python-mako
Requires:       pychart
BuildRequires: systemd
%{?systemd_requires}

%description
Server package for OpenERP.

OpenERP is a free Enterprise Resource Planning and Customer Relationship 
Management software. It is mainly developed to meet changing needs.

The main functional features are: CRM & SRM, analytic and financial accounting,
double-entry stock management, sales and purchases management, tasks automation,
help desk, marketing campaign, ... and vertical modules for very specific
businesses.

Technical features include a distributed server, flexible workflows, an object 
database, dynamic GUIs, custom reports, NET-RPC and XML-RPC interfaces, ...

For more information, please visit:
http://www.openerp.com/

This server package contains the core (server) of OpenERP system and all
addons of the official distribution. You may need the GTK client to connect
to this server, or the web-client, which serves to HTML browsers. You can
also find more addons (aka. modules) for this ERP system in:
    http://www.openerp.com/
or  http://apps.openerp.com/


%prep
%setup -q
%patch -P 0 -p1 -b .logrotate
%patch -P 1 -p1 -b .qr-encode-fix


%build
NO_INSTALL_REQS=1 python setup.py build --quiet


%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot}
# the Python installer plants the RPM_BUILD_ROOT inside the launch script
sed -i "s|%{buildroot}||" %{buildroot}%{_bindir}/openerp-server

# When setup.py copies files, it removes the executable bit, so we have to
# restore it here for some scripts:
pushd %{buildroot}%{python_sitelib}/%{name}
  chmod a+x addons/document_ftp/ftpserver/ftpserver.py \
    addons/document/odt2txt.py \
    addons/document/test_cindex.py \
    addons/document_webdav/test_davclient.py \
    addons/email_template/html2text.py \
    addons/mail_gateway/scripts/openerp_mailgate/openerp_mailgate.py \
    openerp-server.py \
    report/render/rml2txt/rml2txt.py \
    tools/graph.py \
    tools/which.py
popd

# Install the conf
install -m 0644 -D doc/openerp-server.conf \
  %{buildroot}/etc/openerp-server.conf
install -m 0644 -D doc/openerp-server.logrotate \
  %{buildroot}/etc/logrotate.d/openerp-server

# Create systemd unit file
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/openerp-server.service

mkdir -p %{buildroot}/var/log/openerp
mkdir -p %{buildroot}/var/lib/openerp


%clean
rm -rf %{buildroot}


%pre
/usr/sbin/useradd -c "OpenERP Server" \
  -s /sbin/nologin -r -d /var/lib/openerp openerp 2>/dev/null || :

%post
%systemd_post openerp-server.service

%preun
%systemd_preun openerp-server.service

%postun
%systemd_postun_with_restart openerp-server.service


%files
%defattr(-,root,root)
%doc LICENSE README doc/INSTALL doc/Changelog
%attr(0775,openerp,openerp) %dir /var/log/openerp
%attr(0775,openerp,openerp) %dir /var/lib/openerp
%attr(0640,root,openerp) %config(noreplace) /etc/openerp-server.conf
%config(noreplace) /etc/logrotate.d/openerp-server
%{_bindir}/openerp-server
%{_unitdir}/openerp-server.service
%{python_sitelib}/openerp-server/
%{python_sitelib}/openerp_server-%{version}-py%{python_version}.egg-info
%{_mandir}/man1/openerp-server.*
%{_mandir}/man5/openerp_serverrc.5*


%changelog
* Sun Nov  2 2025 Matthias Saou <matthias@saou.eu> 6.0.4-2
- Fix QR code character encoding.

* Mon Jun 28 2021 Matthias Saou <matthias@saou.eu> 6.0.4-1
- Fix logrotate by adding missing "su" directive.

* Fri Jun 18 2021 Matthias Saou <matthias@saou.eu> 6.0.4-0
- Update to 6.0.4.
- Rip out all patches.
- Simplify spec file to the max.
- Switch to systemd.

* Wed Sep 28 2011 Matthias Saou <matthias@saou.eu> 6.0.3-0
- Update to 6.0.3 final.
- Spec file cleanups from the Fedora package review (#693425).

* Thu Apr 21 2011 P. Christeas <p_christ@hol.gr> 6.0.2-5
  + Redhat: split the spec into server and client ones
  + Redhat: a few more fixes, to reduce lint errors
  + Merge branch 'official' into xrg-60
  + scripts: generate archives2, like the upstream tarballs
  + server: update for RPM builds
  + Merge remote-tracking branch 'origin/xrg-60' into HEAD
  + Updated addons, client, client-web and server, to latest official-6.0

* Tue Apr 12 2011 P. Christeas <p_christ@hol.gr> 39d1e18
  + mandriva: pull changes from redhat spec, consider mageia

* Mon Apr 11 2011 P. Christeas <p_christ@hol.gr> 4d83114
  + Updated submodules addons, client, server
  + Redhat: remove double-listed requires
  + Redhat: remove embedded pychart, use upstream one

* Sun Apr 10 2011 P. Christeas <p_christ@hol.gr> e3c96ef
  + Redhat: cleanup the %doc files
  + Redhat: remove support for intermediate builds
  + Redhat: remove web-client support
  + Redhat: a few improvements, try to build the web-client

* Sat Apr 9 2011 P. Christeas <p_christ@hol.gr> 0037772
  + Redhat: more cleanup, offer default docs
  + Redhat: remove the kde client
  + Redhat: remove the serverinit sub-package
  + Redhat: cleanup macros, requires
  + Redhat: python build --quiet

* Fri Apr 8 2011 P. Christeas <p_christ@hol.gr> e7eab62
  + Radhat: 6.0.2-2 fix groups, cert script, changelog
  + Mandriva: a few changes in .spec file

* Mon Apr 4 2011 P. Christeas <p_christ@hol.gr> b4c22fc
  + redhat: update to 6.0.2
  + redhat: a couple of fixes for rpmlint
  + redhat: improvements at .spec to comply with Guidelines

* Sun Apr 3 2011 P. Christeas <p_christ@hol.gr> 45596e1
  + redhat: bring the server-check.sh and a patch for init.d
  + RedHat: cleanup the .spec file, fix dependencies

* Sat Apr 2 2011 P. Christeas <p_christ@hol.gr> 3a88941
  + mandriva: demote the class, again, to public

* Fri Apr 1 2011 P. Christeas <p_christ@hol.gr> 7d8252a
  + Mandriva: add some dependencies to .spec file
  + Update to 6.0.2+
  + Redhat spec: strip much of the mandriva logic, make it static
  + RPM: copy spec file from Mandriva/Mageia to RedHat

* Thu Mar 24 2011 P. Christeas <p_christ@hol.gr> b9154b0
  + Initialize submodule for 'libcli', the client library

* Mon Mar 21 2011 P. Christeas <p_christ@hol.gr> 469aa48
  + Remove tests/ , they are in the sandbox now.

* Sun Mar 20 2011 P. Christeas <p_christ@hol.gr> 067bf38
  + Add README about this repository

* Thu Mar 17 2011 P. Christeas <p_christ@hol.gr> 968601a
  + Rewrite last gtk-client patch for SpiffGtkWidgets setup
  + mandriva: require python-lxml for gtk client
  + Updated submodules addons, buildbot, client, client-kde, server
  + tests: one for mails, one to dump the doc nodes cache
  + git: Fix submodule URL of buildbot

* Wed Mar 9 2011 P. Christeas <p_christ@hol.gr> fed8f66
  + Updated submodules addons, client, client-kde, extra-addons, server

* Wed Feb 23 2011 P. Christeas <p_christ@hol.gr> 9beefb7
  + Updated submodules addons, client, client-kde, extra-addons, server

* Sat Feb 19 2011 P. Christeas <p_christ@hol.gr> 23f26ca
  + Updated submodules addons, buildbot, client, client-kde, client-web, extra-addons, server

* Fri Jan 21 2011 P. Christeas <p_christ@hol.gr> a1e11b1
  + Merge branch 'official' into xrg-60
  + RPM spec: adapt to official release, dirs have the right names now.

* Thu Jan 20 2011 P. Christeas <xrg@openerp.com> 939c332
  + Official Release 6.0.1 + debian changelogs

* Thu Jan 20 2011 P. Christeas <p_christ@hol.gr> 536461f
  + Merge release 6.0.1

* Wed Jan 19 2011 P. Christeas <p_christ@hol.gr> 4635463
  + Merge commit 'v6.0.0' into xrg-60
  + Merge 6.0.0 into xrg-60
  + Updated submodules addons, client, server
  + Release 6.0.0
  + RPM spec: have all-modules list, skip bad addons, skip server-check.sh
  + RPM: allow modulize.py to skip bad modules.
  + Reset submodules addons, client*, addons, server to official
  + Mandriva: let spec go closer to other RPM distros
  + Updated submodules addons, client, client-kde, client-web, extra-addons, server

* Sat Jan 15 2011 P. Christeas <p_christ@hol.gr> 7486fe9
  + Updated submodules addons, client, client-kde, client-web, server

* Thu Jan 13 2011 P. Christeas <p_christ@hol.gr> a9b50da
  + Updated submodule client, using improved installer

* Mon Jan 3 2011 P. Christeas <p_christ@hol.gr> bd6aa12
  + Version 6.0.0-rc2 with addons, client, client-web, server

* Sun Jan 2 2011 P. Christeas <p_christ@hol.gr> 7266984
  + Further attempt for a correct client-web installation.
  + client-web: fix installation, under "site-packages/openobject/"

