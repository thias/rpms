# remirepo spec file for php 7.1
# with backport stuff, adapted from
#
# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check
%global apiver      20160303
%global zendver     20160303
%global pdover      20150127
# Extension version
%global fileinfover 1.0.5
%global oci8ver     2.1.8
%global zipver      1.13.0
%global jsonver     1.5.0

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 7.1

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%global oraclever 21.8
%global oraclelib 21.1

# Build for LiteSpeed Web Server (LSAPI)
%global with_lsws     1

# Regression tests take a long time, you can skip 'em with this
#global runselftest 0
%{!?runselftest: %global runselftest 1}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

# Optional components; pass "--with mssql" etc to rpmbuild.
%global with_oci8      %{?_with_oci8:1}%{!?_with_oci8:0}

%if 0%{?fedora} >= 22 || 0%{?rhel} >= 8
%global with_libpcre  1
%else
%global with_libpcre  0
%endif

%global with_sqlite3  1

# Build ZTS extension or only NTS
%global with_zts      1

# Debuild build
%global with_debug    %{?_with_debug:1}%{!?_with_debug:0}

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# /usr/sbin/apsx with httpd < 2.4 and defined as /usr/bin/apxs with httpd >= 2.4
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}
%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# systemd to manage the service, with notify mode, with additional service config
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
# httpd 2.4.10 with httpd-filesystem and sethandler support
%if 0%{?fedora} >= 21
%global with_httpd2410 1
%else
%global with_httpd2410 0
%endif
# nginx 1.6 with nginx-filesystem
%if 0%{?fedora} >= 21
%global with_nginx     1
%else
%global with_nginx     0
%endif

%global with_dtrace  1
%global with_libgd   1
%global with_libzip  1
%global with_zip     0

%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

%global upver        7.1.33

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: %{upver}%{?rcver:~%{rcver}}
Release: 24%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: php.ztsmodconf
Source11: php.conf2
Source12: php-fpm.wants
Source13: nginx-fpm.conf
Source14: nginx-php.conf
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist
Source52: 20-oci8.ini
Source99: php-fpm.init

# Build fixes
Patch1: php-7.1.7-httpd.patch
Patch2: php-7.1.33-intl.patch
Patch5: php-7.0.0-includedir.patch
Patch6: php-5.6.3-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-7.0.2-libdb.patch
Patch9: php-7.0.7-curl.patch

# Functional changes
Patch40: php-7.1.16-dlopen.patch
Patch42: php-7.1.0-systzdata-v14.patch
# See http://bugs.php.net/53436
Patch43: php-7.1.24-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-7.1.15-ldap_r.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch
# Automatically load OpenSSL configuration file
Patch48: php-7.1.9-openssl-load-config.patch
# getallheaders for FPM backported from 7.3
Patch49: php-7.1.24-getallheaders.patch

# RC Patch
Patch91: php-5.6.3-oci8conf.patch

# Upstream fixes (100+)

# Security fixes (200+)
Patch201: php-bug78878.patch
Patch202: php-bug78862.patch
Patch203: php-bug78863.patch
Patch204: php-bug78793.patch
Patch205: php-bug78910.patch
Patch206: php-bug79091.patch
Patch207: php-bug79099.patch
Patch208: php-bug79037.patch
Patch209: php-bug77569.patch
Patch210: php-bug79221.patch
Patch211: php-bug79082.patch
Patch212: php-bug79282.patch
Patch213: php-bug79329.patch
Patch214: php-bug79330.patch
Patch215: php-bug79465.patch
Patch216: php-bug78875.patch
Patch217: php-bug78876.patch
Patch218: php-bug79797.patch
Patch219: php-bug79877.patch
Patch220: php-bug79601.patch
Patch221: php-bug79699.patch
Patch222: php-bug77423.patch
Patch223: php-bug80672.patch
Patch224: php-bug80710.patch
Patch225: php-bug81122.patch
Patch226: php-bug76450.patch
Patch227: php-bug81211.patch
Patch228: php-bug81026.patch
Patch229: php-bug79971.patch
Patch230: php-bug81719.patch
Patch231: php-bug81720.patch
Patch232: php-bug81727.patch
Patch233: php-bug81726.patch
Patch234: php-bug81740.patch
Patch235: php-bug81744.patch
Patch236: php-bug81746.patch
Patch237: php-cve-2023-0662.patch

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-7.0.10-datetests.patch
# Revert changes for pcre < 8.34
Patch301: php-7.0.0-oldpcre.patch
# Renew openssl certs
Patch302: php-openssl-cert.patch

# WIP

BuildRequires: bzip2-devel, curl-devel >= 7.9
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
%if %{with_httpd2410}
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
%endif
%if %{with_nginx}
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
%endif
BuildRequires: %{?dtsprefix}libstdc++-devel, openssl-devel
%if %{with_sqlite3}
# For Sqlite3 extension
BuildRequires: sqlite-devel >= 3.6.0
%else
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if %{with_libpcre}
BuildRequires: pcre-devel >= 8.20
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, %{?dtsprefix}gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_dtrace}
BuildRequires: %{?dtsprefix}systemtap-sdt-devel
%endif
#BuildRequires: bison
BuildRequires: /bin/ps

%if 0%{?rhel}
Obsoletes: php53, php53u, php54w, php55u, php55w, php56u, php56w, mod_php70u, php70w, mod_php71u, mod_php71w
%endif
# Avoid obsoleting php54 from RHSCL
Obsoletes: php54 > 5.4
%if %{with_zts}
Obsoletes: php-zts < 5.3.7
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: php-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
%if %{with_httpd2410}
Requires(pre): httpd-filesystem
%else
Requires(pre): httpd
%endif
# php engine for Apache httpd webserver
Provides: php(httpd)
%if 0%{?fedora} >= 27
# httpd have threaded MPM by default
Recommends: php-fpm%{?_isa} = %{version}-%{release}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Don't provides extensions, which are not shared library, as .so
%{?filter_provides_in: %filter_provides_in %{_libdir}/php/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_libdir}/php-zts/modules/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}
%endif


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License:  PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}
%if 0%{?rhel}
Obsoletes: php53-cli, php53u-cli, php54-cli, php54w-cli, php55u-cli, php55w-cli, php56u-cli, php56w-cli, php70u-cli, php70w-cli, php71u-cli, php71w-cli
%endif

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Group: Development/Languages
Summary: The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php56u-dbg, php56w-phpdbg, php70u-dbg, php70w-phpdbg, php70u-dbg, php71w-phpdbg
%endif
%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
BuildRequires: libacl-devel
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_systemd}
BuildRequires: systemd-devel
%{?systemd_requires}
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%else
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif
%if %{with_httpd2410}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
# php engine for Apache httpd webserver
Provides: php(httpd)
%else
Requires(pre): /usr/sbin/useradd
%endif
%if %{with_nginx}
# for /etc/nginx ownership
Requires: nginx-filesystem
%endif
%if 0%{?rhel}
Obsoletes: php53-fpm, php53u-fpm, php54-fpm, php54w-fpm, php55u-fpm, php55w-fpm, php56u-fpm, php56w-fpm, php70u-fpm, php70w-fpm, php71u-fpm, php71w-fpm
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%if %{with_lsws}
%package litespeed
Summary: LiteSpeed Web Server PHP support
Group: Development/Languages
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-litespeed, php53u-litespeed, php54-litespeed, php54w-litespeed, php55u-litespeed, php55w-litespeed, php56u-litespeed, php56w-litespeed, php70u-litespeed, php70w-litespeed, php70w-litespeed, php71w-litespeed
%endif

%description litespeed
The php-litespeed package provides the %{_bindir}/lsphp command
used by the LiteSpeed Web Server (LSAPI enabled PHP).
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP and BSD
# ABI/API check - Arch specific
Provides: php(api) = %{apiver}%{isasuffix}
Provides: php(zend-abi) = %{zendver}%{isasuffix}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
Provides: php-zlib, php-zlib%{?_isa}
# For user experience, those extensions were part of php-common
Requires: php-json%{?_isa} = %{version}-%{release}
#Requires:  php-zip%%{?_isa}

