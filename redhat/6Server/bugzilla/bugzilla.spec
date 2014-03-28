%define bzinstallprefix %{_datadir}
%define bzdatadir %{_localstatedir}/lib/bugzilla

Summary: Bug tracking system
URL: http://www.bugzilla.org/
Name: bugzilla
Version: 4.0.11
Group: Applications/Publishing
Release: 1%{?dist}
License: MPLv1.1
Source0: http://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-%{version}.tar.gz
Source1: bugzilla-httpd-conf
Source2: README.fedora.bugzilla
Source3: bugzilla.cron-daily
Patch0: bugzilla-rw-paths.patch
Patch1: bugzilla-yum.patch

BuildArch: noarch
Requires: webserver, patchutils, perl(SOAP::Lite), which
Requires: perl(CGI) >= 3.51
Requires: perl(Digest::SHA)
Requires: perl(Date::Format) >= 2.21
Requires: perl(DateTime) >= 0.28
Requires: perl(DateTime::TimeZone) >= 0.71
Requires: perl(DBI) >= 1.41
Requires: perl(Template) >= 2.22
Requires: perl(Email::Send) >= 2.00
Requires: perl(Email::MIME) >= 1.904
Requires: perl(URI)
Requires: perl(List::MoreUtils) >= 0.22
Requires: perl(Locale::Language)

%package doc
Summary: Bugzilla documentation
Group: Documentation

%package doc-build
Summary: Tools to generate the Bugzilla documentation
Group: Applications/Publishing

%package contrib
Summary: Bugzilla contributed scripts
Group: Applications/Publishing
BuildRequires: python

%description
Bugzilla is a popular bug tracking system used by multiple open source projects
It requires a database engine installed - either MySQL, PostgreSQL or Oracle.
Without one of these database engines (local or remote), Bugzilla will not work
- see the Release Notes for details.

%description doc
Documentation distributed with the Bugzilla bug tracking system

%description doc-build
Tools to generate the documentation distributed with Bugzilla

%description contrib
Contributed scripts and functions for Bugzilla

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
rm -f Bugzilla/Constants.pm.orig
rm -f Bugzilla/Install/Requirements.pm.orig
# Remove bundled libs
rm -rf lib/CGI*

