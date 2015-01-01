# Regarding brew / rhpkg build:
# This is a noarch package, providing static data and cross platform scripts,
# intended for all platforms. However, it includes data in a Java compatible
# file format. The required "keytool" for building the Java compatible data
# is available on the i686 and x86_64 arches, only.
# As a result, it's necessary to use a compatible build host.
# Unfortunately, I haven't found a way to enforce the build host.
# ExcludeArch/ExclusiveArch doesn't work.
# You must repeat rhpkg build until the build gets randomly assigned to a 
# compatible build host.

%define pkidir %{_sysconfdir}/pki
%define catrustdir %{_sysconfdir}/pki/ca-trust
%define classic_tls_bundle ca-bundle.crt
%define trusted_all_bundle ca-bundle.trust.crt
%define neutral_bundle ca-bundle.neutral-trust.crt
%define bundle_supplement ca-bundle.supplement.p11-kit
%define java_bundle java/cacerts

Summary: The Mozilla CA root certificate bundle
Name: ca-certificates

# For the package version number, we use: year.{upstream version}
#
# The {upstream version} can be found as symbol NSS_BUILTINS_LIBRARY_VERSION at
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/nssckbi.h
# which corresponds to
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/certdata.txt
# (these revisions are the tip of development and might be unreleased).
# For the latest release used in RTM versions of Mozilla Firefox, check:
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/nssckbi.h
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt
#
# (until 2012.87 the version was based on the cvs revision ID of certdata.txt,
# but in 2013 the NSS projected was migrated to HG. Old version 2012.87 is 
# equivalent to new version 2012.1.93, which would break the requirement 
# to have increasing version numbers. However, the new scheme will work, 
# because all future versions will start with 2013 or larger.)

Version: 2013.1.95
# On RHEL 6.x, please keep the release version < 70, suggested 65.x
Release: 65.1%{?dist}
License: Public Domain

Group: System Environment/Base
URL: http://www.mozilla.org/

#Please always update both certdata.txt and nssckbi.h
Source0: certdata.txt
Source1: nssckbi.h
Source2: update-ca-trust
Source3: trust-fixes
Source4: certdata2pem.py
Source5: generate-cacerts.pl
Source10: update-ca-trust.8.txt
Source11: README.usr
Source12: README.etc
Source13: README.extr
Source14: README.java
Source15: README.openssl
Source16: README.pem
Source17: README.src

BuildArch: noarch

Requires: p11-kit >= 0.18.4-2
Requires: p11-kit-trust >= 0.18.4-2

BuildRequires: perl
BuildRequires: python
BuildRequires: openssl
BuildRequires: asciidoc
BuildRequires: libxslt

#for /usr/bin/keytool
BuildRequires: java-1.7.0-openjdk

%description
This package contains the set of CA certificates chosen by the
Mozilla Foundation for use with the Internet PKI.

%prep
rm -rf %{name}
mkdir %{name}
mkdir %{name}/certs
mkdir %{name}/java

%build
pushd %{name}/certs
 pwd
 cp %{SOURCE0} .
 python %{SOURCE4} >c2p.log 2>c2p.err
popd