Obsoletes: php-pecl-phar < 1.2.4
Obsoletes: php-pecl-Fileinfo < 1.0.5
Provides:  php-pecl-Fileinfo = %{fileinfover}, php-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides:  php-pecl(Fileinfo) = %{fileinfover}, php-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Obsoletes: php-mhash < 5.3.0
%if 0%{?rhel}
Obsoletes: php53-mhash, php53u-mhash
Obsoletes: php53-common, php53u-common, php54-common, php54w-common, php55u-common, php55w-common, php56u-common, php56w-common, php70u-common, php70w-common, php71u-common, php71w-common
%endif

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}, autoconf, automake, make
# see "php-config --libs"
Requires: krb5-devel%{?_isa}
Requires: libedit-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: openssl-devel%{?_isa}
%if %{with_libpcre}
Requires: pcre-devel%{?_isa}
%endif
Requires: zlib-devel%{?_isa}
Obsoletes: php-pecl-pdo-devel
Obsoletes: php-pecl-json-devel  < %{jsonver}
Obsoletes: php-pecl-jsonc-devel < %{jsonver}
%if %{with_zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif
%if 0%{?rhel}
Obsoletes: php53-devel, php53u-devel, php54-devel, php54w-devel, php55u-devel, php55w-devel, php56u-devel, php56w-devel, php70u-devel, php70w-devel, php71u-devel, php71w-devel
Obsoletes: php55u-pecl-jsonc-devel, php56u-pecl-jsonc-devel
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
Group:     Development/Languages
License:   PHP
Requires:  php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zendopcache
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}
%if 0%{?rhel}
Obsoletes: php55u-opcache, php55w-opcache, php56u-opcache, php56w-opcache, php70u-opcache, php70w-opcache, php71u-opcache, php71w-opcache
%endif

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel
%if 0%{?rhel}
Obsoletes: php53-imap, php53u-imap, php54-imap, php54w-imap, php55u-imap, php55w-imap, php56u-imap, php56w-imap, php70u-imap, php70w-imap, php71u-imap, php71w-imap
%endif

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel
%if 0%{?rhel}
Obsoletes: php53-ldap, php53u-ldap, php54-ldap, php54w-ldap, php55u-ldap, php55w-ldap, php56u-ldap, php56w-ldap, php70u-ldap, php70w-ldap, php71u-ldap, php71w-ldap
%endif

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}%{isasuffix}
Provides: php(pdo-abi) = %{pdover}%{isasuffix}
%if %{with_sqlite3}
Provides: php-sqlite3, php-sqlite3%{?_isa}
%endif
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}
%if 0%{?rhel}
Obsoletes: php53-pdo, php53u-pdo, php54-pdo, php54w-pdo, php55u-pdo, php55w-pdo, php56u-pdo, php56w-pdo, php70u-pdo, php70w-pdo, php71u-pdo, php71w-pdo
%endif

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
Obsoletes: php-mysql < %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-mysqlnd, php53u-mysqlnd, php54-mysqlnd, php54w-mysqlnd, php55u-mysqlnd, php55w-mysqlnd, php56u-mysqlnd, php56w-mysqlnd, php70u-mysqlnd, php70w-mysqlnd, php71u-mysqlnd, php71w-mysqlnd
Obsoletes: php53-mysql, php53u-mysql, php54-mysql, php54w-mysql, php55u-mysql, php55w-mysql, php56u-mysql, php56w-mysql, php70u-mysql, php70w-mysql, php71u-mysql, php71w-mysql
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel, openssl-devel, postgresql-devel
%if 0%{?rhel}
Obsoletes: php53-pgsql, php53u-pgsql, php54-pgsql, php54w-pgsql, php55u-pgsql, php55w-pgsql, php56u-pgsql, php56w-pgsql, php70u-pgsql, php70w-pgsql, php71u-pgsql, php71w-pgsql
%endif

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}
%if 0%{?rhel}
Obsoletes: php53-process, php53u-process, php54-process, php54w-process, php55u-process, php55w-process, php56u-process, php56w-process, php70u-process, php70w-process, php71u-process, php71w-process
%endif

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel
%if 0%{?rhel}
Obsoletes: php53-odbc, php53u-odbc, php54-odbc, php54w-odbc, php55u-odbc, php55w-odbc, php56u-odbc, php56w-odbc, php70u-odbc, php70w-odbc, php71u-odbc, php71w-odbc
%endif

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel
%if 0%{?rhel}
Obsoletes: php53-soap, php53u-soap, php54-soap, php54w-soap, php55u-soap, php55w-soap, php56u-soap, php56w-soap, php70u-soap, php70w-soap, php71u-soap, php71w-soap
%endif

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires:  firebird-devel
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-firebird, php-firebird%{?_isa}
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}
%if 0%{?rhel}
Obsoletes: php53-interbase, php53u-interbase, php54-interbase, php54w-interbase, php55u-interbase, php55w-interbase, php56u-interbase, php56w-interbase, php70u-interbase, php70w-interbase, php71u-interbase, php71w-interbase
%endif

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.

%if %{with_oci8}
%package oci8
Summary:        A module for PHP applications that use OCI8 databases
Group:          Development/Languages
# All files licensed under PHP version 3.01
License:        PHP
BuildRequires:  oracle-instantclient-devel >= %{oraclever}
Requires:       php-pdo%{?_isa} = %{version}-%{release}
Provides:       php_database
Provides:       php-pdo_oci, php-pdo_oci%{?_isa}
Obsoletes:      php-pecl-oci8 <  %{oci8ver}
Conflicts:      php-pecl-oci8 >= %{oci8ver}
Provides:       php-pecl(oci8) = %{oci8ver}, php-pecl(oci8)%{?_isa} = %{oci8ver}
# Should requires libclntsh.so.12.1, but it's not provided by Oracle RPM.
AutoReq:        0
%if 0%{?rhel}
Obsoletes:      php53-oci8, php53u-oci8, php54-oci8, php54w-oci8, php55u-oci8, php55w-oci8, php56u-oci8, php56w-oci8, php70u-oci8, php70w-oci8, php71u-oci8, php71w-oci8
%endif

%description oci8
The php-oci8 packages provides the OCI8 extension version %{oci8ver}
and the PDO driver to access Oracle Database.

The extension is linked with Oracle client libraries %{oraclever}
(Oracle Instant Client).  For details, see Oracle's note
"Oracle Client / Server Interoperability Support" (ID 207303.1).

You must install libclntsh.so.%{oraclelib} to use this package, provided
in the database installation, or in the free Oracle Instant Client
available from Oracle.

Notice:
- php-oci8 provides oci8 and pdo_oci extensions from php sources.
- php-pecl-oci8 only provides oci8 extension.

Documentation is at http://php.net/oci8 and http://php.net/pdo_oci
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel
%if 0%{?rhel}
Obsoletes: php53-snmp, php53u-snmp, php54-snmp, php54w-snmp, php55u-snmp, php55w-snmp, php56u-snmp, php56w-snmp, php70u-snmp, php70w-snmp, php71u-snmp, php71w-snmp
%endif

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-wddx, php-wddx%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1
%if 0%{?rhel}
Obsoletes: php53-xml, php53u-xml, php54-xml, php54w-xml, php55u-xml, php55w-xml, php56u-xml, php56w-xml, php70u-xml, php70w-xml, php71u-xml, php71w-xml
%endif

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: php-xml%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-xmlrpc, php53u-xmlrpc, php54-xmlrpc, php54w-xmlrpc, php55u-xmlrpc, php55w-xmlrpc, php56u-xmlrpc, php56w-xmlrpc, php70u-xmlrpc, php70w-xmlrpc, php71u-xmlrpc, php71w-xmlrpc
%endif

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-mbstring, php53u-mbstring, php54-mbstring, php54w-mbstring, php55u-mbstring, php55w-mbstring, php56u-mbstring, php56w-mbstring, php70u-mbstring, php70w-mbstring, php71u-mbstring, php71w-mbstring
%endif

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01
%if %{with_libgd}
License: PHP
%else
# bundled libgd is licensed under BSD
License: PHP and BSD
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with_libgd}
BuildRequires: gd-devel >= 2.3.3
%else
# Required to build the bundled GD library
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libwebp-devel
%endif
%if 0%{?rhel}
Obsoletes: php53-gd, php53u-gd, php54-gd, php54w-gd, php55u-gd, php55w-gd, php56u-gd, php56w-gd, php70u-gd, php70w-gd, php71u-gd, php71w-gd
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-bcmath, php53u-bcmath, php54-bcmath, php54w-bcmath, php55u-bcmath, php55w-bcmath, php56u-bcmath, php56w-bcmath, php70u-bcmath, php70w-bcmath, php71u-bcmath, php71w-bcmath
%endif

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-gmp, php53u-gmp, php54-gmp, php54w-gmp, php55u-gmp, php55w-gmp, php56u-gmp, php56w-gmp, php70u-gmp, php70w-gmp, php71u-gmp, php71w-gmp
%endif

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, gdbm-devel, tokyocabinet-devel
Requires: php-common%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-dba, php53u-dba, php54-dba, php54w-dba, php55u-dba, php55w-dba, php56u-dba, php56w-dba, php70u-dba, php70w-dba, php71u-dba, php71w-dba
%endif

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel
%if 0%{?rhel}
Obsoletes: php53-mcrypt, php53u-mcrypt, php54-mcrypt, php54w-mcrypt, php55u-mcrypt, php55w-mcrypt, php56u-mcrypt, php56w-mcrypt, php70u-mcrypt, php70w-mcrypt, php71u-mcrypt, php71w-mcrypt
%endif

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel
%if 0%{?rhel}
Obsoletes: php53-tidy, php53u-tidy, php54-tidy, php54w-tidy, php55u-tidy, php55w-tidy, php56u-tidy, php56w-tidy, php70u-tidy, php70w-tidy, php71u-tidy, php71w-tidy
%endif

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package pdo-dblib
Summary: PDO driver Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel >= 0.91
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}
Obsoletes: php-mssql < %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-mssql, php53u-mssql, php54-mssql, php54w-mssql, php55u-mssql, php55w-mssql, php56u-mssql, php56w-mssql, php70u-pdo-dblib, php70w-pdo_dblib, php71u-pdo-dblib, php71w-pdo_dblib
%endif

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS library.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}
%if 0%{?rhel}
Obsoletes: php53-embedded, php53u-embedded, php54-embedded, php54w-embedded, php55u-embedded, php55w-embedded, php56u-embedded, php56w-embedded, php70u-embedded, php70w-embedded, php71u-embedded, php71w-embedded
%endif

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0
%if 0%{?rhel}
Obsoletes: php53-pspell, php53u-pspell, php54-pspell, php54w-pspell, php55u-pspell, php55w-pspell, php56u-pspell, php56w-pspell, php70u-pspell, php70w-pspell, php71u-pspell, php71w-pspell
%endif

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel
%if 0%{?rhel}
Obsoletes: php53-recode, php53u-recode, php54-recode, php54w-recode, php55u-recode, php55w-recode, php56u-recode, php56w-recode, php70u-recode, php70w-recode, php71u-recode, php71w-recode
%endif

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
# Upstream requires 4.0, we require 69.1 to ensure use of libicu69
BuildRequires: libicu-devel = 69.1
%if 0%{?rhel}
Obsoletes: php53-intl, php53u-intl, php54-intl, php54w-intl, php55u-intl, php55w-intl, php56u-intl, php56w-intl, php70u-intl, php70w-intl, php71u-intl, php71w-intl
%endif

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4
%if 0%{?rhel}
Obsoletes: php53-enchant, php53u-enchant, php54-enchant, php54w-enchant, php55u-enchant, php55w-enchant, php56u-enchant, php56w-enchant, php70u-enchant, php70w-enchant, php71u-enchant, php71w-enchant
%endif

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%if %{with_zip}
%package zip
Summary: ZIP archive management extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zip          < %{zipver}
Provides:  php-pecl(zip)         = %{zipver}
Provides:  php-pecl(zip)%{?_isa} = %{zipver}
Provides:  php-pecl-zip          = %{zipver}
Provides:  php-pecl-zip%{?_isa}  = %{zipver}
%if 0%{?rhel}
Obsoletes: php53-zip, php53u-zip, php54-zip, php54w-zip, php55u-zip, php55w-zip, php56u-zip, php56w-zip, php70u-zip, php70w-zip, php71u-zip, php71w-zip
%endif
%if %{with_libzip}
# 0.11.1 required, but 1.0.1 is bundled
BuildRequires: pkgconfig(libzip) >= 1.0.1
%endif