# Filter unwanted Requires found by /usr/lib/rpm/perldeps.pl:
# create a wrapper script which runs the original perl_requires
# command and strips some of the output
cat << \EOF > .%{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(sanitycheck.cgi)/d;/perl(Apache2::/d;/perl(ModPerl::/d;/perl(Authen::Radius)/d;/perl(Net::LDAP)/d;/perl(DBD::Oracle)/d;/perl(DBD::Pg)/d;/perl(DBI::db)/d;/perl(DBI::st)/d;/perl(Email::MIME::Attachment::Stripper)/d;/perl(Email::Reply)/d;/perl(MIME::Parser)/d;/perl(XML::Twig)/d;/perl(XMLRPC::/d;/perl(HTTP::Message)/d;/perl(Test::Taint)/d;/perl(Image::Magick)/d'
EOF

# use that wrapper script instead of the original perl_requires script
%define __perl_requires %{_builddir}/%{name}-%{version}/.%{name}-req
chmod +x %{__perl_requires}

# TODO: Remove from provides : 
# /perl(Bugzilla::Extension::/d;

# Deal with changing /usr/local paths here instead of via patches
%{__perl} -pi -e 's|/usr/local/bin/python\b|%{__python}|' contrib/*.py
%{__perl} -pi -e 's|/usr/local/bin/ruby\b|%{_bindir}/ruby|' contrib/*.rb
grep -rl '/usr/lib/sendmail\b' contrib docs \
| xargs %{__perl} -pi -e 's|/usr/lib/sendmail\b|%{_sbindir}/sendmail|'

%build
find . -depth -name CVS -type d -exec rm -rf {} \;
find . -depth -name .cvsignore -type f -exec rm -rf {} \;
# Remove the execute bit from files that don't start with #!
for file in `find -type f -perm /111`; do
  if head -1 $file | grep -E -v '^\#!' &>/dev/null; then
    chmod a-x $file
  fi
done
# Ensure shebang shell scripts have executable bit set
for file in `find -type f -perm /664`; do
  if head -1 $file | grep -E '^\#!' &>/dev/null; then
    chmod a+x $file
  fi
done


%install
mkdir -p ${RPM_BUILD_ROOT}/%{bzinstallprefix}/bugzilla
cp -pr * ${RPM_BUILD_ROOT}/%{bzinstallprefix}/bugzilla
echo "0-59/15 * * * * apache cd %{bzinstallprefix}/bugzilla && env LANG=C %{bzinstallprefix}/bugzilla/whine.pl" > ${RPM_BUILD_ROOT}/%{bzinstallprefix}/bugzilla/cron.whine
rm -f ${RPM_BUILD_ROOT}/%{bzinstallprefix}/bugzilla/{README,UPGRADING,UPGRADING-pre-2.8}
mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/doc/%{name}-%{version}
cp %{SOURCE2} ./README.fedora
mkdir -p ${RPM_BUILD_ROOT}/%{bzdatadir}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/bugzilla
install -m 0644 -D -p %{SOURCE1}  ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/bugzilla.conf
install -m 0755 -D -p %{SOURCE3}  ${RPM_BUILD_ROOT}%{bzinstallprefix}/bugzilla/cron.daily

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
(pushd %{bzinstallprefix}/bugzilla > /dev/null
[ -f /etc/bugzilla/localconfig ] || ./checksetup.pl > /dev/null
popd > /dev/null)

%files
%defattr(-,root,root,-)
%dir %{bzinstallprefix}/bugzilla
%{bzinstallprefix}/bugzilla/*.cgi
%{bzinstallprefix}/bugzilla/*.pl
%{bzinstallprefix}/bugzilla/Bugzilla.pm
%{bzinstallprefix}/bugzilla/bugzilla.dtd
%{bzinstallprefix}/bugzilla/robots.txt
%{bzinstallprefix}/bugzilla/Bugzilla
%{bzinstallprefix}/bugzilla/extensions
%{bzinstallprefix}/bugzilla/images
%{bzinstallprefix}/bugzilla/js
%{bzinstallprefix}/bugzilla/lib
%{bzinstallprefix}/bugzilla/skins
%{bzinstallprefix}/bugzilla/t
%{bzinstallprefix}/bugzilla/xt
%{bzinstallprefix}/bugzilla/template
%{bzinstallprefix}/bugzilla/cron.daily
%{bzinstallprefix}/bugzilla/cron.whine
%{bzinstallprefix}/bugzilla/contrib/recode.pl
%config(noreplace) %{_sysconfdir}/httpd/conf.d/bugzilla.conf
%defattr(-,root,root,-)
%doc README
%doc README.fedora
%dir %{bzdatadir}
%defattr(0750,root,apache,-)
%dir %{_sysconfdir}/bugzilla

%files doc
%defattr(-,root,root,-)
%{bzinstallprefix}/bugzilla/docs/en
%{bzinstallprefix}/bugzilla/docs/bugzilla.ent
%{bzinstallprefix}/bugzilla/docs/style.css

%files doc-build
%defattr(-,root,root,-)
%{bzinstallprefix}/bugzilla/docs/makedocs.pl
%{bzinstallprefix}/bugzilla/docs/lib

%files contrib
%defattr(-,root,root,-)
%{bzinstallprefix}/bugzilla/contrib/bugzilla_ldapsync.rb
%{bzinstallprefix}/bugzilla/contrib/bugzilla-queue.rhel
%{bzinstallprefix}/bugzilla/contrib/bugzilla-queue.suse
%{bzinstallprefix}/bugzilla/contrib/bugzilla-submit
%{bzinstallprefix}/bugzilla/contrib/bzdbcopy.pl
%{bzinstallprefix}/bugzilla/contrib/bz_webservice_demo.pl
%{bzinstallprefix}/bugzilla/contrib/cmdline
%{bzinstallprefix}/bugzilla/contrib/console.pl
%{bzinstallprefix}/bugzilla/contrib/convert-workflow.pl
%{bzinstallprefix}/bugzilla/contrib/cvs-update.pl
%{bzinstallprefix}/bugzilla/contrib/extension-convert.pl
%{bzinstallprefix}/bugzilla/contrib/fixperms.pl
%{bzinstallprefix}/bugzilla/contrib/jb2bz.py*
%{bzinstallprefix}/bugzilla/contrib/merge-users.pl
%{bzinstallprefix}/bugzilla/contrib/mysqld-watcher.pl
%{bzinstallprefix}/bugzilla/contrib/new-yui.sh
%{bzinstallprefix}/bugzilla/contrib/README
%{bzinstallprefix}/bugzilla/contrib/sendbugmail.pl
%{bzinstallprefix}/bugzilla/contrib/sendunsentbugmail.pl
%{bzinstallprefix}/bugzilla/contrib/syncLDAP.pl
%{bzinstallprefix}/bugzilla/contrib/yp_nomail.sh

%changelog
* Fri Mar 28 2014 Matthias Saou <matthias@saou.eu> 4.0.11-1
- Update to 4.0.11.

* Sat Nov  3 2012 Matthias Saou <matthias@saou.eu> 4.0.8-1
- Update to 4.0.8.

* Fri May  4 2012 Matthias Saou <matthias@saou.eu> 4.0.6-1
- Update to 4.0.6, rebase on Emmanuel Seyman's latest Fedora 4.0.x package.

* Mon Feb 27 2012 Matthias Saou <matthias@saou.eu> 4.0.5-1
- Update to 4.0.5.

* Tue Feb  7 2012 Matthias Saou <matthias@saou.eu> 4.0.4-1
- Change req deps back to script override.
- Rebuild for EL6.

* Wed Feb  1 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 4.0.4-1
- Update to 4.0.4 to fix security flaws (#786550)
- Remove JSON:RPC patch, upstreamed (bmo #706753)
- Correct upstream URL in README.fedora.bugzilla, thanks to Ken Dreyer (#783014)

* Tue Jan 10 2012 Tom Callaway <spot@fedoraproject.org> - 4.0.3-2
- patch bz to use JSON::RPC::Legacy::Server::CGI

* Fri Dec 30 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 4.0.3-1
- Update to 4.0.3
- Add perl(Locale::Language) to the Requires
- Put the xml docs source in the doc-build subpackage
- Add index.html to the DirectoryIndex
- Fix typo in README.fedora.bugzilla

* Fri Aug 05 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 4.0.2-1
- Update to 4.0.2
- Add RPM-4.9-style filtering
- Put graphs in /var/lib/bugzilla/graphs.

* Sun May 01 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 4.0.1-1
- Update to 4.0.1
- Patch the installation procedure to recommend yum

* Sun Mar 27 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 4.0-1
- Update to 4.0

* Sun Mar 06 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-7
- Put contrib/recode.pl in the main package so that it no longer depends on
  python and ruby
- Remove the contents of the lib/ directory, not the directory itself.

* Tue Feb 15 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-6
- More filtering

* Mon Feb 14 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-5
- Fix broken dependencies
- Remove unused patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-3
- Remove no-longer-needed files

* Sat Jan 29 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-2
- Move to the current filtering system for provides and requires

* Tue Jan 25 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.4-1
- Update to 3.6.4
- Add RPM-4.9-style filtering
- 

* Wed Nov 03 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.3-1
- Update to 3.6.3 (#649406)
- Fix webdot alias in /etc/httpd/conf.d/bugzilla (#630255)
- Do not apply graphs patch (upstreamed)

* Wed Aug 18 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.2-1
- Update to 3.6.2 (#623426)
- Only run checksetup if /etc/bugzilla/localconfig does not exist (#610210)
- Add bugzilla-contrib to Requires (#610198)

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.6.1-2
- recompiling .py files against Python 2.7 (rhbz#623281)

* Fri Jun 25 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6.1-1
- Update to 3.6.1

* Sun Jun  6 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6-3
- Remove mod_perl from the requirements (#600924)

* Sun Jun  6 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6-2
- Fix missing provides (#600922)

* Tue Apr 13 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.6-1
- Update to 3.6 (#598377)
- Patch to put graphs in /var/lib/bugzilla/ (brc #564450, bmo #313739)

* Mon Feb 01 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4.5-1
- Update to 3.4.5 (CVE-2009-3989, CVE-2009-3387)
- Remove bugzilla-EL5-perl-versions.patch which is EPEL-specific

* Thu Nov 19 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4.4-1
- Update to 3.4.4 (CVE-2009-3386)

* Wed Nov 11 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4.3-1
- Update to 3.4.3 (fixes memory leak issues)
- Add perl(Digest::SHA) in the Requires
- Specify Perl module versions in the Requires (fixes #524309)
- Add an alias to make $webdotdir a working path (fixes #458848)

* Fri Sep 11 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4.2-1
- Update to 3.4.2 (CVE-2009-3125, CVE-2009-3165 and CVE-2009-3166)

* Tue Aug 04 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 3.4.1-2
- fix EL-5 perl dependencies bz#515158

* Sun Aug 02 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4.1-1
- Update to 3.4.1, fixing a security leak

* Wed Jul 29 2009 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 3.4-1
- Update to 3.4 (fixes #514315)
- move makedocs.pl to its own package (fixes #509041)
- move the extensions dir to /usr/share/ (fixes #450636)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 3.2.4-1
- fix https://bugzilla.mozilla.org/show_bug.cgi?id=495257

* Mon Apr 06 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 3.2.3-1
- fix CVE-2009-1213

* Thu Mar 05 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 3.2.2-2
- fix from BZ #474250 Comment #16, from Chris Eveleigh -->
- add python BR for contrib subpackage
- fix description
- change Requires perl-SOAP-Lite to perl(SOAP::Lite) according guidelines

* Sun Mar 01 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 3.2.2-1
- thanks to Chris Eveleigh <chris dot eveleigh at planningportal dot gov dot uk>
- for contributing with patches :-)
- Upgrade to upstream 3.2.2 to fix multiple security vulns
- Removed old perl_requires exclusions, added new ones for RADIUS, Oracle and sanitycheck.cgi
- Added Oracle to supported DBs in description (and moved line breaks)
- Include a patch to fix max_allowed_packet warnin when using with mysql

* Sat Feb 28 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 3.0.8-1
- Upgrade to 3.0.8, fix #466077 #438080
- fix macro in changelog rpmlint warning
- fix files-attr-not-set rpmlint warning for doc and contrib sub-packages

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Stepan Kasal <skasal@redhat.com> - 3.0.4-3
- do not require perl-Email-Simple, it is (no longer) in use
- remove several explicit perl-* requires; the automatic dependencies
  do handle them

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.4-2
- fix license tag

* Fri May  9 2008 John Berninger <john at ncphotography dot com> - 3.0.4-1
- Update to upstream 3.0.4 to fix multiple security vulns
- Change perms on /etc/bugzilla for bz 427981

* Sun May  4 2008 John Berninger <john at ncphotography dot com> - 3.0.3-0
- Update to upstream 3.0.3 - bz 444669

* Fri Dec 28 2007 John Berninger <john at ncphotography dot com> - 3.0.2-6
- Add cron.daily, cron.whine to payload list

* Fri Dec 28 2007 John Berninger <john at ncphotography dot com> - 3.0.2-5
- Typo in spec file, rebuild

* Fri Dec 28 2007 John Berninger <john at ncphotography dot com> - 3.0.2-3
- bz 426465 - don't enable cron jobs so cron doesn't complain about
  an unconfigured installation

* Fri Oct 26 2007 John Berninger <john at ncphotography dot com> - 3.0.2-2
- fix issue with AlowOverride Options

* Mon Oct 22 2007 John Berninger <john at ncphotography dot com> - 3.0.2-1
- updates to requires and httpd conf for BZ's 279961, 295861, 339531

* Mon Sep 24 2007 John Berninger <john at ncphotography dot com> - 3.0.2-0
- update to 3.0.2 - bz 299981

* Mon Aug 27 2007 John Berninger <john at ncphotography dot com> - 3.0.1-0
- update to 3.0.1 - bz 256021

* Fri May 18 2007 John Berninger <jwb at redhat dot com> - 3.0-2
- update Requires for bz's 241037, 241206

* Fri May 18 2007 John Berninger <jwb at redhat dot com> - 3.0-1
- update to upstream version 3.0
- add new dependencies on mod_perl, perl-SOAP-Lite
- refactor patch(es) to change paths for read-only /usr

* Tue Feb 20 2007 John Berninger <jwb at redhat dot com> - 2.22.2-1
- update to 2.22.2 - bz 229163

* Wed Feb 14 2007 John Berninger <jwb at redhat dot com> - 2.22-12
- More cron job fixes

* Wed Jan 31 2007 John Berninger <jwb at redhat dot com> - 2.22-11
- Fix cron job perms

* Sat Jan 27 2007 John Berninger <jwb at redhat dot com> - 2.22-10
- Fix collectstats cron job, bx 224550

* Mon Jan 22 2007 John Berninger <jwb at redhat dot com> - 2.22-9
- Fix linebreak issues in specfile

* Mon Jan 22 2007 John Berninger <jwb at redhat dot com> - 2.22-8
- Put daily and hourly cronjobs in place per bz 223747

* Wed Nov  8 2006 John Berninger <johnw at berningeronline dot net> - 2.22-7
- Fixes for bz # 212355

* Tue Jun 26 2006 John Berninger <johnw at berningeronline dot net> - 2.22-6
- Clean up BugzillaEmail requires (filter it out)

* Mon Jun 26 2006 John Berninger <johnw at berningeronline dot net> - 2.22-5
- License is MPL, not GPL
- Clean up %%doc specs

* Sun Jun 25 2006 John Benringer <johnw at berningeronline dot net> - 2.22-4
- Remove localconfig file per upstream
- Patch to have localconfig appear in /etc/bugzilla when checksetup.pl is run

* Tue Jun 20 2006 John Berninger <johnw at berningeronline dot net> - 2.22-3
- Add README.fedora file
- Add additional requires per comments from upstream

* Mon Jun 19 2006 John Berninger <johnw at berningeronline dot net> - 2.22-2
- Code to /usr/share, data to /var/lib/bugzilla per FE packaging req's

* Tue Jun 13 2006 John Berninger <johnw at berningeronline dot net> - 2.22-1
- Shift to /var/lib/bugzilla install dir per discussion in review request
- Minor change in filtering requires

* Tue May 23 2006 John Berninger <johnw at berningeronline dot net> - 2.22-0
- Update to upstream 2.22 release
- Split off -contrib package, but keep it where it usually gets installed

* Wed Apr 26 2006 John Berninger <johnw at berningeronline dot net> - 2.20.1-4
- rpmlint cleanups

* Mon Apr 24 2006 John Berninger <johnw at berningeronline dot net> - 2.20.1-3
- Cleanup of prov/req filters
- Split docs into -doc package

* Thu Apr 20 2006 John Berninger <johnw at berningeronline dot net> - 2.20.1-2
- No need for CVS tarball - I was thinking things too far through.  Change
  to 2.20.1 release.

* Fri Apr  7 2006 John Berninger <johnw at berningeronline dot net> - 2.20-0.1cvs20060407
- Initial spec creation/build for Fedora Extras packaging.