pushd %{name}
 (
   cat <<EOF
# This is a bundle of X.509 certificates of public Certificate
# Authorities.  It was generated from the Mozilla root CA list.
#
# Source: nss/lib/ckfw/builtins/certdata.txt
# Source: nss/lib/ckfw/builtins/nssckbi.h
#
# Generated from:
EOF
   cat %{SOURCE1}  |grep -w NSS_BUILTINS_LIBRARY_VERSION | awk '{print "# " $2 " " $3}';
   echo '#';
 ) > %{classic_tls_bundle}

 (
   cat <<EOF
# This is a bundle of X.509 certificates of public Certificate
# Authorities.  It was generated from the Mozilla root CA list.
# These certificates are in the OpenSSL "TRUSTED CERTIFICATE"
# format and have trust bits set accordingly.
#
# Source: nss/lib/ckfw/builtins/certdata.txt
# Source: nss/lib/ckfw/builtins/nssckbi.h
#
# Generated from:
EOF
   cat %{SOURCE1}  |grep -w NSS_BUILTINS_LIBRARY_VERSION | awk '{print "# " $2 " " $3}';
   echo '#';
 ) > %{trusted_all_bundle}
 
 for f in certs/*.crt; do 
   echo "processing $f"
   tbits=`sed -n '/^# openssl-trust/{s/^.*=//;p;}' $f`
   distbits=`sed -n '/^# openssl-distrust/{s/^.*=//;p;}' $f`
   alias=`sed -n '/^# alias=/{s/^.*=//;p;q;}' $f | sed "s/'//g" | sed 's/"//g'`
   case $tbits in
     *serverAuth*) openssl x509 -text -in "$f" >> %{classic_tls_bundle} ;;
   esac
   targs=""
   if [ -n "$tbits" ]; then
      for t in $tbits; do
         targs="${targs} -addtrust $t"
      done
   fi
   if [ -n "$distbits" ]; then
      for t in $distbits; do
         targs="${targs} -addreject $t"
      done
   fi
   if [ -n "$targs" ]; then
      echo "trust flags $targs for $f" >> info.trust
      openssl x509 -text -in "$f" -trustout $targs -setalias "$alias" >> %{trusted_all_bundle}
   else
      echo "no trust flags for $f" >> info.notrust
      openssl x509 -text -in "$f" -setalias "$alias" >> %{neutral_bundle}
   fi
 done

 for p in certs/*.p11-kit; do 
   cat "$p" >> %{bundle_supplement}
 done

 # Append our trust fixes
 cat %{SOURCE3} >> %{bundle_supplement}
popd

pushd %{name}/java
 test -s ../%{classic_tls_bundle} || exit 1
 %{__perl} %{SOURCE5} %{_bindir}/keytool ../%{classic_tls_bundle}
 touch -r %{SOURCE0} cacerts
popd

#manpage
cp %{SOURCE10} %{name}/update-ca-trust.8.txt
asciidoc.py -v -d manpage -b docbook %{name}/update-ca-trust.8.txt
xsltproc --nonet -o %{name}/update-ca-trust.8 /usr/share/asciidoc/docbook-xsl/manpage.xsl %{name}/update-ca-trust.8.xml


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -p -m 644 %{name}/update-ca-trust.8 ${RPM_BUILD_ROOT}%{_mandir}/man8

#### traditional, old-style
mkdir -p $RPM_BUILD_ROOT%{pkidir}/tls/certs
install -p -m 644 %{name}/%{classic_tls_bundle} $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{classic_tls_bundle}
install -p -m 644 %{name}/%{trusted_all_bundle} $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{trusted_all_bundle}

ln -s certs/%{classic_tls_bundle} $RPM_BUILD_ROOT%{pkidir}/tls/cert.pem
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{classic_tls_bundle}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{pkidir}/tls/certs/%{trusted_all_bundle}

# Install Java cacerts file.
mkdir -p -m 755 $RPM_BUILD_ROOT%{pkidir}/java
install -p -m 644 %{name}/%{java_bundle} $RPM_BUILD_ROOT%{pkidir}/java/

# /etc/ssl/certs symlink for 3rd-party tools
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl
ln -s ../pki/tls/certs $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs

#### extracted, new-style
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source/anchors
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/source/blacklist
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/pem
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl
mkdir -p -m 755 $RPM_BUILD_ROOT%{catrustdir}/extracted/java
mkdir -p -m 755 $RPM_BUILD_ROOT%{_bindir}
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/anchors
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/blacklist

install -p -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/README
install -p -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{catrustdir}/README
install -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{catrustdir}/extracted/README
install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{catrustdir}/extracted/java/README
install -p -m 644 %{SOURCE15} $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl/README
install -p -m 644 %{SOURCE16} $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/README
install -p -m 644 %{SOURCE17} $RPM_BUILD_ROOT%{catrustdir}/source/README

install -p -m 644 %{name}/%{trusted_all_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{trusted_all_bundle}
install -p -m 644 %{name}/%{neutral_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{neutral_bundle}
install -p -m 644 %{name}/%{bundle_supplement} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{bundle_supplement}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{trusted_all_bundle}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{neutral_bundle}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{bundle_supplement}

install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/update-ca-trust

# touch ghosted files that will be extracted dynamically
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/tls-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/email-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/pem/objsign-ca-bundle.pem
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/openssl/%{trusted_all_bundle}
touch $RPM_BUILD_ROOT%{catrustdir}/extracted/%{java_bundle}


%clean
rm -rf $RPM_BUILD_ROOT


%post
if test -e %{_bindir}/update-ca-trust ; then
	%{_bindir}/update-ca-trust
fi

%postun
# While the following is strictly discouraged, we cannot prevent it from happening:
# An admin could potentially use "update-ca-trust enable", thereby installing
# symbolic links for the legacy filename, and afterwards, the admin could 
# downgrade the ca-certificates package to an older version, which doesn't
# provide the new system of extracted files.
# If that happened, the symbolic links will become dangling links,
# and the old bundle files will get installed as .rpmnew files.
# That's a broken configuration.
# 
# Let's attempt to prevent admins from shooting themselves in the foot,
# by handling that scenario in a sane way.
#
if [ $1 -gt 0 ] ; then
	# This isn't a complete removal of the package.
	# There is still a ca-certificates package installed.
	# Because we are noarch, this cannot be a multilib situation.
	# Therefore it's clear the package that belongs to this script 
	# has been replaced by a newer or an older package.
	#
	# Detect if the legacy filenames are symbolic links.
	# If they aren't symbolic links, we're good, the legacy support was disabled,
	#     we assume the upgrade or downgrade has succeeded,
	#     and we don't take any action.
	# If they are symbolic links, then we must check if the link resolves to a file.
	# If it resolves, we're good. It was an upgrade or a downgrade to package version
	#     that provides the target files. No action necessary.
	# However, if we detect broken (dangling) links, then the new package version
	#     doesn't provide the new target files. We assume it's a downgrade
	#     and we must repair the dangling links. We'll replace them with ordinary
	#     files, either taking the files from our backup, or if no backup is
	#     available (unexpectedly) we'll use the .rpmnew file that just got installed.
    #
    # The above logic will restore the backup files that got saved at the time
    # the "enable" command had been executed.
    # If one of the backed up files was a file that had been modified by the admin
    # (prior to the backup), then that modified file will be restored
    # (because rpm kept the config(noreplace) file.
    # However, if the admin didn't change the files, then rpm has installed
    # more recent versions of the bundle files, and that more recent file will
    # be backed up.
    # In the latter scenario, as a result, our recovery logic will recover
    # using the more recent bundle file from the more recent package,
    # despite an older package being installed.
    # This side effect, which keeps slightly more recent unmodified bundles 
    # despite a package downgrade, should be an acceptable side effect, because
    # restoring the manually modified bundle files is much more important.
    
    backuppath=/etc/pki/backup-traditional-recent-config/
    already_warned=0
    for legacy in "cacerts" "ca-bundle.crt" "ca-bundle.trust.crt"; do
		lpath=
		if [ $legacy = "cacerts" ]; then
			lpath="/etc/pki/java/"
		fi
		if [ $legacy = "ca-bundle.crt" ]; then
			lpath="/etc/pki/tls/certs/"
		fi
		if [ $legacy = "ca-bundle.trust.crt" ]; then
			lpath="/etc/pki/tls/certs/"
		fi
		
		if ! test -z "$lpath"; then
			# sanity check succeded, lpath not empty
			if test -L ${lpath}${legacy}; then
				# is link
				if test -e ${lpath}${legacy}; then
					echo "Please ignore warnings about %{lpath}${legacy}.rpmnew, they are expected as the new consolidated configuration feature is enabled" >&2
				else
					# link target doesnt exist
					
					if [ $already_warned -eq 0 ] ; then 
						echo "Detected a downgrade of ca-certificates.rpm to an older package," >&2
						echo "  which doesn't support the new consolidated configuration feature." >&2
						echo "However, at the time of dowgrading, the new consolidated feature was enabled." >&2
						echo "This was an unsupported action, but this script will try its best to recover." >&2
						already_warned=1
					fi
					
					rm -f ${lpath}${legacy}
					echo "Removing symbolic link ${lpath}${legacy}" >&2
					echo "  because the new configuration feature has been removed" >&2
					
					if test -e ${backuppath}${legacy}; then
						# backup file exists
						echo "Backup file found at ${backuppath}${legacy}," >&2
						echo "    restoring it as ${lpath}${legacy}" >&2
						cp --dereference --preserve --force \
							${backuppath}${legacy} ${lpath}${legacy}
					else
						echo "No backup file found."
						if test -e ${lpath}${legacy}.rpmnew; then
							# .rpmnew file found
							echo "Using file ${lpath}${legacy}.rpmnew " >&2
							echo "  and installing it at ${lpath}${legacy}" >&2
							cp --dereference --preserve --force \
								${lpath}${legacy}.rpmnew ${lpath}${legacy}
						# else
							# there's nothing we can do
							echo "Sorry, no files found to provide ${lpath}${legacy}" >&2
						fi
					fi
				fi
			fi
		fi
	done
fi


%files
%defattr(-,root,root,-)
%{_mandir}/man8/update-ca-trust.8.gz
%dir %{pkidir}/java
%config(noreplace) %{pkidir}/java/cacerts
%dir %{pkidir}/tls
%dir %{pkidir}/tls/certs
%config(noreplace) %{pkidir}/tls/certs/ca-bundle.*crt
%{pkidir}/tls/cert.pem
%dir %{_sysconfdir}/ssl
%{_sysconfdir}/ssl/certs

%dir %{catrustdir}
%dir %{catrustdir}/source
%dir %{catrustdir}/source/anchors
%dir %{catrustdir}/source/blacklist
%dir %{catrustdir}/extracted
%dir %{catrustdir}/extracted/pem
%dir %{catrustdir}/extracted/openssl
%dir %{catrustdir}/extracted/java
%dir %{_datadir}/pki/ca-trust-source
%dir %{_datadir}/pki/ca-trust-source/anchors
%dir %{_datadir}/pki/ca-trust-source/blacklist

%{_datadir}/pki/ca-trust-source/README
%{catrustdir}/README
%{catrustdir}/extracted/README
%{catrustdir}/extracted/java/README
%{catrustdir}/extracted/openssl/README
%{catrustdir}/extracted/pem/README
%{catrustdir}/source/README

# master bundle file with trust
%{_datadir}/pki/ca-trust-source/%{trusted_all_bundle}
%{_datadir}/pki/ca-trust-source/%{neutral_bundle}
%{_datadir}/pki/ca-trust-source/%{bundle_supplement}
# update/extract tool
%{_bindir}/update-ca-trust
# extracted files
%ghost %{catrustdir}/extracted/pem/tls-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/email-ca-bundle.pem
%ghost %{catrustdir}/extracted/pem/objsign-ca-bundle.pem
%ghost %{catrustdir}/extracted/openssl/%{trusted_all_bundle}
%ghost %{catrustdir}/extracted/%{java_bundle}


%changelog
* Thu Feb 13 2014 Matthias Saou <matthias@saou.eu> 2013.1.95-65.1
- Update java BR from 1.6.0 to 1.7.0 for el5 rebuild.

* Tue Dec 17 2013 Kai Engert <kaie@redhat.com> - 2013.1.95-65.1
- Update to CKBI 1.95 from NSS 3.15.3.1

* Tue Sep 03 2013 Kai Engert <kaie@redhat.com> - 2013.1.94-65.0
- Update to CKBI 1.94 from NSS 3.15

* Thu Jul 18 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.9
- fix manpage format

* Wed Jul 17 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.8
- improve manpage

* Thu Jul 11 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.7
- ExcludeArch/ExclusiveArch doesn't work to enforce a build host
- Added comment that explains the special build requirements.
- Added a comment suggesting to keep the release number below the 
  ones used on RHEL 7.
- Fixed permissions of /etc/pki/java (thanks to stefw)

* Mon Jul 08 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.6
- set a certificate alias in trusted bundle (thanks to Ludwig Nussel)

* Mon Jul 08 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.5
- update required p11-kit version

* Wed Jul 03 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.4
- attempt to handle unsupported downgrades, where the admin has enabled
  legacy support, but downgrades to an old package that is incompatible
  provide the new feature.
- move manual page to the man8 section (system administration commands)
- simplify the README files now that we have a manual page

* Fri Jun 14 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.3
- added a manual page and related build requirements
- updated copyright sections in scripts
- enhance update-ca-trust script

* Fri Jun 14 2013 Stef Walter <stefw@redhat.com> - 2012.87-65.2
- update-ca-trust: Print warnings to stderr

* Fri Jun 14 2013 Stef Walter <stefw@redhat.com> - 2012.87-65.1
- update-ca-trust: Update p11-kit script path
- update-ca-trust: script uses bash not sh

* Fri Jun 14 2013 Kai Engert <kaie@redhat.com> - 2012.87-65.0
- Major rework introducing the SharedSystemCertificates feature, 
  disabled by default.
- Require the p11-kit package that contains tools to automatically create
  other file format bundles.
- Added a update-ca-trust script which can be used to enable the
  new system and to regenerate the merged trust output.
- Refer to the various README files that have been added for more detailed
  explanation of the new system.
- No longer require rsc for building. Remove use of rcs/ident.
- Update source URLs and comments, add source file for version information.
- Add explanation for the future version numbering scheme,
  because the old numbering scheme assumed upstream using cvs,
  which is no longer true, and therefore can no longer be used.

* Thu Mar  1 2012 Joe Orton <jorton@redhat.com> - 2010.63-4
- fix inclusion of code-signing-only certs in .trust.crt
- exclude blacklisted root from java keystore too
- remove trust from DigiNotar root (#734678)

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-3
- package /etc/ssl/certs symlink for third-party apps (#572725)

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-2
- rebuild

* Wed Apr  7 2010 Joe Orton <jorton@redhat.com> - 2010.63-1
- update to certdata.txt r1.63
- use upstream RCS version in Version

* Fri Mar 19 2010 Joe Orton <jorton@redhat.com> - 2010-4
- fix ca-bundle.crt (#575111)

* Thu Mar 18 2010 Joe Orton <jorton@redhat.com> - 2010-3
- update to certdata.txt r1.58
- add /etc/pki/tls/certs/ca-bundle.trust.crt using 'TRUSTED CERTICATE' format
- exclude ECC certs from the Java cacerts database
- catch keytool failures
- fail parsing certdata.txt on finding untrusted but not blacklisted cert

* Fri Jan 15 2010 Joe Orton <jorton@redhat.com> - 2010-2
- fix Java cacert database generation: use Subject rather than Issuer
  for alias name; add diagnostics; fix some alias names.

* Mon Jan 11 2010 Joe Orton <jorton@redhat.com> - 2010-1
- adopt Python certdata.txt parsing script from Debian

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Joe Orton <jorton@redhat.com> 2009-1
- update to certdata.txt r1.53

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 14 2008 Joe Orton <jorton@redhat.com> 2008-7
- update to certdata.txt r1.49

* Wed Jun 25 2008 Thomas Fitzsimmons <fitzsim@redhat.com> - 2008-6
- Change generate-cacerts.pl to produce pretty aliases.

* Mon Jun  2 2008 Joe Orton <jorton@redhat.com> 2008-5
- include /etc/pki/tls/cert.pem symlink to ca-bundle.crt

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-4
- use package name for temp dir, recreate it in prep

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-3
- fix source script perms
- mark packaged files as config(noreplace)

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-2
- add (but don't use) mkcabundle.pl
- tweak description
- use /usr/bin/keytool directly; BR java-openjdk

* Tue May 27 2008 Joe Orton <jorton@redhat.com> 2008-1
- Initial build (#448497)