%description zip
The php-zip package provides an extension that will add
support for ZIP archive management to PHP.
%endif

%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-json          < %{jsonver}
Obsoletes: php-pecl-jsonc         < %{jsonver}
Provides:  php-pecl(json)         = %{jsonver}
Provides:  php-pecl(json)%{?_isa} = %{jsonver}
Provides:  php-pecl-json          = %{jsonver}
Provides:  php-pecl-json%{?_isa}  = %{jsonver}
%if 0%{?rhel}
Obsoletes: php53-json, php53u-json, php54-json, php54w-json, php55u-json, php55w-json, php56u-json, php56w-json, php70u-json, php70w-json, php71u-json, php71w-json
Obsoletes: php55u-pecl-jsonc, php56u-pecl-jsonc
%endif

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.


%prep
: CIBLE = %{name}-%{version}-%{release} oci8=%{with_oci8} libzip=%{with_libzip}

%setup -q -n php-%{upver}%{?rcver}

%patch1 -p1 -b .mpmcheck
%patch2 -p1 -b .true
%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb
%if 0%{?rhel}
%patch9 -p1 -b .curltls
%endif

%patch40 -p1 -b .dlopen
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 6
%patch42 -p1 -b .systzdata
%endif
%patch43 -p1 -b .headers
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .loadconf
%patch49 -p1 -b .getallheaders

%patch91 -p1 -b .remi-oci8

# upstream patches

# security patches
%patch201 -p1 -b .bug78878
%patch202 -p1 -b .bug78862
%patch203 -p1 -b .bug78863
%patch204 -p1 -b .bug78793
%patch205 -p1 -b .bug78910
%patch206 -p1 -b .bug79091
%patch207 -p1 -b .bug79099
%patch208 -p1 -b .bug79037
%patch209 -p1 -b .bug77569
%patch210 -p1 -b .bug79221
%patch211 -p1 -b .bug79082
%patch212 -p1 -b .bug79282
%patch213 -p1 -b .bug79329
%patch214 -p1 -b .bug79330
%patch215 -p1 -b .bug79465
%patch216 -p1 -b .bug78875
%patch217 -p1 -b .bug78876
%patch218 -p1 -b .bug79797
%patch219 -p1 -b .bug79877
%patch220 -p1 -b .bug79601
%patch221 -p1 -b .bug79699
%patch222 -p1 -b .bug77423
%patch223 -p1 -b .bug80672
%patch224 -p1 -b .bug80710
%patch225 -p1 -b .bug81122
%patch226 -p1 -b .bug76450
%patch227 -p1 -b .bug81211
%patch228 -p1 -b .bug81026
%patch229 -p1 -b .bug79971
%patch230 -p1 -b .bug81719
%patch231 -p1 -b .bug81720
%patch232 -p1 -b .bug81727
%patch233 -p1 -b .bug81726
%patch234 -p1 -b .bug81740
%patch235 -p1 -b .bug81744
%patch236 -p1 -b .bug81746
%patch237 -p1 -b .cve0662

# Fixes for tests
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 6
%patch300 -p1 -b .datetests
%endif
%if %{with_libpcre}
if ! pkg-config libpcre --atleast-version 8.34 ; then
# Only apply when system libpcre < 8.34
%patch301 -p1 -b .pcre834
fi
%endif
# New openssl certs
%patch302 -p1 -b .renewcert
rm ext/openssl/tests/bug65538_003.phpt

# WIP patch

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
%if ! %{with_libgd}
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
%endif
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# Should be skipped but fails sometime
rm ext/standard/tests/file/file_get_contents_error001.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt
# slow and erratic result
rm sapi/cli/tests/upload_2G.phpt
# avoid issue when 2 builds run simultaneously (keep 64321 for the SCL)
%ifarch x86_64
sed -e 's/64321/64322/' -i ext/openssl/tests/*.phpt
%else
sed -e 's/64321/64323/' -i ext/openssl/tests/*.phpt
%endif

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{upver}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{upver}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=$(sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h)
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=$(sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h)
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=$(sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h)
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_OCI8_VERSION /{s/.* "//;s/".*$//;p}' ext/oci8/php_oci8.h)
if test "$ver" != "%{oci8ver}"; then
   : Error: Upstream OCI8 version is now ${ver}, expecting %{oci8ver}.
   : Update the oci8ver macro and rebuild.
   exit 1
fi

%if %{with_zip}
ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the %{zipver} macro and rebuild.
   exit 1
fi
%endif

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the %{jsonver} macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# Some extensions have their own configuration file
cp %{SOURCE50} 10-opcache.ini
%if 0%{?rhel} != 6
cat << EOF >>10-opcache.ini

; Enables or disables copying of PHP code (text segment) into HUGE PAGES.
; This should improve performance, but requires appropriate OS configuration.
opcache.huge_code_pages=0
EOF
%endif
cp %{SOURCE52} 20-oci8.ini

# Regenerated bison files
# to force, rm Zend/zend_{language,ini}_parser.[ch]
if [ ! -f Zend/zend_language_parser.c ]; then
  ./genfiles
fi

# For doc
cat %{SOURCE1} %{SOURCE11} >httpd-php.conf


%build
%{?dtsenable}

# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)

# aclocal workaround - to be improved
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4

# Force use of system libtool:
libtoolize --force --copy
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force
%if %{with_debug}
LDFLAGS="-fsanitize=address"
export LDFLAGS
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign -fsanitize=address -ggdb"
%else
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
# Only provided in official tarball (not in snapshot)
if [ -f ../Zend/zend_language_parser.c ]; then
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
fi

# Always static:
# date, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap and wddx
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} \
    --enable-gd-native-ttf \
    --without-gdbm \
    --with-jpeg-dir=%{_prefix} \
    --with-openssl \
    --with-system-ciphers \
%if %{with_libpcre}
    --with-pcre-regex=%{_prefix} \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_prefix} \
%if 0%{?fedora} >= 25 || 0%{?rhel} >= 6
    --with-system-tzdata \
%endif
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
%if %{with_debug}
    --enable-debug \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
%if 0%{?rhel} == 6
      --disable-huge-code-pages \
%endif
      --enable-phpdbg \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
      --with-webp-dir=%{_prefix} \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with_oci8}
%ifarch x86_64
      --with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever} \
%else
      --with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client/lib,%{oraclever} \
%endif
      --with-pdo-oci=shared,instantclient,/usr,%{oraclever} \
%endif
      --with-interbase=shared \
      --with-pdo-firebird=shared \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if %{with_sqlite3}
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-json \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
%if %{with_lsws}
      --with-litespeed \
%endif
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemd}
      --with-fpm-systemd \
%endif
      --with-fpm-acl \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp7.so
pushd build-embedded
build --enable-embed \
      --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
%if 0%{?rhel} == 6
      --disable-huge-code-pages \
%endif
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
      --with-webp-dir=%{_prefix} \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
%if %{with_oci8}
%ifarch x86_64
      --with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client64/lib,%{oraclever} \
%else
      --with-oci8=shared,instantclient,%{_libdir}/oracle/%{oraclever}/client/lib,%{oraclever} \
%endif
      --with-pdo-oci=shared,instantclient,/usr,%{oraclever} \
%endif
      --with-interbase=shared \
      --with-pdo-firebird=shared \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if %{with_sqlite3}
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
%if %runselftest
cd build-fpm

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
export SKIP_SLOW_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      head -n 100 "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif


%install
%{?dtsenable}

%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7.so

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7-zts.so
%endif

# Apache config fragment
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4 (fedora <= 17)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%if %{with_zts} && 0%{?fedora} < 27 && 0%{?rhel} < 8
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif
%if %{with_httpd2410}
cat %{SOURCE11} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
mkdir _fpmdoc
cat %{SOURCE1} %{SOURCE11} >_fpmdoc/httpd-php.conf
cat << 'EOF' >_fpmdoc/README
To use FPM with Apache HTTP server:
- copy the httpd-php.conf to %{_httpd_confdir}/php.conf

To use FPM with NGINX web server:
- copy the nginx-fpm.conf to %{_sysconfdir}/nginx/conf.d/php-fpm.conf
- copy the nginx-php.conf to %{_sysconfdir}/nginx/default.d/php.conf
EOF
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/opcache
%if 0%{?fedora} >= 24
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/peclxml
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl
%endif

%if %{with_lsws}
install -m 755 build-apache/sapi/litespeed/php $RPM_BUILD_ROOT%{_bindir}/lsphp
%endif

# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm

# Environment file
%if 0%{?fedora} < 26
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
%endif

%if %{with_systemd}
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# install systemd unit files and scripts for handling server startup
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -Dm 644 %{SOURCE6}  $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
%if 0%{?fedora} >= 27
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d/php-fpm.conf
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/nginx.service.d/php-fpm.conf
%endif
%else
sed  -ne '1,2p' -i $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE99} $RPM_BUILD_ROOT%{_initrddir}/php-fpm
%endif

%if 0%{?fedora} >= 26
sed -e '/EnvironmentFile/d' -i $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
%endif

%if %{with_nginx}
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

# Switch to UDS
# FPM
sed -e 's@127.0.0.1:9000@/run/php-fpm/www.sock@' \
    -e 's@^;listen.acl_users@listen.acl_users@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
# Nginx
sed -e 's@127.0.0.1:9000@unix:/run/php-fpm/www.sock@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
# Apache
sed -e 's@proxy:fcgi://127.0.0.1:9000@proxy:unix:/run/php-fpm/www.sock|fcgi://localhost@' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
install -D -m 644 %{SOURCE13} _fpmdoc/nginx-fpm.conf
install -D -m 644 %{SOURCE14} _fpmdoc/nginx-php.conf
%endif

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc imap json \
    mysqlnd mysqli pdo_mysql \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with_zip}
    zip \
%endif
%if %{with_oci8}
    oci8 pdo_oci \
%endif
    interbase pdo_firebird \
%if %{with_sqlite3}
    sqlite3 \
%endif
    enchant phar fileinfo intl \
    mcrypt tidy pdo_dblib pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml \
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      pdo_*|mysqli|wddx|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if %{with_oci8}
cat files.pdo_oci >> files.oci8
%endif
cat files.pdo_firebird >> files.interbase

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if %{with_sqlite3}
cat files.sqlite3 >> files.pdo
%endif

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{upver}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
%if 0%{?fedora} >= 24
echo '%%pecl_xmldir   %{_localstatedir}/lib/php/peclxml' >>macros.php
%endif
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%pre common
%if %{?fedora}%{!?fedora:99} < 25
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%if ! %{with_httpd2410}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0
%endif

%post fpm
%if %{with_systemd}
%systemd_post php-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add php-fpm
fi
%endif

%preun fpm
%if %{with_systemd}
%systemd_preun php-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi
%endif

%if 0%{?fedora} < 27 && 0%{?rhel} < 8
%postun fpm
%if %{with_systemd}
%systemd_postun_with_restart php-fpm.service
%else
if [ $1 -ge 1 ]; then
    /sbin/service php-fpm condrestart >/dev/null 2>&1 || :
fi
%endif
%endif

%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
# Raised by new pool installation or new extension installation
%transfiletriggerin fpm -- %{_sysconfdir}/php-fpm.d %{_sysconfdir}/php.d
systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php-fpm
%if 0%{?fedora} >= 15
if [ -f /etc/rc.d/init.d/php-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php-fpm.service >/dev/null 2>&1 || :
fi
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig


%posttrans common
cat << EOF
=====================================================================

  WARNING : PHP 7.1 have reached its "End of Life" in
  December 2019. Even, if this package includes some of
  the important security fixes, backported from 8.0, the
  UPGRADE to a maintained version is very strongly RECOMMENDED.

=====================================================================
EOF


%{!?_licensedir:%global license %%doc}

%files
%{_httpd_moddir}/libphp7.so
%if %{with_zts}
%{_httpd_moddir}/libphp7-zts.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%endif
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%license LICENSE TSRM_LICENSE ZEND_LICENSE
%license libmagic_LICENSE
%license phar_LICENSE
%license timelib_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%if 0%{?fedora} >= 24
%dir %{_localstatedir}/lib/php/peclxml
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%endif
%dir %{_datadir}/php

%files cli
%{_bindir}/php
%{_bindir}/zts-php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/zts-php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%{_mandir}/man1/zts-phpize.1*
%doc sapi/cgi/README* sapi/cli/README

%files dbg
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with_zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif
%doc sapi/phpdbg/{README.md,CREDITS}

%files fpm
%doc php-fpm.conf.default www.conf.default httpd-php.conf
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/php.conf
%else
%doc _fpmdoc/*
%endif
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%if 0%{?fedora} < 26
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%endif
%if %{with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%endif
%if %{with_systemd}
%{_unitdir}/php-fpm.service
%if 0%{?fedora} >= 27
%{_unitdir}/httpd.service.d/%{?scl_prefix}php-fpm.conf
%{_unitdir}/nginx.service.d/%{?scl_prefix}php-fpm.conf
%endif
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %ghost /run/php-fpm
%else
%{_initrddir}/php-fpm
%dir %{_localstatedir}/run/php-fpm
%endif
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%if %{with_lsws}
%files litespeed
%{_bindir}/lsphp
%endif

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
%{_libdir}/php-zts/build
%endif
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/zts-php-config.1*
%{macrosdir}/macros.php

%files embedded
%{_libdir}/libphp7.so
%{_libdir}/libphp7-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%license oniguruma_COPYING
%license ucgendat_LICENSE
%files gd -f files.gd
%if ! %{with_libgd}
%license libgd_README
%license libgd_COPYING
%endif
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_COPYING
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files pdo-dblib -f files.pdo_dblib
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files interbase -f files.interbase
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%if %{with_oci8}
%files oci8 -f files.oci8
%endif
%if %{with_zip}
%files zip -f files.zip
%endif
%files json -f files.json


%changelog
* Tue Feb 14 2023 Remi Collet <remi@remirepo.net> - 7.1.33-24
- fix #81744: Password_verify() always return true with some hash
  CVE-2023-0567
- fix #81746: 1-byte array overrun in common path resolve code
  CVE-2023-0568
- fix DOS vulnerability when parsing multipart request body
  CVE-2023-0662

* Mon Dec 19 2022 Remi Collet <remi@remirepo.net> - 7.1.33-23
- pdo: fix #81740: PDO::quote() may return unquoted string
  CVE-2022-31631
- use oracle client library version 21.8

* Tue Sep 27 2022 Remi Collet <remi@remirepo.net> - 7.1.33-22
- phar: fix #81726 DOS when using quine gzip file. CVE-2022-31628
- core: fix #81727 Don't mangle HTTP variable names that clash with ones
  that have a specific semantic meaning. CVE-2022-31629
- use oracle client library version 21.7

* Tue Jun  7 2022 Remi Collet <remi@remirepo.net> - 7.1.33-20
- use oracle client library version 21.6
- mysqlnd: fix #81719: mysqlnd/pdo password buffer overflow. CVE-2022-31626
- pgsql: fix #81720: Uninitialized array in pg_query_params(). CVE-2022-31625

* Mon Nov 15 2021 Remi Collet <remi@remirepo.net> - 7.1.33-19
- Fix #79971 special character is breaking the path in xml function
  CVE-2021-21707

* Wed Oct 20 2021 Remi Collet <remi@remirepo.net> - 7.1.33-18
- fix PHP-FPM oob R/W in root process leading to priv escalation
  CVE-2021-21703
- use libicu version 69
- use oracle client library version 21.3

* Wed Aug 25 2021 Remi Collet <remi@remirepo.net> - 7.1.33-16
- Fix #81211 Symlinks are followed when creating PHAR archive

* Mon Jun 28 2021 Remi Collet <remi@remirepo.net> - 7.1.33-15
- Fix #81122 SSRF bypass in FILTER_VALIDATE_URL
  CVE-2021-21705
- Fix #76448 Stack buffer overflow in firebird_info_cb
- Fix #76449 SIGSEGV in firebird_handle_doer
- Fix #76450 SIGSEGV in firebird_stmt_execute
- Fix #76452 Crash while parsing blob data in firebird_fetch_blob
  CVE-2021-21704

* Wed Apr 28 2021 Remi Collet <remi@remirepo.net> - 7.1.33-13
- Fix #80710 imap_mail_compose() header injection
- use oracle client library version 21.1

* Wed Feb  3 2021 Remi Collet <remi@remirepo.net> - 7.1.33-12
- Fix #80672 Null Dereference in SoapClient
  CVE-2021-21702
- better fix for #77423

* Mon Jan  4 2021 Remi Collet <remi@remirepo.net> - 7.1.33-11
- Fix #77423 FILTER_VALIDATE_URL accepts URLs with invalid userinfo
  CVE-2020-7071

* Tue Sep 29 2020 Remi Collet <remi@remirepo.net> - 7.1.33-10
- Core:
  Fix #79699 PHP parses encoded cookie names so malicious `__Host-` cookies can be sent
  CVE-2020-7070
- OpenSSL:
  Fix #79601 Wrong ciphertext/tag in AES-CCM encryption for a 12 bytes IV
  CVE-2020-7069
  Fix bug #78079 openssl_encrypt_ccm.phpt fails with OpenSSL 1.1.1c

* Tue Aug  4 2020 Remi Collet <remi@remirepo.net> - 7.1.33-9
- Core:
  Fix #79877 getimagesize function silently truncates after a null byte
- Phar:
  Fix #79797 use of freed hash key in the phar_parse_zipfile function
  CVE-2020-7068

* Tue May 12 2020 Remi Collet <remi@remirepo.net> - 7.1.33-8
- Core:
  Fix #78875 Long filenames cause OOM and temp files are not cleaned
  CVE-2019-11048
  Fix #78876 Long variables in multipart/form-data cause OOM and temp
  files are not cleaned

* Tue Apr 14 2020 Remi Collet <remi@remirepo.net> - 7.1.33-7
- standard:
  Fix #79330 shell_exec silently truncates after a null byte
  Fix #79465 OOB Read in urldecode
  CVE-2020-7067

* Tue Mar 17 2020 Remi Collet <remi@remirepo.net> - 7.1.33-6
- standard:
  Fix #79329 get_headers() silently truncates after a null byte
  CVE-2020-7066
- exif:
  Fix #79282 Use-of-uninitialized-value in exif
  CVE-2020-7064
- use oracle client library version 19.6 (18.5 on EL-6)

* Tue Feb 18 2020 Remi Collet <remi@remirepo.net> - 7.1.33-5
- dom:
  Fix #77569 Write Access Violation in DomImplementation
- phar:
  Fix #79082 Files added to tar with Phar::buildFromIterator have all-access permissions
  CVE-2020-7063
- session:
  Fix #79221 Null Pointer Dereference in PHP Session Upload Progress
  CVE-2020-7062

* Thu Jan 23 2020 Remi Collet <remi@remirepo.net> - 7.1.33-4
- mbstring:
  Fix #79037 global buffer-overflow in mbfl_filt_conv_big5_wchar
  CVE-2020-7060
- session:
  Fix #79091 heap use-after-free in session_create_id
- standard:
  Fix #79099 OOB read in php_strip_tags_ex
  CVE-2020-7059

* Tue Dec 17 2019 Remi Collet <remi@remirepo.net> - 7.1.33-2
- bcmath:
  Fix #78878 Buffer underflow in bc_shift_addsub
  CVE-2019-11046
- core:
  Fix #78862 link() silently truncates after a null byte on Windows
  CVE-2019-11044
  Fix #78863 DirectoryIterator class silently truncates after a null byte
  CVE-2019-11045
- exif
  Fix #78793 Use-after-free in exif parsing under memory sanitizer
  CVE-2019-11050
  Fix #78910 Heap-buffer-overflow READ in exif
  CVE-2019-11047
- use oracle client library version 19.5 (18.5 on EL-6)

* Wed Oct 23 2019 Remi Collet <remi@remirepo.net> - 7.1.33-1
- Update to 7.1.33 - http://www.php.net/releases/7_1_33.php

* Wed Aug 28 2019 Remi Collet <remi@remirepo.net> - 7.1.32-1
- Update to 7.1.32 - http://www.php.net/releases/7_1_32.php

* Wed Jul 31 2019 Remi Collet <remi@remirepo.net> - 7.1.31-1
- Update to 7.1.31 - http://www.php.net/releases/7_1_31.php

* Tue Jul  2 2019 Remi Collet <remi@remirepo.net> - 7.1.30-3
- use oracle client library version 19.3
- disable opcache.huge_code_pages in default configuration

* Tue May 28 2019 Remi Collet <remi@remirepo.net> - 7.1.30-1
- Update to 7.1.30 - http://www.php.net/releases/7_1_30.php

* Wed May  1 2019 Remi Collet <remi@remirepo.net> - 7.1.29-1
- Update to 7.1.29 - http://www.php.net/releases/7_1_29.php

* Tue Apr  2 2019 Remi Collet <remi@remirepo.net> - 7.1.28-1
- Update to 7.1.28 - http://www.php.net/releases/7_1_28.php

* Wed Mar  6 2019 Remi Collet <remi@remirepo.net> - 7.1.27-1
- Update to 7.1.27 - http://www.php.net/releases/7_1_27.php
- add upstream patch for OpenSSL 1.1.1b

* Wed Jan  9 2019 Remi Collet <remi@remirepo.net> - 7.1.26-1
- Update to 7.1.26 - http://www.php.net/releases/7_1_26.php

* Sat Dec  8 2018 Remi Collet <remi@remirepo.net> - 7.1.25-2
- Fix null pointer dereference in imap_mail CVE-2018-19935

* Wed Dec  5 2018 Remi Collet <remi@remirepo.net> - 7.1.25-1
- Update to 7.1.25 - http://www.php.net/releases/7_1_25.php

* Thu Nov 22 2018 Remi Collet <remi@remirepo.net> - 7.1.25~RC1-1
- update to 7.1.25RC1

* Wed Nov  7 2018 Remi Collet <remi@remirepo.net> - 7.1.24-1
- Update to 7.1.24 - http://www.php.net/releases/7_1_24.php

* Wed Oct 24 2018 Remi Collet <remi@remirepo.net> - 7.1.24~RC1-2
- FPM: add getallheaders, backported from 7.3

* Wed Oct 24 2018 Remi Collet <remi@remirepo.net> - 7.1.24~RC1-1
- update to 7.1.24RC1

* Wed Oct 10 2018 Remi Collet <remi@remirepo.net> - 7.1.23-1
- Update to 7.1.23 - http://www.php.net/releases/7_1_23.php

* Sat Sep 29 2018 Remi Collet <remi@remirepo.net> - 7.1.23~RC1-1
- update to 7.1.23RC1
- use oracle client library version 18.3

* Wed Sep 12 2018 Remi Collet <remi@remirepo.net> - 7.1.22-1
- Update to 7.1.22 - http://www.php.net/releases/7_1_22.php

* Thu Aug 30 2018 Remi Collet <remi@remirepo.net> - 7.1.22~RC1-1
- update to 7.1.22RC1

* Wed Aug 15 2018 Remi Collet <remi@remirepo.net> - 7.1.21-1
- Update to 7.1.21 - http://www.php.net/releases/7_1_21.php

* Thu Jul 19 2018 Remi Collet <remi@remirepo.net> - 7.1.20-1
- Update to 7.1.20 - http://www.php.net/releases/7_1_20.php

* Fri Jul  6 2018 Remi Collet <remi@remirepo.net> - 7.1.20~RC1-1
- update to 7.1.20RC1

* Thu Jun 21 2018 Remi Collet <remi@remirepo.net> - 7.1.19-1
- Update to 7.1.19 - http://www.php.net/releases/7_1_19.php

* Thu Jun  7 2018 Remi Collet <remi@remirepo.net> - 7.1.19~RC1-1
- update to 7.1.19RC1

* Thu May 24 2018 Remi Collet <remi@remirepo.net> - 7.1.18-1
- Update to 7.1.18 - http://www.php.net/releases/7_1_18.php

* Mon May 14 2018 Remi Collet <remi@remirepo.net> - 7.1.18~RC1-2
- rebuild against EL 7.5

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 7.1.18~RC1-1
- update to 7.1.18RC1

* Wed Apr 25 2018 Remi Collet <remi@remirepo.net> - 7.1.17-1
- Update to 7.1.17 - http://www.php.net/releases/7_1_17.php

* Wed Mar 28 2018 Remi Collet <remi@remirepo.net> - 7.1.16-1
- Update to 7.1.16 - http://www.php.net/releases/7_1_16.php
- FPM: update default pool configuration for process.dumpable

* Wed Mar 21 2018 Remi Collet <remi@remirepo.net> - 7.1.16~RC1-3
- use systemd RuntimeDirectory instead of /etc/tmpfiles.d

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 7.1.16~RC1-2
- add file trigger to restart the php-fpm service
  when new pool or new extension installed (F27+)

* Wed Mar 14 2018 Remi Collet <remi@remirepo.net> - 7.1.16~RC1-1
- Update to 7.1.16RC1

* Wed Feb 28 2018 Remi Collet <remi@remirepo.net> - 7.1.15-1
- Update to 7.1.15 - http://www.php.net/releases/7_1_15.php
- FPM: revert pid file removal

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.1.15~RC1-1
- Update to 7.1.15RC1
- adapt ldap patch

* Wed Jan 31 2018 Remi Collet <remi@remirepo.net> - 7.1.14-1
- Update to 7.1.14 - http://www.php.net/releases/7_1_14.php

* Wed Jan 17 2018 Remi Collet <remi@remirepo.net> - 7.1.14~RC1-1
- Update to 7.1.14RC1
- define SOURCE_DATE_EPOCH for reproducible build

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.1.13-3
- rebuild for gdbm 1.13 (1.14 was reverted)

* Wed Jan 10 2018 Remi Collet <remi@remirepo.net> - 7.1.13-2
- rebuild for gdbm 1.14 BC break (see rhbz#1532997)

* Wed Jan  3 2018 Remi Collet <remi@remirepo.net> - 7.1.13-1
- Update to 7.1.13 - http://www.php.net/releases/7_1_13.php

* Wed Dec  6 2017 Remi Collet <remi@remirepo.net> - 7.1.13~RC1-1
- Update to 7.1.13RC1

* Fri Dec  1 2017 Remi Collet <remi@remirepo.net> - 7.1.12-4
- add upstream patch for https://bugs.php.net/75573

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.1.12-3
- refresh patch for https://bugs.php.net/75514

* Wed Nov 22 2017 Remi Collet <remi@remirepo.net> - 7.1.12-2
- Update to 7.1.12 - http://www.php.net/releases/7_1_12.php

* Mon Nov 13 2017 Remi Collet <remi@remirepo.net> - 7.1.12~RC1-2
- test build for https://bugs.php.net/75514

* Tue Nov  7 2017 Remi Collet <remi@remirepo.net> - 7.1.12~RC1-1
- Update to 7.1.12RC1

* Wed Oct 25 2017 Remi Collet <remi@remirepo.net> - 7.1.11-1
- Update to 7.1.11 - http://www.php.net/releases/7_1_11.php

* Wed Oct 11 2017 Remi Collet <remi@remirepo.net> - 7.1.11~RC1-1
- Update to 7.1.11RC1
- oci8 version is now 2.1.8

* Wed Sep 27 2017 Remi Collet <remi@remirepo.net> - 7.1.10-1
- Update to 7.1.10 - http://www.php.net/releases/7_1_10.php

* Mon Sep 25 2017 Remi Collet <remi@remirepo.net> - 7.1.10~RC1-3
- F27: php now requires php-fpm and start it with httpd / nginx

* Thu Sep 14 2017 Remi Collet <remi@remirepo.net> - 7.1.10~RC1-2
- update builder from RHEL 7.3 to RHEL 7.4

* Wed Sep 13 2017 Remi Collet <remi@remirepo.net> - 7.1.10~RC1-1
- Update to 7.1.10RC1
- Automatically load OpenSSL configuration file, from PHP 7.2

* Thu Aug 31 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9-2
- add patch for EL-6, fix undefined symbol: sqlite3_errstr

* Wed Aug 30 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9-1
- Update to 7.1.9 - http://www.php.net/releases/7_1_9.php

* Tue Aug 22 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9~RC1-2
- disable httpd MPM check
- php-fpm: drop unneeded "pid" from default configuration

* Wed Aug 16 2017 Remi Collet <remi@fedoraproject.org> - 7.1.9~RC1-1
- Update to 7.1.9RC1
- oci8 version is now 2.1.7

* Wed Aug  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8-2
- add patch for EL-6, fix undefined symbol: sqlite3_errstr

* Wed Aug  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8-1
- Update to 7.1.8 - http://www.php.net/releases/7_1_8.php

* Tue Jul 18 2017 Remi Collet <remi@fedoraproject.org> - 7.1.8~RC1-1
- Update to 7.1.8RC1
- oci8 version is now 2.1.6

* Thu Jul  6 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7-1
- Update to 7.1.7 - http://www.php.net/releases/7_1_7.php

* Wed Jun 21 2017 Remi Collet <remi@fedoraproject.org> - 7.1.7~RC1-1
- Update to 7.1.7RC1
- oci8 version is now 2.1.5
- use oracle instant client version 12.2

* Wed Jun  7 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6-1
- Update to 7.1.6 - http://www.php.net/releases/7_1_6.php
- add upstream security patches for oniguruma

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 7.1.6~RC1-1
- Update to 7.1.6RC1

* Tue May  9 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5-1
- Update to 7.1.5 - http://www.php.net/releases/7_1_5.php

* Thu Apr 27 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5~RC1-2
- new sources from new tag

* Tue Apr 25 2017 Remi Collet <remi@fedoraproject.org> - 7.1.5~RC1-1
- Update to 7.1.5RC1
- oci8 version is now 2.1.4

* Tue Apr 11 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-1
- Update to 7.1.4 - http://www.php.net/releases/7_1_4.php

* Tue Mar 28 2017 Remi Collet <remi@fedoraproject.org> - 7.1.4-0.1.RC1
- Update to 7.1.4RC1

* Tue Mar 14 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-1
- Update to 7.1.3 - http://www.php.net/releases/7_1_3.php

* Fri Mar 10 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-0.2.RC1
- fix interbase build on F26

* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 7.1.3-0.1.RC1
- Update to 7.1.3RC1

* Wed Feb 15 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-1
- Update to 7.1.2 - http://www.php.net/releases/7_1_2.php

* Thu Feb  2 2017 Remi Collet <remi@fedoraproject.org> - 7.1.2-0.2.RC1
- Update to 7.1.2RC1 (new sources)

* Wed Feb  1 2017 Remi Collet <remi@fedoraproject.org> 7.1.2-0.1.RC1
- Update to 7.1.2RC1

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-3
- EL-7: add patch for https://bugs.php.net/73956
- switch back to gcc 6.2

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-2
- EL-7: rebuild using gcc 4.8 instead of 6.2
  because of https://bugzilla.redhat.com/1414348

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-1
- Update to 7.1.1 - http://www.php.net/releases/7_1_1.php

* Thu Jan  5 2017 Remi Collet <remi@fedoraproject.org> 7.1.1-0.1.RC1
- Update to 7.1.1RC1

* Mon Dec 26 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-2
- test optimized build using GCC 6.2

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-1
- Update to 7.1.0 - http://www.php.net/releases/7_1_0.php
- use bundled pcre library 8.38 on EL-7
- disable pcre.jit everywhere as it raise AVC #1398474
- sync provided configuration with upstream production defaults

* Wed Nov  9 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.8.RC6
- Update to 7.1.0RC6

* Wed Oct 26 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.7.RC5
- Update to 7.1.0RC5

* Mon Oct 17 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.6.RC4
- Update to 7.1.0RC4
- update tzdata patch to v14, improve check for valid tz file
- oci8 version is now 2.1.3

* Thu Sep 29 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.5.RC3
- Update to 7.1.0RC3

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.4.RC2
- Update to 7.1.0RC2
- API version is now 20160303

* Thu Sep  1 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.3.RC1
- Update to 7.1.0RC1
- oci8 version is now 2.1.2
- json version is now 1.5.0

* Wed Aug  3 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.2.beta2
- Update to 7.1.0beta2

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> 7.1.0-0.1.beta1
- Update to 7.1.0beta1

* Wed Jul 20 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-1
- Update to 7.0.9 - http://www.php.net/releases/7_0_9.php
- wddx: add upstream patch for https://bugs.php.net/72564

* Wed Jul  6 2016 Remi Collet <remi@fedoraproject.org> 7.0.9-0.1.RC1
- Update to 7.0.9RC1

* Thu Jun 30 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-1.1
- own tests/doc directories for pecl packages (f24)

* Wed Jun 22 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-1
- Update to 7.0.8 - http://www.php.net/releases/7_0_8.php

* Wed Jun  8 2016 Remi Collet <remi@fedoraproject.org> 7.0.8-0.1.RC1
- Update to 7.0.8RC1
- opcache version is now php version

* Wed May 25 2016 Remi Collet <remi@fedoraproject.org> 7.0.7-1
- Update to 7.0.7 - http://www.php.net/releases/7_0_7.php

* Thu May 12 2016 Remi Collet <remi@fedoraproject.org> 7.0.7-0.1.RC1
- Update to 7.0.7RC1
- oci8 version is now 2.1.1

* Thu Apr 28 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-3
- Update to 7.0.6 - http://www.php.net/releases/7_0_6.php
- rebuild for new sources

* Wed Apr 27 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-1
- Update to 7.0.6
  http://www.php.net/releases/7_0_6.php

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> 7.0.6-0.1.RC1
- Update to 7.0.6RC1

* Fri Apr  8 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-2
- Fixed bug #71914 (Reference is lost in "switch")

* Wed Mar 30 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-1
- Update to 7.0.5
  http://www.php.net/releases/7_0_5.php

* Wed Mar 16 2016 Remi Collet <remi@fedoraproject.org> 7.0.5-0.1.RC1
- Update to 7.0.5RC1

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-2
- adapt for F24: define %%pecl_xmldir and own it

* Wed Mar  2 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-1
- Update to 7.0.4
  http://www.php.net/releases/7_0_4.php
- pcre: disables JIT compilation of patterns with system pcre < 8.38

* Thu Feb 18 2016 Remi Collet <remi@fedoraproject.org> 7.0.4-0.1.RC1
- Update to 7.0.4RC1

* Wed Feb  3 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-1
- Update to 7.0.3
  http://www.php.net/releases/7_0_3.php

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-0.2.RC1
- FPM: test build for https://bugs.php.net/62172

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> 7.0.3-0.1.RC1
- Update to 7.0.3RC1

* Wed Jan  6 2016 Remi Collet <remi@fedoraproject.org> 7.0.2-1
- Update to 7.0.2
  http://www.php.net/releases/7_0_2.php

* Sun Dec 27 2015 Remi Collet <remi@fedoraproject.org> 7.0.2-0.1.RC1
- Update to 7.0.2RC1
- opcache: build with --disable-huge-code-pages on EL-6

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> 7.0.1-1
- Update to 7.0.1
  http://www.php.net/releases/7_0_1.php
- curl: add CURL_SSLVERSION_TLSv1_x constant (EL)

* Wed Dec  9 2015 Remi Collet <remi@fedoraproject.org> 7.0.1-0.1.RC1
- Update to 7.0.1RC1
- drop --disable-huge-code-pages build option on EL-6,
  but keep it disabled in default configuration
- php-devel obsoletes php-pecl-jsonc-devel

* Sat Dec  5 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-3
- EL-6 rebuild

* Thu Dec  3 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-2
- build with --disable-huge-code-pages on EL-6

* Tue Dec  1 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-1
- Update to 7.0.0
  http://www.php.net/releases/7_0_0.php

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.16.RC8
- set opcache.huge_code_pages=0 on EL-6
  see  https://bugs.php.net/70973 and https://bugs.php.net/70977

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.12.RC8
- Update to 7.0.0RC8
- set opcache.huge_code_pages=1 on x86_64

* Thu Nov 12 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.11.RC7
- Update to 7.0.0RC7 (retagged)

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.10.RC7
- Update to 7.0.0RC7

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.9.RC6
- Update to 7.0.0RC6

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.8.RC5
- rebuild as retagged

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.7.RC5
- Update to 7.0.0RC5
- update php-fpm.d/www.conf comments
- API and Zend API are now set to 20151012

* Wed Sep 30 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.6.RC4
- Update to 7.0.0RC4
- php-fpm: set http authorization headers

* Wed Sep 16 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.5.RC3
- Update to 7.0.0RC3
- disable zip extension (provided in php-pecl-zip)

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.4.RC2
- Update to 7.0.0RC2
- enable oci8 and pdo_oci extensions
- sync php.ini with upstream php.ini-production

* Sat Aug 22 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.3.RC1
- Update to 7.0.0RC1

* Wed Aug  5 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.2.beta3
- update to 7.0.0beta3

* Thu Jul 23 2015 Remi Collet <remi@fedoraproject.org> 7.0.0-0.1.beta2
- update to 7.0.0beta2
- merge changes from php70-php spec file

* Sun Jul 12 2015 Remi Collet <remi@fedoraproject.org> 5.6.11-1
- Update to 5.6.11
  http://www.php.net/releases/5_6_11.php

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-1.1
- don't provide php-sqlite3 on EL-5
- the phar link is now correctly created
- avoid issue when 2 builds run simultaneously

* Thu Jun 11 2015 Remi Collet <remi@fedoraproject.org> 5.6.10-1
- Update to 5.6.10
  http://www.php.net/releases/5_6_10.php
- opcache is now 7.0.6-dev

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> 5.6.9-1
- Update to 5.6.9
  http://www.php.net/releases/5_6_9.php

* Thu Apr 16 2015 Remi Collet <remi@fedoraproject.org> 5.6.8-1
- Update to 5.6.8
  http://www.php.net/releases/5_6_8.php

* Fri Apr 10 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-2
- add upstream patch to drop SSLv3 tests

* Thu Mar 19 2015 Remi Collet <remi@fedoraproject.org> 5.6.7-1
- Update to 5.6.7
  http://www.php.net/releases/5_6_7.php

* Fri Feb 20 2015 Remi Collet <remi@fedoraproject.org> 5.6.6-1.1
- rebuild for new tokyocabinet in EL-5

* Thu Feb 19 2015 Remi Collet <remi@fedoraproject.org> 5.6.6-1
- Update to 5.6.6
  http://www.php.net/releases/5_6_6.php

* Wed Jan 21 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-1
- Update to 5.6.5
  http://www.php.net/releases/5_6_5.php

* Fri Jan  9 2015 Remi Collet <remi@fedoraproject.org> 5.6.5-0.1.RC1
- update to 5.6.5RC1
- FPM: enable ACL for Unix Domain Socket

* Wed Dec 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-2
- Update to 5.6.4
  http://www.php.net/releases/5_6_4.php
- add sybase_ct extension (in mssql sub-package)
- xmlrpc requires xml

* Wed Dec 10 2014 Remi Collet <remi@fedoraproject.org> 5.6.4-1
- Update to 5.6.4
  http://www.php.net/releases/5_6_4.php

* Thu Nov 27 2014 Remi Collet <rcollet@redhat.com> 5.6.4-0.1.RC1
- php 5.6.4RC1

* Sun Nov 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-3
- FPM: add upstream patch for https://bugs.php.net/68421
  access.format=R doesn't log ipv6 address
- FPM: add upstream patch for https://bugs.php.net/68420
  listen=9000 listens to ipv6 localhost instead of all addresses
- FPM: add upstream patch for https://bugs.php.net/68423
  will no longer load all pools

* Thu Nov 13 2014 Remi Collet <remi@fedoraproject.org> 5.6.3-1
- Update to PHP 5.6.3
  http://php.net/releases/5_6_3.php
- GMP: add upstream patch for https://bugs.php.net/68419
  Fix build with libgmp < 4.2

* Thu Oct 30 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.4.RC1
- php 5.6.3RC1 (refreshed, phpdbg changes reverted)

* Thu Oct 30 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.3.RC1
- new version of systzdata patch, fix case sensitivity
- ignore Factory in date tests

* Wed Oct 29 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.2.RC1
- php 5.6.3RC1 (refreshed)
- enable phpdbg_webhelper new extension (in php-dbg)

* Tue Oct 28 2014 Remi Collet <rcollet@redhat.com> 5.6.3-0.1.RC1
- php 5.6.3RC1
- disable opcache.fast_shutdown in default config
- disable phpdbg_webhelper new extension for now

* Thu Oct 16 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.2
  http://php.net/releases/5_6_2.php

* Fri Oct  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.1-1
- Update to PHP 5.6.1
  http://php.net/releases/5_6_1.php

* Fri Sep 26 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0
- test build for upcoming 5.6.1
- use default system cipher list by Fedora policy
  http://fedoraproject.org/wiki/Changes/CryptoPolicy

* Wed Sep 24 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.2.RC1
- provides nginx configuration (see #1142298)

* Fri Sep 12 2014 Remi Collet <rcollet@redhat.com> 5.6.1-0.1.RC1
- php 5.6.1RC1

* Wed Sep  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.2
- ensure gd-last 2.1.0-3, with libvpx support, is used

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.1
- enable libvpx on EL 6 (with libvpx 1.3.0)

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1
- PHP 5.6.0 is GA
- fix ZTS man pages, upstream patch for 67878

* Wed Aug 20 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.22.RC4
- backport rawhide stuff for F21+ and httpd-filesystem
  with support for SetHandler to proxy_fcgi

* Thu Aug 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.21.RC4
- php 5.6.0RC4

* Wed Jul 30 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.20.RC3
- php 5.6.0RC3
- fix license handling
- fix zts-php-config --php-binary output #1124605
- cleanup with_libmysql
- add php-litespeed subpackage (/usr/bin/lsphp)

* Fri Jul 25 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.18.RC2
- dont display timezone version in phpinfo (tzdata patch v11)

* Sat Jul 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.17.RC2
- test build for #67635

* Mon Jul  7 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.16.RC2
- php 5.6.0RC2

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.15.RC1
- add workaround for unserialize/mock issue from 5.4/5.5

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.14.RC1
- fix phpdbg with libedit https://bugs.php.net/67499

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.13.RC1
- php 5.6.0RC1

* Mon Jun 16 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.12.beta4
- test build for serialize

* Tue Jun 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.11.beta4
- test build for bug 67410, 67411, 67412, 67413
- fix 67392, dtrace breaks argument unpack

* Thu Jun  5 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.10.beta4
- fix regression introduce in fix for #67118

* Wed Jun  4 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.9.beta4
- php 5.6.0beta4

* Wed May 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.beta3
- php 5.6.0beta3

* Tue May  6 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.201405061030
- new snapshot php5.6-201405061030

* Sat May  3 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.7.beta2
- php 5.6.0beta2

* Thu Apr 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.6.beta1
- php 5.6.0beta1

* Wed Apr  9 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.5.201404090430
- new snapshot php5.6-201404090430
- add numerical prefix to extension configuration files
- prevent .user.ini files from being viewed by Web clients
- load php directives only when mod_php is active

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403261230
- new snapshot php5.6-201403261230
- oci8 version 2.0.9
- opcache version 7.0.4-dev

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403170630
- new snapshot php5.6-201403170630

* Wed Mar 12 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.3.201403120830
- new snapshot php5.6-201403120830
- rebuild against gd-last without libvpx on EL < 7
- oci8 version 2.0.8

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.2.alpha3
- php 5.6.0alpha3
- add php-dbg subpackage
- update php.ini from upstream production template
- move /usr/bin/zts-php to php-cli subpackage

* Wed Feb 26 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.4.RC1
- php-fpm should own /var/lib/php/session and wsdlcache

* Tue Feb 25 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.3.RC1
- test build for https://bugs.php.net/66762

* Fri Feb 21 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.2.RC1
- another test build of 5.5.10RC1
- fix memleak in fileinfo ext
- revert test changes for pcre 8.34

* Thu Feb 20 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.1.RC1
- test build of 5.5.10RC1

* Tue Feb 18 2014 Remi Collet <rcollet@redhat.com> 5.5.9-2
- upstream patch for https://bugs.php.net/66731

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> 5.5.9-1
- Update to 5.5.9
  http://www.php.net/ChangeLog-5.php#5.5.9
- Install macros to /usr/lib/rpm/macros.d where available.
- Add configtest option to php-fpm ini script (EL)

* Thu Jan 23 2014 Remi Collet <rcollet@redhat.com> 5.5.9-0.1.RC1
- test build of 5.5.9RC1

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 5.5.8-2
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Jan 20 2014 Remi Collet <rcollet@redhat.com> 5.5.8-2
- test build for https://bugs.php.net/66412

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-1
- update to 5.5.8
- drop conflicts with other opcode caches as both can
  be used only for user data cache

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-0.2.RC1
- another test build of 5.5.8RC1

* Sat Dec 28 2013 Remi Collet <rcollet@redhat.com> 5.5.8-0.1.RC1
- test build of 5.5.8RC1

* Fri Dec 20 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1.1
- test build for https://bugs.php.net/66331

* Wed Dec 11 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1
- update to 5.5.7, fix for CVE-2013-6420
- fix zend_register_functions breaks reflection, php bug 66218
- fix Heap buffer over-read in DateInterval, php bug 66060
- fix fix overflow handling bug in non-x86

* Tue Dec 10 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.4.RC1
- test build

* Wed Dec 04 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.3.RC1
- test build

* Mon Dec 02 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.2.RC1
- test build for https://bugs.php.net/66218
  zend_register_functions breaks reflection

* Thu Nov 28 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.1.RC1
- test build of 5.5.7RC1

* Wed Nov 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-1
- update to 5.5.6

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.7
- update to 5.5.6, test build

* Fri Nov  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.6.RC1
- add --with debug option for debug build

* Wed Nov  6 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.5.RC1
- test buid with opcache changes reverted

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.4.RC1
- test build opcache with phar build shared
  https://github.com/zendtech/ZendOptimizerPlus/issues/147

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.3.RC1
- build phar shared, opcache loaded with RTLD_LAZY

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.2.RC1
- build phar static for opcache dep.

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.1.RC1
- test build of 5.5.6RC1

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> 5.5.5-2
- rebuild using libicu-last 50.1.2

* Tue Oct 15 2013 Remi Collet <rcollet@redhat.com> - 5.5.5-1
- update to 5.5.5

* Mon Sep 23 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-2
- test build

* Thu Sep 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-1
- update to 5.5.4
- improve security, use specific soap.wsdl_cache_dir
  use /var/lib/php/wsdlcache for mod_php and php-fpm
- sync short_tag comments in php.ini with upstream

* Fri Aug 30 2013 Remi Collet <rcollet@redhat.com> - 5.5.4.0.1-201308300430
- test build with -fsanitize=address
- test build for https://bugs.php.net/65564

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-1
- update to 5.5.3
- build without zip extension, requires php-pecl-zip
- fix typo and add missing entries in php.ini

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-0
- update to 5.5.3
- test build without zip extension
- fix typo and add missing entries in php.ini

* Mon Aug 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.2-1
- update to 5.5.2

* Thu Aug  8 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.2.RC1
- improve system libzip patch

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.1.RC1
- 5.5.2RC1

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 5.5.1-2
- test build with oracle instantclient 12.1

* Mon Jul 22 2013 Remi Collet <rcollet@redhat.com> - 5.5.1-1
- update to 5.5.1
- add Provides: php(pdo-abi), for consistency with php(api)
  and php(zend-abi)
- improved description for mod_php
- fix opcache ZTS configuration (blacklists in /etc/php-zts.d)
- add missing man pages (phar, php-cgi)
- fix php-enchant summary and description

* Fri Jul 12 2013 Remi Collet <rcollet@redhat.com> - 5.5.0-2
- add security fix for CVE-2013-4113
- add missing ASL 1.0 license
- 32k stack size seems ok for tests on both 32/64bits build

* Mon Jun 24 2013 Remi Collet <rcollet@redhat.com> 5.5.1-0.1.201306240630
- test build (bundled libgd)

* Thu Jun 20 2013 Remi Collet <rcollet@redhat.com> 5.5.0-1
- update to 5.5.0 final

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.11.RC3
- also drop JSON from sources
- clean conditional for JSON (as removed from the sources)
- clean conditional for FPM (always build)

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3.1
- EL-5 rebuild with gd-last

* Thu Jun 13 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3
- drop JSON extension
- build with system GD when 2.1.0 is available

* Thu Jun  6 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.35.RC3
- update to 5.5.0RC3

* Mon May 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.34.201305271230.
-test build with systemd gd

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.33.RC2
- update to 5.5.0RC2
- add missing options in php-fpm.conf
- improved systemd configuration, documentation about
  /etc/sysconfig/php-fpm being deprecated

* Wed May 22 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305220430
- test build for https://bugs.php.net/64895

* Sat May 18 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305181030
- test build with systemd integration (type=notify)

* Wed May  8 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.31.RC1
- update to 5.5.0RC1

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.30.201305041230
- test build for libgd

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.29.201304291030
- new snapshot
- review some sub-packages description
- add option to disable json extension

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.28.beta4
- update to 5.5.0beta4, rebuild with new sources

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.27.beta4
- update to 5.5.0beta4

* Mon Apr 22 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.27-201304221230
- new snapshot
- try build with system gd 2.1.0

* Thu Apr 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.26-201304181030
- new snapshot
- zend_extension doesn't requires full path
- refresh system libzip patch
- drop opcache patch merged upstream

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.25.beta3
- allow wildcard in opcache.blacklist_filename and provide
  default /etc/php.d/opcache-default.blacklist

* Wed Apr 10 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.24.beta3
- update to 5.5.0beta3

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.23-201304040630
- new snapshot
- clean old deprecated options

* Thu Mar 28 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.22.beta2
- update to 5.5.0beta2
- Zend Optimizer+ renamed to Zend OPcache
- sync provided configuration with upstream

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.21-201303251230
- new snapshot
- generated parser using system bison, test for https://bugs.php.net/64503

* Wed Mar 20 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.20-201303201430
- new snapshot (beta1)

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.19-201303180830
- new snapshot
- temporary disable dtrace
- new extension opcache in php-opccache sub-package

* Thu Mar 14 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.18-201303141230
- new snapshot
- hardened build (links with -z now option)
- remove %%config from /etc/rpm/macros.php

* Fri Mar  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.17-201303081230
- new snapshot (post alpha 6)
- make php-mysql package optional (and disabled)
- make ZTS build optional (still enabled)

* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302281430
- new snapshot

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302211230
- new snapshot (post alpha 5)

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302131030
- enable tokyocabinet and gdbm dba handlers

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.15-201302121230
- new snapshot

* Mon Feb  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302040630
- new snapshot

* Fri Feb  1 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302010630
- new snapshot

* Mon Jan 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.13-201301281030
- new snapshot
- don't display XFAIL tests in report

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.12-201301230630
- new snapshot, alpha4

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.11-201301170830
- new snapshot
- fix php.conf to allow MultiViews managed by php scripts

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301100830
- new snapshot, alpha3

* Wed Jan  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301021430
- new snapshot

* Mon Dec 24 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212241030
- new snapshot (post alpha2)
- use xz compressed tarball

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212181230
- new snapshot

* Wed Dec 12 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212121430
- new snapshot

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212110630
- patch for unpack

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.7.201212110630
- prevent php_config.h changes across (otherwise identical) rebuilds
- drop "Configure Command" from phpinfo output

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212110630
- new snapshot
- move gmp in new sub-package

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212100830
- build sockets, tokenizer extensions shared

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.5.201212100830
- new snapshot
- enable dtrace

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.4.201211301534
- build simplexml and xml extensions shared (in php-xml)
- build bz2, calendar, ctype, exif, ftp, gettext and iconv
  extensions shared (in php-common)
- build gmp extension shared (in php-bcmath)
- build shmop extension shared (in php-process)

* Mon Dec  3 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.3.201211301534
- drop some old compatibility provides (php-api, php-zend-abi, php-pecl-*)
- obsoletes php55-*

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.2.201211301534
- update to have zend_execute_ex for xDebug

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.1.201211300857
- Initial work on 5.5.0-dev

* Fri Nov 23 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-2
- add patch for https://bugs.php.net/63588
  duplicated implementation of php_next_utf8_char

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-1
- update to 5.4.9

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.5.RC1
- switch back to upstream generated scanner/parser

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.4.RC1
- use _httpd_contentdir macro and fix php.gif path

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.3.RC1
- improve system libzip patch to use pkg-config

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.2.RC1
- use _httpd_moddir macro

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- improves php.conf (use FilesMatch + SetHandler)
- improves filter (httpd module)
- apply ldap_r patch on fedora >= 18 only

* Fri Nov  9 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.2.RC1
- sync with rawhide

* Fri Nov  9 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- clarify Licenses
- missing provides xmlreader and xmlwriter
- modernize spec

* Thu Nov  8 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- change php embedded library soname version to 5.4

* Tue Nov  6 2012 Remi Collet <rcollet@redhat.com> 5.4.8-5
- fix _httpd_mmn macro definition

* Mon Nov  5 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix mysql_sock macro definition

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- fix installed headers

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 5.4.8-2
- use libldap_r for ldap extension

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-1
- update to 5.4.8
- define both session.save_handler and session.save_path
- fix possible segfault in libxml (#828526)
- php-fpm: create apache user if needed
- use SKIP_ONLINE_TEST during make test
- php-devel requires pcre-devel and php-cli (instead of php)

* Fri Oct  5 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-0.3.RC1
- provides php-phar

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.2.RC1
- update systzdata patch to v10, timezone are case insensitive

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.1.RC1
- update to 5.4.8RC1

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-10
- fix typo in systemd macro

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-9
- php-fpm: enable PrivateTmp
- php-fpm: new systemd macros (#850268)
- php-fpm: add upstream patch for startup issue (#846858)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 5.4.7-8
- systemd integration, https://bugs.php.net/63085
- no odbc call during timeout, https://bugs.php.net/63171
- check sqlite3_column_table_name, https://bugs.php.net/63149

* Mon Sep 24 2012 Remi Collet <rcollet@redhat.com> 5.4.7-7
- most failed tests explained (i386, x86_64)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-6
- fix for http://bugs.php.net/63126 (#783967)

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-6
- add --daemonize / --nodaemonize options to php-fpm
  upstream RFE: https://bugs.php.net/63085

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-5
- sync with rawhide
- patch to report libdb version https://bugs.php.net/63117

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-5
- patch to ensure we use latest libdb (not libdb4)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- really fix rhel tests (use libzip and libdb)

* Tue Sep 18 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- fix test to enable zip extension on RHEL-7

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-2
- remove session.save_path from php.ini
  move it to apache and php-fpm configuration files

* Fri Sep 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-1
- update to 5.4.7
  http://www.php.net/releases/5_4_7.php
- php-fpm: don't daemonize

* Thu Sep 13 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-1
- update to 5.4.7

* Mon Sep  3 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.2.RC1
- obsoletes php53* and php54*

* Fri Aug 31 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.1.RC1
- update to 5.4.7RC1

* Mon Aug 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-2
- enable php-fpm on secondary arch (#849490)

* Thu Aug 16 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-1
- update to 5.4.6

* Thu Aug 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.6-0.1.RC1
- update to 5.4.6RC1

* Fri Jul 20 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-1
- update to 5.4.5

* Sat Jul 07 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.2.RC1
- update patch for system libzip

* Wed Jul 04 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.1.RC1
- update to 5.4.5RC1 with bundled libzip.

* Mon Jul 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-4
- use system pcre only on fedora >= 14 (version 8.10)
- drop BR for libevent (#835671)
- provide php(language) to allow version check
- define %%{php_version}

* Thu Jun 21 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-2
- clean spec, sync with rawhide
- add missing provides (core, ereg, filter, standard)

* Wed Jun 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-1
- update to 5.4.4 finale
- fedora >= 15: use /usr/lib/tmpfiles.d instead of /etc/tmpfiles.d
- fedora >= 15: use /run/php-fpm instead of /var/run/php-fpm

* Thu May 31 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.2.RC2
- update to 5.4.4RC2

* Thu May 17 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.1.RC1
- update to 5.4.4RC1

* Wed May 09 2012 Remi Collet <Fedora@famillecollet.com> 5.4.3-1
- update to 5.4.3 (CVE-2012-2311, CVE-2012-2329)

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> 5.4.2-1
- update to 5.4.2 (CVE-2012-1823)

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-1
- update to 5.4.1
- use libdb in fedora >= 18 instead of db4

* Fri Apr 13 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.3.RC2
- update to 5.4.1RC2

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.2.RC1
- rebuild

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.1.RC1
- update to 5.4.1RC1, split php conf when httpd 2.4

* Tue Mar 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1.1
- sync with rawhide (httpd 2.4 stuff)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-2
- rebuild against httpd 2.4
- use _httpd_mmn, _httpd_apxs macros
- fix --without-system-tzdata build for Debian et al

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1
- update to PHP 5.4.0 finale

* Sat Feb 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.16.RC8
- update to 5.4.0RC8

* Sat Feb 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.15.RC7
- update to 5.4.0RC7

* Fri Jan 27 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.14.RC6
- build against system libzip (fedora >= 17), patch from spot

* Thu Jan 26 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.13.RC6
- add /etc/sysconfig/php-fpm environment file (#784770)

* Wed Jan 25 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.12.RC6
- keep all ZTS binaries in /usr/bin (with zts prefix)

* Thu Jan 19 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.11.RC6
- update to 5.4.0RC6

* Wed Jan 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.10.RC5
- add some fedora patches back (dlopen, easter, phpize)

* Mon Jan 16 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.9.RC5
- improves mysql.sock default path

* Fri Jan 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.8.RC5
- update to 5.4.0RC5
- patch for https://bugs.php.net/60748 (mysql.sock hardcoded)
- move session.path from php.ini to httpd/conf.d/php.conf
- provides both ZTS mysql extensions (libmysql/mysqlnd)
- build php cli ZTS binary, in -devel, mainly for test

* Wed Jan 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.7.201201041830
- new snapshot (5.4.0RC5-dev) with fix for https://bugs.php.net/60627

* Fri Dec 30 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112300630
- new snapshot (5.4.0RC5-dev)

* Mon Dec 26 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112261030
- new snapshot (5.4.0RC5-dev)

* Sat Dec 17 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.5.201112170630
- new snapshot (5.4.0RC4-dev)

* Mon Dec 12 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.4.201112121330
- new snapshot (5.4.0RC4-dev)
- switch to systemd

* Fri Dec 09 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201112091730
- new snapshot (5.4.0RC4-dev)
- removed patch merged upstream for https://bugs.php.net/60392
- clean ini (from upstream production default)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111260730
- new snapshot (5.4.0RC3-dev)
- patch for https://bugs.php.net/60392 (old libicu on EL-5)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111130730
- new snapshot (5.4.0RC2-dev)
- sync with latest changes in 5.3 spec

* Thu Sep 08 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.2.201109081430
- new snapshot
- build mysql/mysqli against both libmysql and mysqlnd (new mysqlnd sub-package)

* Sat Sep 03 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.1.201109031230
- first work on php 5.4
- remove -sqlite subpackage
- move php/modules-zts to php-zts/modules

