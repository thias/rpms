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
%global apiver      20240924
%global zendver     20240924
%global pdover      20240423
# Extension version
%global fileinfover 1.0.5
%global zipver      1.22.6

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 8.4

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Build for LiteSpeed Web Server (LSAPI), you can disable using --without tests
%bcond_without        lsws

# Regression tests take a long time, you can skip 'em using --without tests
%bcond_without        tests

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

%bcond_without        libpcre

%bcond_without        qdbm

%bcond_without        libxcrypt

# Build firebird extensions, you can disable using --without firebird
%if 0%{?rhel} == 10
%bcond_with           firebird
%else
%bcond_without        firebird
%endif

# Build ZTS extension or only NTS using --without zts
%bcond_with           zts

# Debug build, using --with debug
%bcond_with           debug

# build with system tzdata
%bcond_without        tzdata

# /usr/sbin/a# build with libiodbc instead of unixODBC
%bcond_with           iodbc

# OpenSSL2 with argon2
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9
%bcond_without       openssl32
%else
%bcond_with          openssl32
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

%bcond_without         dtrace
%bcond_without         libgd
%bcond_with            zip

%global upver          8.4.10
#global rcver          RC1
# TODO set PHP_EXTRA_VERSION for EOL version

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: %{upver}%{?rcver:~%{rcver}}
Release: 1%{?dist}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
# Zend/asm is Boost
License: PHP-3.01 AND Zend-2.0 AND BSD-2-Clause AND MIT AND Apache-1.0 AND NCSA AND BSL-1.0
URL: http://www.php.net/

Source0: http://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source9: php.modconf
Source12: php-fpm.wants
Source13: nginx-fpm.conf
Source14: nginx-php.conf
# See https://secure.php.net/gpg-keys.php
Source20: https://www.php.net/distributions/php-keyring.gpg
Source21: https://www.php.net/distributions/php-%{upver}%{?rcver}.tar.xz.asc
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist
Source53: 20-ffi.ini

# Build fixes
Patch1: php-8.4.0-httpd.patch
Patch5: php-8.4.0-includedir.patch
Patch6: php-8.4.6-embed.patch
Patch8: php-8.4.0-libdb.patch

# Functional changes
# Use system nikic/php-parser
Patch41: php-8.3.3-parser.patch
# use system tzdata
Patch42: php-8.4.0-systzdata-v24.patch
# See http://bugs.php.net/53436
# + display PHP version backported from 8.4
Patch43: php-8.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-8.4.0-ldap_r.patch
# Ignore unsupported "threads" option on password_hash
Patch46: php-8.0.7-argon2.patch
# drop "Configure command" from phpinfo output
# and only use gcc (instead of full version)
Patch47: php-8.4.0-phpinfo.patch
# Always warn about missing curve_name
# Both Fedora and RHEL do not support arbitrary EC parameters
Patch48: php-8.3.0-openssl-ec-param.patch

# RC Patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-7.4.0-datetests.patch

# WIP

BuildRequires: gnupg2
BuildRequires: bzip2-devel
BuildRequires: pkgconfig(libcurl)  >= 7.29.0
BuildRequires: httpd-devel >= 2.0.46-1
BuildRequires: pam-devel
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
BuildRequires: %{?dtsprefix}libstdc++-devel
%if %{with openssl32}
BuildRequires: pkgconfig(openssl) >= 3.2
%else
# no pkgconfig to avoid compat-openssl10/compat-openssl11
BuildRequires: openssl-devel >= 1.0.2
%endif
BuildRequires: pkgconfig(sqlite3) >= 3.7.4
BuildRequires: pkgconfig(zlib) >= 1.2.0.4
BuildRequires: smtpdaemon
BuildRequires: pkgconfig(libedit)
%if %{with libpcre}
BuildRequires: pkgconfig(libpcre2-8) >= 10.30
%else
Provides:      bundled(pcre2) = 10.40
%endif
%if %{with libxcrypt}
BuildRequires: pkgconfig(libxcrypt)
%endif
BuildRequires: bzip2
BuildRequires: perl
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: make
BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?dtsprefix}gcc-c++
BuildRequires: libtool
BuildRequires: libtool-ltdl-devel
%if %{with dtrace}
BuildRequires: %{?dtsprefix}systemtap-sdt-devel
%if 0%{?fedora} >= 41
BuildRequires: %{?dtsprefix}systemtap-sdt-dtrace
%endif
%endif
#BuildRequires: bison
#BuildRequires: re2c >= 1.0.3
# used for tests
BuildRequires: /bin/ps
%if %{with tzdata}
BuildRequires: tzdata
%endif

%if %{with zts}
Obsoletes: php-zts < 5.3.7
Provides: php-zts = %{version}-%{release}
Provides: php-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: php-common%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# php engine for Apache httpd webserver
Provides: php(httpd)
# For backwards-compatibility, require php-cli for the time being:
Recommends: php-cli%{?_isa}      = %{version}-%{release}
# httpd have threaded MPM by default
Recommends: php-fpm%{?_isa}      = %{version}-%{release}
# as "php" is now mostly a meta-package, commonly used extensions
Recommends: php-mbstring%{?_isa} = %{version}-%{release}
Recommends: php-opcache%{?_isa}  = %{version}-%{release}
Recommends: php-pdo%{?_isa}      = %{version}-%{release}
Recommends: php-sodium%{?_isa}   = %{version}-%{release}
Recommends: php-xml%{?_isa}      = %{version}-%{release}


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
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License:  PHP-3.01 AND Zend-2.0 AND BSD-2-Clause AND MIT AND Apache-1.0 AND NCSA AND PostgreSQL
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}, php-cgi%{?_isa} = %{version}-%{release}
Provides: php-pcntl, php-pcntl%{?_isa}
Provides: php-readline, php-readline%{?_isa}

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Summary: The interactive PHP debugger
Requires: php-common%{?_isa} = %{version}-%{release}

%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Summary: PHP FastCGI Process Manager
BuildRequires: libacl-devel
BuildRequires: pkgconfig(libsystemd) >= 209
BuildRequires: pkgconfig(libselinux)
Requires: php-common%{?_isa} = %{version}-%{release}
%{?systemd_requires}
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
# php engine for Apache httpd webserver
Provides: php(httpd)
# for /etc/nginx ownership
# Temporarily not mandatory to allow nginx for nginx repo
Recommends: nginx-filesystem

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%if %{with lsws}
%package litespeed
Summary: LiteSpeed Web Server PHP support
Requires: php-common%{?_isa} = %{version}-%{release}

%description litespeed
The php-litespeed package provides the %{_bindir}/lsphp command
used by the LiteSpeed Web Server (LSAPI enabled PHP).
%endif

%package common
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP-3.01 AND BSD-2-Clause

%if %{with tzdata}
Requires:  tzdata
%endif
%if %{with libpcre}
%global pcre2_buildver %(pkg-config --silence-errors --modversion libpcre2-8 2>/dev/null || echo 10.30)
Requires:  pcre2%{?_isa} >= %{pcre2_buildver}
%endif

# ABI/API check - Arch specific
Provides: php(api) = %{apiver}-%{__isa_bits}
Provides: php(zend-abi) = %{zendver}-%{__isa_bits}
Provides: php(language) = %{version}, php(language)%{?_isa} = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2, php-bz2%{?_isa}
Provides: php-calendar, php-calendar%{?_isa}
Provides: php-core = %{version}, php-core%{?_isa} = %{version}
Provides: php-ctype, php-ctype%{?_isa}
Provides: php-curl, php-curl%{?_isa}
Provides: php-date, php-date%{?_isa}
Provides: bundled(timelib)
Provides: php-exif, php-exif%{?_isa}
Provides: php-fileinfo, php-fileinfo%{?_isa}
Provides: bundled(libmagic) = 5.43
Provides: php-filter, php-filter%{?_isa}
Provides: php-ftp, php-ftp%{?_isa}
Provides: php-gettext, php-gettext%{?_isa}
Provides: php-hash, php-hash%{?_isa}
Provides: php-mhash = %{version}, php-mhash%{?_isa} = %{version}
Provides: php-iconv, php-iconv%{?_isa}
Obsoletes: php-json < 8
Obsoletes: php-pecl-json < 8
Obsoletes: php-pecl-jsonc < 8
Provides: php-json = %{upver}, php-json%{?_isa} = %{upver}
Provides: php-libxml, php-libxml%{?_isa}
Provides: php-openssl, php-openssl%{?_isa}
Provides: php-phar, php-phar%{?_isa}
Provides: php-pcre, php-pcre%{?_isa}
Provides: php-random, php-random%{?_isa}
Provides: php-reflection, php-reflection%{?_isa}
Provides: php-session, php-session%{?_isa}
Provides: php-sockets, php-sockets%{?_isa}
Provides: php-spl, php-spl%{?_isa}
Provides: php-standard = %{version}, php-standard%{?_isa} = %{version}
Provides: php-tokenizer, php-tokenizer%{?_isa}
Provides: php-zlib, php-zlib%{?_isa}

Obsoletes: php-pecl-phar < 1.2.4
Obsoletes: php-pecl-Fileinfo < 1.0.5
Provides:  php-pecl-Fileinfo = %{fileinfover}, php-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides:  php-pecl(Fileinfo) = %{fileinfover}, php-pecl(Fileinfo)%{?_isa} = %{fileinfover}
Obsoletes: php-mhash < 5.3.0

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Summary: Files needed for building PHP extensions
Requires: php-cli%{?_isa} = %{version}-%{release}
# always needed to build extension
Requires: autoconf
Requires: automake
Requires: make
Requires: gcc
Requires: gcc-c++
Requires: libtool
# see "php-config --libs"
Requires: krb5-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: openssl-devel%{?_isa} >= 1.0.2
%if %{with libpcre}
Requires: pcre2-devel%{?_isa}
%endif
Requires: zlib-devel%{?_isa}
Obsoletes: php-pecl-json-devel  < %{version}
Obsoletes: php-pecl-jsonc-devel < %{version}
%if %{with zts}
Provides: php-zts-devel = %{version}-%{release}
Provides: php-zts-devel%{?_isa} = %{version}-%{release}
%endif
Recommends: php-nikic-php-parser5 >= 5.0.0

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP-3.01
BuildRequires: pkgconfig(capstone) >= 3.0
Requires:  php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zendopcache < 7.0.6
Provides:  php-pecl-zendopcache = %{version}
Provides:  php-pecl-zendopcache%{?_isa} = %{version}
Provides:  php-pecl(opcache) = %{version}
Provides:  php-pecl(opcache)%{?_isa} = %{version}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%package ldap
Summary: A module for PHP applications that use LDAP
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libsasl2)
BuildRequires: openldap-devel
BuildRequires: openssl-devel >= 1.0.2

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}-%{__isa_bits}
Provides: php(pdo-abi) = %{pdover}-%{__isa_bits}
Provides: php-sqlite3, php-sqlite3%{?_isa}
Provides: php-pdo_sqlite, php-pdo_sqlite%{?_isa}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-mysqli%{?_isa} = %{version}-%{release}
Provides: php-pdo_mysql, php-pdo_mysql%{?_isa}
Obsoletes: php-mysql < %{version}-%{release}

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql, php-pdo_pgsql%{?_isa}
BuildRequires: krb5-devel
BuildRequires: openssl-devel >= 1.0.2
BuildRequires: postgresql-devel

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-posix, php-posix%{?_isa}
Provides: php-shmop, php-shmop%{?_isa}
Provides: php-sysvsem, php-sysvsem%{?_isa}
Provides: php-sysvshm, php-sysvshm%{?_isa}
Provides: php-sysvmsg, php-sysvmsg%{?_isa}

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License:  PHP-3.01
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc%{?_isa}
%if %{with iodbc}
BuildRequires: pkgconfig(libiodbc)
%else
BuildRequires: pkgconfig(odbc)
%endif

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.
%if %{with iodbc}
Package build using libiodbc (instead of unixODBC).
%endif

%package soap
Summary: A module for PHP applications that use the SOAP protocol
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(libxml-2.0)

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%if %{with firebird}
%package pdo-firebird
Summary: PDO driver for Interbase/Firebird databases
# All files licensed under PHP version 3.01
License:  PHP-3.01
BuildRequires:  firebird-devel
Requires: php-pdo%{?_isa} = %{version}-%{release}
Provides: php_database
Provides: php-pdo_firebird, php-pdo_firebird%{?_isa}

%description pdo-firebird
The php-pdo-firebird package contains the PDO driver for
Interbase/Firebird databases.
%endif

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: php-dom, php-dom%{?_isa}
Provides: php-domxml, php-domxml%{?_isa}
Provides: php-simplexml, php-simplexml%{?_isa}
Provides: php-xmlreader, php-xmlreader%{?_isa}
Provides: php-xmlwriter, php-xmlwriter%{?_isa}
Provides: php-xsl, php-xsl%{?_isa}
BuildRequires: pkgconfig(libxslt)  >= 1.1
BuildRequires: pkgconfig(libexslt)
BuildRequires: pkgconfig(libxml-2.0)  >= 2.7.6

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP-3.01 AND LGPL-2.1-only AND OLDAP-2.8
%if 0%{?rhel}
BuildRequires: oniguruma5php-devel
%else
BuildRequires: oniguruma-devel
%endif
Provides: bundled(libmbfl) = 1.3.2
Requires: php-common%{?_isa} = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
# All files licensed under PHP version 3.01
%if %{with libgd}
License:  PHP-3.01
%else
# bundled libgd is licensed under MIT
License:  PHP-3.01 and MIT
%endif
Requires: php-common%{?_isa} = %{version}-%{release}
%if %{with libgd}
BuildRequires: pkgconfig(gdlib) >= 2.3.3
%else
# Required to build the bundled GD library
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libavif)
Provides: bundled(gd) = 2.0.35
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License:  PHP-3.01 AND LGPL-2.1-or-later
Requires: php-common%{?_isa} = %{version}-%{release}
Provides: bundled(libbcmath)

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
# All files licensed under PHP version 3.01
License:  PHP-3.01
BuildRequires: gmp-devel
Requires: php-common%{?_isa} = %{version}-%{release}

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
# All files licensed under PHP version 3.01
License:  PHP-3.01
BuildRequires: libdb-devel
BuildRequires: tokyocabinet-devel
BuildRequires: lmdb-devel
%if %{with qdbm}
BuildRequires: qdbm-devel
%endif
Requires: php-common%{?_isa} = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package pdo-dblib
Summary: PDO driver for Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel >= 0.91
Provides: php-pdo_dblib, php-pdo_dblib%{?_isa}
Obsoletes: php-mssql < %{version}-%{release}

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS library.

%package embedded
Summary: PHP library for embedding in applications
Requires: php-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}
Provides: php-embedded-devel%{?_isa} = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.

%package intl
Summary: Internationalization extension for PHP applications
# All files licensed under PHP version 3.01
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(icu-i18n) >= 74
BuildRequires: pkgconfig(icu-io)   >= 74
BuildRequires: pkgconfig(icu-uc)   >= 74

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
BuildRequires: pkgconfig(enchant-2)

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%if %{with zip}
%package zip
Summary: ZIP archive management extension for PHP
# All files licensed under PHP version 3.0.1
License:  PHP-3.01
Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zip          < %{zipver}
Provides:  php-pecl(zip)         = %{zipver}
Provides:  php-pecl(zip)%{?_isa} = %{zipver}
Provides:  php-pecl-zip          = %{zipver}
Provides:  php-pecl-zip%{?_isa}  = %{zipver}
BuildRequires: pkgconfig(libzip) >= 0.11

%description zip
The php-zip package provides an extension that will add
support for ZIP archive management to PHP.
%endif

%package sodium
Summary: Wrapper for the Sodium cryptographic library
# All files licensed under PHP version 3.0.1
License:  PHP-3.01
# Minimal is 1.0.8, 1.0.14 is needed for argon2 password
BuildRequires:  pkgconfig(libsodium) >= 1.0.14

Requires: php-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-libsodium2 < 3
Provides:  php-pecl(libsodium)         = %{version}
Provides:  php-pecl(libsodium)%{?_isa} = %{version}

%description sodium
The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.


%package ffi
Summary: Foreign Function Interface
# All files licensed under PHP version 3.0.1
License:  PHP-3.01
BuildRequires:  pkgconfig(libffi)

Requires: php-common%{?_isa} = %{version}-%{release}

%description ffi
FFI is one of the features that made Python and LuaJIT very useful for fast
prototyping. It allows calling C functions and using C data types from pure
scripting language and therefore develop “system code” more productively.

For PHP, FFI opens a way to write PHP extensions and bindings to C libraries
in pure PHP.


%prep
: Building %{name}-%{version}-%{release}
%if %{with lsws}
: With Litespeed SAPI
%endif
%if %{with firebird}
: With pdo_firebird extension
%endif
%if %{with zip}
: With Zip extension
%endif
%if %{with tests}
: Run Test suite
%endif
%if %{with libgd}
: Use System libgd
%else
: Use Bundled libgd
%endif
%if %{with libpcre}
: Use System libpcre
%else
: Use Bundled libpcre
%endif
%if %{with zts}
: Enable ZTS build
%endif
%if %{with debug}
: Enable Debug build
%endif
%if %{with dtrace}
: Enable Dtrace build
%endif

%{?gpgverify:%{gpgverify} --keyring='%{SOURCE20}' --signature='%{SOURCE21}' --data='%{SOURCE0}'}

%setup -q -n php-%{upver}%{?rcver}

%patch -P1 -p1 -b .mpmcheck
%patch -P5 -p1 -b .includedir
%patch -P6 -p1 -b .embed
%patch -P8 -p1 -b .libdb

%patch -P41 -p1 -b .syslib
%if %{with tzdata}
%patch -P42 -p1 -b .systzdata
%endif
%patch -P43 -p1 -b .headers
%patch -P45 -p1 -b .ldap_r
%patch -P46 -p1 -b .argon2
%patch -P47 -p1 -b .phpinfo
%patch -P48 -p1 -b .ec-param

# upstream patches

# security patches

# Fixes for tests related to tzdata
%if %{with tzdata}
%patch -P300 -p1 -b .datetests
%endif

# WIP patch

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE ZEND_LICENSE
cp Zend/asm/LICENSE BOOST_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/bcmath/libbcmath/LICENSE libbcmath_LICENSE
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Multiple builds for multiple SAPIs
# mod_php (apache2handler) and libphp (embed) can not be built from same tree
mkdir \
    build-cgi \
    build-apache \
%if %{with zts}
    build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
%if %{with tzdata}
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/bug80963.phpt
%endif
%if 0%{?fedora} < 36
# need tzdata 2022b
rm ext/date/tests/bug33415-2.phpt
%endif
# too fast builder
rm ext/date/tests/bug73837.phpt
# Should be skipped but fails sometime
rm ext/standard/tests/file/file_get_contents_error001.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt
# slow and erratic result
rm sapi/cli/tests/upload_2G.phpt
# tar issue
rm ext/zlib/tests/004-mb.phpt
# Both Fedora and RHEL do not support arbitrary EC parameters
# https://bugzilla.redhat.com/2223953
rm ext/openssl/tests/ecc_custom_params.phpt

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
ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the %{zipver} macro and rebuild.
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
cp %{SOURCE50} %{SOURCE51} %{SOURCE53} .

# Regenerated bison files
# to force, rm Zend/zend_{language,ini}_parser.[ch]
if [ ! -f Zend/zend_language_parser.c ]; then
  scripts/dev/genfiles
fi


%build
# This package fails to build with LTO due to undefined symbols.  LTO
# was disabled in OpenSuSE as well, but with no real explanation why
# beyond the undefined symbols.  It really shold be investigated further.
# Disable LTO
%define _lto_cflags %{nil}

%{?dtsenable}

# Set build date from https://reproducible-builds.org/specs/source-date-epoch/
export SOURCE_DATE_EPOCH=$(date +%s -r NEWS)
export PHP_UNAME=$(uname)
export PHP_BUILD_SYSTEM=$(cat /etc/redhat-release | sed -e 's/ Beta//')
%if 0%{?vendor:1}
export PHP_BUILD_PROVIDER="%{vendor}"
%endif
export PHP_BUILD_COMPILER="$(gcc --version | head -n1)"
export PHP_BUILD_ARCH="%{_arch}"

# Force use of system libtool:
libtoolize --force --copy
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4

# Regenerate configure scripts (patches change config.m4's)
touch configure.ac
./buildconf --force
%if %{with debug}
LDFLAGS="-fsanitize=address"
export LDFLAGS
CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign  -fsanitize=address -ggdb | sed 's/-mstackrealign//')
%else
CFLAGS=$(echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign | sed 's/-mstackrealign//')
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
# session: dep on hash, used by soap
# sockets: heavily used by FPM test suite
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --enable-rtld-now \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --without-gdbm \
    --with-openssl \
%if %{with openssl32}
    --with-openssl-argon2 \
%endif
    --with-system-ciphers \
%if %{with libpcre}
    --with-external-pcre \
%endif
%if %{with libxcrypt}
    --with-external-libcrypt \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-libxml \
%if %{with tzdata}
    --with-system-tzdata \
%endif
    --with-mhash \
    --without-password-argon2 \
%if %{with dtrace}
    --enable-dtrace \
%endif
%if %{with debug}
    --enable-debug \
%endif
    --enable-sockets \
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build cli and cgi SAPI, and most shared extensions
pushd build-cgi

build --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
      --with-capstone \
      --enable-phpdbg --enable-phpdbg-readline \
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with libgd}
      --with-external-gd \
%else
      --with-webp \
      --with-jpeg \
      --with-xpm \
      --with-freetype \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
                          --with-lmdb=%{_prefix} \
%if %{with qdbm}
                          --with-qdbm=%{_prefix} \
%endif
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-tokenizer=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
%if %{with firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
%if %{with iodbc}
      --with-iodbc=shared \
      --with-pdo-odbc=shared,iodbc \
%else
      --with-unixODBC=shared \
      --with-pdo-odbc=shared,unixODBC \
%endif
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared \
%if %{with zip}
      --with-zip=shared \
%endif
      --without-readline \
      --with-libedit \
      --enable-phar=shared \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --enable-fileinfo=shared \
      --with-ffi=shared \
      --with-sodium=shared \
      --enable-intl=shared \
      --with-enchant=shared
popd

without_shared="--disable-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --without-mysqli \
      --disable-pdo \
      --disable-opcache \
      --disable-phpdbg \
      --without-ffi \
      --disable-xmlreader --disable-xmlwriter \
      --without-sodium \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module
# use separate build to avoid libedit, libncurses...
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
%if %{with lsws}
      --enable-litespeed \
%endif
      ${without_shared}
popd

# Build php-fpm and embed
pushd build-fpm
build --enable-fpm \
      --with-fpm-systemd \
      --with-fpm-selinux \
      --with-fpm-acl \
      --enable-embed \
      ${without_shared}
popd

%if %{with zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
      --with-capstone \
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
%if %{with libgd}
      --with-external-gd \
%else
      --with-webp \
      --with-jpeg \
      --with-xpm \
      --with-freetype \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
                          --with-lmdb=%{_prefix} \
%if %{with qdbm}
                          --with-qdbm=%{_prefix} \
%endif
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
%if %{with firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
%if %{with iodbc}
      --with-iodbc=shared \
      --with-pdo-odbc=shared,iodbc \
%else
      --with-unixODBC=shared \
      --with-pdo-odbc=shared,unixODBC \
%endif
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
      --with-pdo-dblib=shared,%{_prefix} \
      --with-sqlite3=shared \
%if %{with zip}
      --with-zip=shared \
%endif
      --without-readline \
      --with-libedit \
      --enable-phar=shared \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --enable-fileinfo=shared \
      --with-ffi=shared \
      --with-sodium=shared \
      --enable-intl=shared \
      --with-enchant=shared
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif


%check
: Ensure proper NTS/ZTS build
$RPM_BUILD_ROOT%{_bindir}/php     -n -v | grep NTS
%if %{with zts}
$RPM_BUILD_ROOT%{_bindir}/zts-php -n -v | grep ZTS
%endif

%if %{with tests}
cd build-fpm

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
export SKIP_IO_CAPTURE_TESTS=1
unset TZ LANG LC_ALL
if ! make test TESTS=%{?_smp_mflags}; then
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

%if %{with zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-fpm install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Use php-config from embed SAPI to reduce used libs
install -m 755 build-fpm/scripts/php-config $RPM_BUILD_ROOT%{_bindir}/php-config

# Install the default configuration file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php/preload

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp.so

# Apache config fragment
# Dual config file with httpd >= 2.4 (fedora >= 18)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/20-php.conf
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/opcache
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/peclxml
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/pecl
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/tests/pecl

%if %{with lsws}
install -m 755 build-apache/sapi/litespeed/lsphp $RPM_BUILD_ROOT%{_bindir}/lsphp
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

install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# install systemd unit files and scripts for handling server startup
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -Dm 644 %{SOURCE6}  $RPM_BUILD_ROOT%{_unitdir}/php-fpm.service
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/httpd.service.d/php-fpm.conf
install -Dm 644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/nginx.service.d/php-fpm.conf

# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

TESTCMD="$RPM_BUILD_ROOT%{_bindir}/php --no-php-ini"
# Ensure all provided extensions are really there
for mod in core date filter hash json libxml openssl pcntl pcre readline reflection session spl standard zlib
do
     $TESTCMD --modules | grep -i "$mod\$"
done

TESTCMD="$TESTCMD --define extension_dir=$RPM_BUILD_ROOT%{_libdir}/php/modules"

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp \
    mysqlnd mysqli \
    mbstring gd dom xsl soap bcmath dba \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    tokenizer opcache \
    pdo \
%if %{with zip}
    zip \
%endif
    sqlite3 \
    enchant phar fileinfo intl \
    ffi \
    tidy curl \
    sodium \
    posix shmop sysvshm sysvsem sysvmsg xml \
    pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite pdo_dblib \
%if %{with firebird}
    pdo_firebird \
%endif
    xmlreader xmlwriter
do
    case $mod in
      opcache)
        # Zend extensions
        TESTCMD="$TESTCMD --define zend_extension=$mod"
        ini=10-${mod}.ini;;
      pdo_*|mysqli|xmlreader)
        # Extensions with dependencies on 20-*
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        TESTCMD="$TESTCMD --define extension=$mod"
        ini=20-${mod}.ini;;
    esac

    $TESTCMD --modules | grep -i "$mod\$"

    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
      %if %{with zts}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
      %endif
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%if %{with zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
%if %{with zts}
%{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype \
    files.tokenizer > files.common

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini
%endif

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}-%{__isa_bits}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}-%{__isa_bits}/" \
    -e "s/@PHP_PDOVER@/%{pdover}-%{__isa_bits}/" \
    -e "s/@PHP_VERSION@/%{upver}/" \
%if %{without zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php
install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_bindir}/zts-phar* \
       $RPM_BUILD_ROOT%{_mandir}/man1/zts-phar* \
       $RPM_BUILD_ROOT%{_libdir}/libphp.a \
       $RPM_BUILD_ROOT%{_libdir}/libphp.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%pre common
%if %{?fedora}%{!?fedora:99} < 29
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif


%post fpm
%systemd_post php-fpm.service

%preun fpm
%systemd_preun php-fpm.service

# Raised by new pool installation or new extension installation
%transfiletriggerin fpm -- %{_sysconfdir}/php-fpm.d %{_sysconfdir}/php.d
systemctl try-restart php-fpm.service >/dev/null 2>&1 || :


%files
%{_httpd_moddir}/libphp.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_httpd_modconfdir}/20-php.conf

%files common -f files.common
%doc EXTENSIONS NEWS UPGRADING* README.REDIST.BINS *md docs
%license LICENSE TSRM_LICENSE ZEND_LICENSE BOOST_LICENSE
%license libmagic_LICENSE
%license timelib_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php
%dir %{_localstatedir}/lib/php/peclxml
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%dir %{_datadir}/php

%files cli
%{_bindir}/php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%if %{with zts}
%{_bindir}/zts-php
%{_mandir}/man1/zts-php.1*
%{_mandir}/man1/zts-phpize.1*
%endif

%files dbg
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif
%doc sapi/phpdbg/CREDITS

%files fpm
%doc php-fpm.conf.default www.conf.default
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%{_unitdir}/php-fpm.service
%config(noreplace) %{_sysconfdir}/systemd/system/httpd.service.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/systemd/system/nginx.service.d/php-fpm.conf
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir %ghost /run/php-fpm
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%if %{with lsws}
%files litespeed
%{_bindir}/lsphp
%endif

%files devel
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
%{_libdir}/php-zts/build
%{_mandir}/man1/zts-php-config.1*
%endif
%{_mandir}/man1/php-config.1*
%{macrosdir}/macros.php

%files embedded
%{_libdir}/libphp.so
%{_libdir}/libphp-%{embed_version}.so

%files pgsql -f files.pgsql
%files odbc -f files.odbc
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%files gd -f files.gd
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_LICENSE
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files tidy -f files.tidy
%files pdo-dblib -f files.pdo_dblib
%files intl -f files.intl
%files process -f files.process
%if %{with firebird}
%files pdo-firebird -f files.pdo_firebird
%endif
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
%if %{with zip}
%files zip -f files.zip
%endif
%files sodium -f files.sodium
%files ffi -f files.ffi
%dir %{_datadir}/php/preload


%changelog
* Wed Jul  2 2025 Remi Collet <remi@remirepo.net> - 8.4.10-1
- Update to 8.4.10 - http://www.php.net/releases/8_4_10.php

* Wed Jun 18 2025 Remi Collet <remi@remirepo.net> - 8.4.9~RC1-1
- Update to 8.4.9RC1

* Wed Jun  4 2025 Remi Collet <remi@remirepo.net> - 8.4.8-1
- Update to 8.4.8 - http://www.php.net/releases/8_4_8.php

* Wed May 21 2025 Remi Collet <remi@remirepo.net> - 8.4.8~RC1-1
- Update to 8.4.8RC1
- use same build tree for fpm and embed

* Tue May  6 2025 Remi Collet <remi@remirepo.net> - 8.4.7-1
- Update to 8.4.7 - http://www.php.net/releases/8_4_7.php

* Thu May  1 2025 Remi Collet <remi@remirepo.net> - 8.4.7~RC2-1
- Update to 8.4.7RC2

* Tue Apr 22 2025 Remi Collet <remi@remirepo.net> - 8.4.7~RC1-1
- Update to 8.4.7RC1

* Wed Apr  9 2025 Remi Collet <remi@remirepo.net> - 8.4.6-1
- Update to 8.4.6 - http://www.php.net/releases/8_4_6.php

* Wed Mar 26 2025 Remi Collet <remi@remirepo.net> - 8.4.6~RC1-1
- Update to 8.4.6RC1

* Wed Mar 12 2025 Remi Collet <remi@remirepo.net> - 8.4.5-1
- Update to 8.4.5 - http://www.php.net/releases/8_4_5.php

* Tue Feb 25 2025 Remi Collet <remi@remirepo.net> - 8.4.5~RC1-1
- Update to 8.4.5RC1

* Wed Feb 12 2025 Remi Collet <remi@remirepo.net> - 8.4.4-1
- Update to 8.4.4 - http://www.php.net/releases/8_4_4.php

* Fri Jan 31 2025 Remi Collet <remi@remirepo.net> - 8.4.4~RC2-1
- Update to 8.4.4RC2

* Wed Jan 29 2025 Remi Collet <remi@remirepo.net> - 8.4.4~RC1-1
- Update to 8.4.4RC1

* Wed Jan 15 2025 Remi Collet <remi@remirepo.net> - 8.4.3-1
- Update to 8.4.3 - http://www.php.net/releases/8_4_3.php

* Wed Jan  1 2025 Remi Collet <remi@remirepo.net> - 8.4.3~RC1-1
- Update to 8.4.3RC1

* Wed Dec 18 2024 Remi Collet <remi@remirepo.net> - 8.4.2-1
- Update to 8.4.2 - http://www.php.net/releases/8_4_2.php

* Tue Dec  3 2024 Remi Collet <remi@remirepo.net> - 8.4.2~RC1-1
- Update to 8.4.2RC1
- EL-9.5: enable argon2 password hash, using OpenSSL 3.2

* Wed Nov 20 2024 Remi Collet <remi@remirepo.net> - 8.4.1-1
- Update to 8.4.1 - http://www.php.net/releases/8_4_1.php

* Wed Nov 20 2024 Remi Collet <remi@remirepo.net> - 8.4.0-1
- Update to 8.4.0 GA

* Tue Nov  5 2024 Remi Collet <remi@remirepo.net> - 8.4.0~rc4-1
- Update to 8.4.0RC4

* Wed Oct 23 2024 Remi Collet <remi@remirepo.net> - 8.4.0~rc3-1
- Update to 8.4.0RC3

* Tue Oct  8 2024 Remi Collet <remi@remirepo.net> - 8.4.0~rc2-1
- Update to 8.4.0RC2

* Tue Sep 24 2024 Remi Collet <remi@remirepo.net> - 8.4.0~rc1-1
- Update to 8.4.0RC1
- bump ABI/API numbers

* Mon Sep 23 2024 Remi Collet <remi@remirepo.net> - 8.4.0~beta5-1
- update to 8.4.0beta5
- drop oci8, pdo_oci8, pspell and imap extensions
- disable ZTS build

* Tue Sep 10 2024 Remi Collet <remi@remirepo.net> - 8.3.12~RC1-1
- update to 8.3.12RC1
- use ICU 74.2

* Wed Aug 28 2024 Remi Collet <remi@remirepo.net> - 8.3.11-1
- Update to 8.3.11 - http://www.php.net/releases/8_3_11.php

* Thu Aug 22 2024 Remi Collet <remi@remirepo.net> - 8.3.11~RC2-1
- update to 8.3.11RC2

* Wed Aug 14 2024 Remi Collet <remi@remirepo.net> - 8.3.11~RC1-2
- allow to build using libiodbc instead of unixODBC (--with iodbc)

* Wed Aug 14 2024 Remi Collet <remi@remirepo.net> - 8.3.11~RC1-1
- update to 8.3.11RC1

* Tue Jul 30 2024 Remi Collet <remi@remirepo.net> - 8.3.10-1
- Update to 8.3.10 - http://www.php.net/releases/8_3_10.php
- use oracle client library version 23.5 on x86_64

* Tue Jul 16 2024 Remi Collet <remi@remirepo.net> - 8.3.10~RC1-1
- update to 8.3.10RC1
- use oracle client library version 23.4 on x86_64, 19.23 on aarch64

* Wed Jul  3 2024 Remi Collet <remi@remirepo.net> - 8.3.9-1
- Update to 8.3.9 - http://www.php.net/releases/8_3_9.php

* Fri Jun  7 2024 Remi Collet <remi@remirepo.net> - 8.3.8-2
- Fix GH-14480 Method visibility issue introduced in version 8.3.8

* Tue Jun  4 2024 Remi Collet <remi@remirepo.net> - 8.3.8-1
- Update to 8.3.8 - http://www.php.net/releases/8_3_8.php

* Wed May 22 2024 Remi Collet <remi@remirepo.net> - 8.3.8~RC1-1
- update to 8.3.8RC1

* Mon May 13 2024 Remi Collet <remi@remirepo.net> - 8.3.7-1
- Update to 8.3.7 - http://www.php.net/releases/8_3_7.php

* Wed Apr 24 2024 Remi Collet <remi@remirepo.net> - 8.3.7~RC1-1
- update to 8.3.7RC1
- use oracle client library version 19.22 on aarch64

* Wed Apr 10 2024 Remi Collet <remi@remirepo.net> - 8.3.6-1
- Update to 8.3.6 - http://www.php.net/releases/8_3_6.php

* Wed Apr 10 2024 Remi Collet <remi@remirepo.net> - 8.3.5-1
- Update to 8.3.5 - http://www.php.net/releases/8_3_5.php

* Wed Mar 27 2024 Remi Collet <remi@remirepo.net> - 8.3.5~RC1-1
- update to 8.3.5RC1

* Wed Mar 13 2024 Remi Collet <remi@remirepo.net> - 8.3.4-1
- Update to 8.3.4 - http://www.php.net/releases/8_3_4.php

* Wed Feb 28 2024 Remi Collet <remi@remirepo.net> - 8.3.4~RC1-1
- update to 8.3.4RC1

* Wed Feb 14 2024 Remi Collet <remi@remirepo.net> - 8.3.3-1
- Update to 8.3.3 - http://www.php.net/releases/8_3_3.php
- use oracle client library version 21.13 on x86_64

* Wed Jan 31 2024 Remi Collet <remi@remirepo.net> - 8.3.3~RC1-1
- update to 8.3.3RC1

* Tue Jan 16 2024 Remi Collet <remi@remirepo.net> - 8.3.2-1
- Update to 8.3.2 - http://www.php.net/releases/8_3_2.php

* Wed Jan  3 2024 Remi Collet <remi@remirepo.net> - 8.3.2~RC1-1
- update to 8.3.2RC1

* Wed Dec 20 2023 Remi Collet <remi@remirepo.net> - 8.3.1-1
- Update to 8.3.1 - http://www.php.net/releases/8_3_1.php

* Thu Dec  7 2023 Remi Collet <remi@remirepo.net> - 8.3.1~RC3-1
- update to 8.3.1RC3

* Wed Dec  6 2023 Remi Collet <remi@remirepo.net> - 8.3.1~RC1-1
- update to 8.3.1RC1

* Wed Nov 22 2023 Remi Collet <remi@remirepo.net> - 8.3.0-1
- Update to 8.3.0 GA - http://www.php.net/releases/8_3_0.php

* Wed Nov  8 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc6-1
- update to 8.3.0RC6
- use oracle client library version 21.12 on x86_64
- use ICU 73.2
- build sockets extension statically

* Tue Oct 24 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc5-1
- update to 8.3.0RC5

* Wed Oct 11 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc4-1
- update to 8.3.0RC4

* Tue Sep 26 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc3-1
- update to 8.3.0RC3

* Mon Sep 25 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc2-3
- add internal UTC if tzdata is missing

* Thu Sep 21 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc2-2
- use oracle client library version 19.19 on aarch64
- use official Oracle Instant Client RPM

* Tue Sep 12 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc2-1
- update to 8.3.0RC2
- use oracle client library version 21.11

* Tue Aug 29 2023 Remi Collet <remi@remirepo.net> - 8.3.0~rc1-1
- update to 8.3.0RC1
- bump to final API/ABI
- switch to nikic/php-parser version 5
- openssl: always warn about missing curve_name

* Tue Aug 29 2023 Remi Collet <remi@remirepo.net> - 8.2.10-1
- Update to 8.2.10 - http://www.php.net/releases/8_2_10.php

* Thu Aug 17 2023 Remi Collet <remi@remirepo.net> - 8.2.10~RC1-1
- update to 8.2.10RC1

* Thu Aug  3 2023 Remi Collet <remi@remirepo.net> - 8.2.9-2
- Update to 8.2.9 - http://www.php.net/releases/8_2_9.php
- rebuild for new sources

* Tue Aug  1 2023 Remi Collet <remi@remirepo.net> - 8.2.9-1
- Update to 8.2.9 - http://www.php.net/releases/8_2_9.php

* Tue Jul 18 2023 Remi Collet <remi@remirepo.net> - 8.2.9~RC1-1
- update to 8.2.9RC1
- move httpd/nginx wants directive to config files in /etc

* Wed Jul  5 2023 Remi Collet <remi@remirepo.net> - 8.2.8-1
- Update to 8.2.8 - http://www.php.net/releases/8_2_8.php

* Tue Jun 20 2023 Remi Collet <remi@remirepo.net> - 8.2.8~RC1-1
- update to 8.2.8RC1

* Wed Jun  7 2023 Remi Collet <remi@remirepo.net> - 8.2.7-2
- Update to 8.2.7 - http://www.php.net/releases/8_2_7.php
- rebuild for new sources

* Tue Jun  6 2023 Remi Collet <remi@remirepo.net> - 8.2.7-1
- Update to 8.2.7 - http://www.php.net/releases/8_2_7.php

* Wed May 24 2023 Remi Collet <remi@remirepo.net> - 8.2.7~RC1-1
- update to 8.2.7RC1

* Wed May 10 2023 Remi Collet <remi@remirepo.net> - 8.2.6-1
- Update to 8.2.6 - http://www.php.net/releases/8_2_6.php

* Tue Apr 25 2023 Remi Collet <remi@remirepo.net> - 8.2.6~RC1-2
- define %%__phpize and %%__phpconfig

* Tue Apr 25 2023 Remi Collet <remi@remirepo.net> - 8.2.6~RC1-1
- update to 8.2.6RC1
- use oracle client library version 21.10
- use ICU 72.1
- oci8 version is now 3.3.0

* Wed Apr 12 2023 Remi Collet <remi@remirepo.net> - 8.2.5-1
- Update to 8.2.5 - http://www.php.net/releases/8_2_5.php

* Wed Mar 29 2023 Remi Collet <remi@remirepo.net> - 8.2.5~RC1-1
- update to 8.2.5RC1

* Wed Mar 15 2023 Remi Collet <remi@remirepo.net> - 8.2.4-1
- Update to 8.2.4 - http://www.php.net/releases/8_2_4.php

* Wed Mar  1 2023 Remi Collet <remi@remirepo.net> - 8.2.4~RC1-1
- update to 8.2.4RC1

* Tue Feb 21 2023 Remi Collet <remi@remirepo.net> - 8.2.3-2
- F38: enable imap extension

* Tue Feb 14 2023 Remi Collet <remi@remirepo.net> - 8.2.3-1
- Update to 8.2.3 - http://www.php.net/releases/8_2_3.php

* Fri Feb 10 2023 Remi Collet <remi@remirepo.net> - 8.2.2-2
- F38: disable imap extension

* Wed Feb  1 2023 Remi Collet <remi@remirepo.net> - 8.2.2-1
- Update to 8.2.2 - http://www.php.net/releases/8_2_2.php
- add dependency on pcre2 minimal version

* Wed Jan 18 2023 Remi Collet <remi@remirepo.net> - 8.2.2~RC1-1
- update to 8.2.2RC1

* Wed Jan  4 2023 Remi Collet <remi@remirepo.net> - 8.2.1-1
- Update to 8.2.1 - http://www.php.net/releases/8_2_1.php

* Tue Dec 20 2022 Remi Collet <remi@remirepo.net> - 8.2.1~RC1-3
- add upstream patch for failing test

* Mon Dec 19 2022 Remi Collet <remi@remirepo.net> - 8.2.1~RC1-2
- php-fpm.conf: move include directive after [global] section
  https://github.com/remicollet/remirepo/issues/225

* Wed Dec 14 2022 Remi Collet <remi@remirepo.net> - 8.2.1~RC1-1
- update to 8.2.1RC1
- use oracle client library version 21.8

* Tue Dec  6 2022 Remi Collet <remi@remirepo.net> - 8.2.0-1
- update to 8.2.0 GA

* Fri Nov 25 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC7-9
- test build for GH-9997 with new upstream patch

* Wed Nov 23 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC7-8
- update to 8.2.0RC7

* Tue Nov  8 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC6-7
- update to 8.2.0RC6

* Wed Oct 26 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC5-6
- update to 8.2.0RC5

* Tue Oct 11 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC4-5
- update to 8.2.0RC4

* Wed Sep 28 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC3-4
- update to 8.2.0RC3

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC2-3
- update to 8.2.0RC2 (new tag)
- add patch from https://github.com/php/php-src/pull/9537

* Wed Sep 14 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC2-2
- update to 8.2.0RC2

* Fri Sep  2 2022 Remi Collet <remi@remirepo.net> - 8.2.0~RC1-1
- update to 8.2.0RC1
- bump API/ABI
- new random extension
- add dependency on libselinux

* Thu Sep  1 2022 Remi Collet <remi@remirepo.net> - 8.1.10-1
- Update to 8.1.10 - http://www.php.net/releases/8_1_10.php

* Wed Aug 17 2022 Remi Collet <remi@remirepo.net> - 8.1.10~RC1-1
- update to 8.1.10RC1
- use oracle client library version 21.7
- use ICU 71.1

* Tue Aug  2 2022 Remi Collet <remi@remirepo.net> - 8.1.9-1
- Update to 8.1.9 - http://www.php.net/releases/8_1_9.php

* Wed Jul 20 2022 Remi Collet <remi@remirepo.net> - 8.1.9~RC1-1
- update to 8.1.9RC1

* Wed Jul  6 2022 Remi Collet <remi@remirepo.net> - 8.1.8-1
- Update to 8.1.8 - http://www.php.net/releases/8_1_8.php

* Tue Jun 21 2022 Remi Collet <remi@remirepo.net> - 8.1.8~RC1-1
- update to 8.1.8RC1

* Wed Jun  8 2022 Remi Collet <remi@remirepo.net> - 8.1.7-1
- Update to 8.1.7 - http://www.php.net/releases/8_1_7.php

* Fri Jun  3 2022 Remi Collet <remi@remirepo.net> - 8.1.7~RC1-2
- add upstream patch to initialize pcre before mbstring

* Wed May 25 2022 Remi Collet <remi@remirepo.net> - 8.1.7~RC1-1
- update to 8.1.7RC1

* Wed May 11 2022 Remi Collet <remi@remirepo.net> - 8.1.6-1
- Update to 8.1.6 - http://www.php.net/releases/8_1_6.php
- use oracle client library version 21.6

* Wed Apr 27 2022 Remi Collet <remi@remirepo.net> - 8.1.6~RC1-1
- update to 8.1.6RC1

* Wed Apr 13 2022 Remi Collet <remi@remirepo.net> - 8.1.5-1
- Update to 8.1.5 - http://www.php.net/releases/8_1_5.php

* Fri Apr  1 2022 Remi Collet <remi@remirepo.net> - 8.1.5~RC1-1
- update to 8.1.5RC1

* Wed Mar 16 2022 Remi Collet <remi@remirepo.net> - 8.1.4-1
- Update to 8.1.4 - http://www.php.net/releases/8_1_4.php

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 8.1.4~RC1-1
- update to 8.1.4RC1

* Tue Feb 22 2022 Remi Collet <remi@remirepo.net> - 8.1.3-2
- retrieve tzdata version
- use oracle client library version 21.5

* Wed Feb 16 2022 Remi Collet <remi@remirepo.net> - 8.1.3-1
- Update to 8.1.3 - http://www.php.net/releases/8_1_3.php

* Tue Feb  8 2022 Remi Collet <remi@remirepo.net> - 8.1.3~RC1-2
- fix GH-8059 arginfo not regenerated for extension

* Thu Feb  3 2022 Remi Collet <remi@remirepo.net> - 8.1.3~RC1-1
- update to 8.1.3RC1

* Wed Jan 19 2022 Remi Collet <remi@remirepo.net> - 8.1.2-1
- Update to 8.1.2 - http://www.php.net/releases/8_1_2.php
- Fix GH-7899 Regression in unpack for negative int value
- Fix GH-7883 Segfault when INI file is not readable

* Wed Jan  5 2022 Remi Collet <remi@remirepo.net> - 8.1.2~RC1-1
- update to 8.1.2RC1

* Wed Dec 15 2021 Remi Collet <remi@remirepo.net> - 8.1.1-1
- Update to 8.1.1 - http://www.php.net/releases/8_1_1.php

* Thu Dec  2 2021 Remi Collet <remi@remirepo.net> - 8.1.1~RC1-1
- update to 8.1.1RC1
- use oracle client library version 21.4
- ensure libgd 2.3 is used

* Wed Nov 24 2021 Remi Collet <remi@remirepo.net> - 8.1.0-1
- update to 8.1.0 GA

* Wed Nov 10 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC6-1
- update to 8.1.0RC6

* Tue Oct 26 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC5-1
- update to 8.1.0RC5
- build using system libxcrypt (Fedora only)

* Tue Oct 26 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC4-2
- dba: enable qdbm backend
- dba: drop gdbm backend

* Wed Oct 13 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC4-1
- update to 8.1.0RC4

* Fri Oct  1 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC3-3
- rebuild using ICU 69

* Wed Sep 29 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC3-1
- update to 8.1.0RC3

* Sat Sep 18 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC2-1
- update to 8.1.0RC2
- use oracle client library version 21.3

* Thu Sep  2 2021 Remi Collet <remi@remirepo.net> - 8.1.0~RC1-1
- update to 8.1.0RC1
- bump API version

* Tue Aug 24 2021 Remi Collet <remi@remirepo.net> - 8.0.10-1
- Update to 8.0.10 - http://www.php.net/releases/8_0_10.php

* Wed Aug 11 2021 Remi Collet <remi@remirepo.net> - 8.0.10~RC1-2
- phar: switch to sha256 signature by default, backported from 8.1
- phar: implement openssl_256 and openssl_512 for signatures, backported from 8.1
- snmp: add sha256 / sha512 security protocol, backported from 8.1

* Tue Aug 10 2021 Remi Collet <remi@remirepo.net> - 8.0.10~RC1-1
- update to 8.0.10RC1
- adapt systzdata patch for timelib 2020.03 (v20)

* Thu Jul 29 2021 Remi Collet <remi@remirepo.net> - 8.0.9-1
- Update to 8.0.9 - http://www.php.net/releases/8_0_9.php

* Tue Jul 13 2021 Remi Collet <remi@remirepo.net> - 8.0.9~RC1-1
- update to 8.0.9RC1

* Tue Jun 29 2021 Remi Collet <remi@remirepo.net> - 8.0.8-1
- Update to 8.0.8 - http://www.php.net/releases/8_0_8.php

* Tue Jun 15 2021 Remi Collet <remi@remirepo.net> - 8.0.8~RC1-1
- update to 8.0.8RC1
- ignore unsupported "threads" option on password_hash

* Wed Jun  2 2021 Remi Collet <remi@remirepo.net> - 8.0.7-1
- Update to 8.0.7 - http://www.php.net/releases/8_0_7.php

* Thu May 20 2021 Remi Collet <remi@remirepo.net> - 8.0.7~RC1-1
- update to 8.0.7RC1

* Sat May  8 2021 Remi Collet <remi@remirepo.net> - 8.0.6-2
- get rid of inet_ntoa, inet_aton, inet_addr and gethostbyaddr calls

* Wed May  5 2021 Remi Collet <remi@remirepo.net> - 8.0.6-1
- Update to 8.0.6 - http://www.php.net/releases/8_0_6.php

* Tue Apr 27 2021 Remi Collet <remi@remirepo.net> - 8.0.5-1
- Update to 8.0.5 - http://www.php.net/releases/8_0_5.php

* Tue Apr 13 2021 Remi Collet <remi@remirepo.net> - 8.0.5~RC1-1
- update to 8.0.5RC1

* Tue Mar 16 2021 Remi Collet <remi@remirepo.net> - 8.0.4~RC1-1
- update to 8.0.4RC1
- use oracle client library version 21.1

* Wed Mar  3 2021 Remi Collet <remi@remirepo.net> - 8.0.3-1
- Update to 8.0.3 - http://www.php.net/releases/8_0_3.php

* Thu Feb 18 2021 Remi Collet <remi@remirepo.net> - 8.0.3~RC1-1
- update to 8.0.3RC1

* Tue Feb  2 2021 Remi Collet <remi@remirepo.net> - 8.0.2-1
- Update to 8.0.2 - http://www.php.net/releases/8_0_2.php

* Thu Jan 28 2021 Remi Collet <remi@remirepo.net> - 8.0.2~RC1-2
- add upstream patch for https://bugs.php.net/80682
  fix opcache doesn't honour pcre.jit option

* Tue Jan 19 2021 Remi Collet <remi@remirepo.net> - 8.0.2~RC1-1
- update to 8.0.2RC1
- oci8 version is now 3.0.1

* Tue Jan  5 2021 Remi Collet <remi@remirepo.net> - 8.0.1-1
- Update to 8.0.1 - http://www.php.net/releases/8_0_1.php

* Tue Dec 15 2020 Remi Collet <remi@remirepo.net> - 8.0.1~RC1-1
- update to 8.0.1RC1

* Wed Nov 25 2020 Remi Collet <remi@remirepo.net> - 8.0.0-1
- update to 8.0.0 GA

* Wed Nov 18 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc5-9
- update to 8.0.0RC5
- use oracle client library version 19.9

* Tue Nov 10 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc4-8
- update to 8.0.0RC4

* Tue Oct 27 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc3-7
- update to 8.0.0RC3

* Wed Oct 14 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc2-6
- update to 8.0.0RC2

* Wed Sep 30 2020 Remi Collet <remi@remirepo.net> - 8.0.0~rc1-34
- update to 8.0.0rc1
- bump ABI/API versions

* Thu Sep 17 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-4
- drop mod_php for ZTS (have never be suported)
- use %%bcond_without for dtrace, libgd, firebird, lsws, libpcre and zts
  so can be disabled during rebuild
- use %%bcond_with for libgd, libpcre, oci8, zip and debug
  so can be enabled during rebuild

* Thu Sep 17 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-3
- properly use --enable-zts for ZTS builds

* Wed Sep 16 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta4-2
- update to 8.0.0beta4

* Fri Sep 11 2020 Remi Collet <remi@remirepo.net> - 8.0.0~beta3-1
- update to 8.0.0beta3
- bump ABI/API versions
- drop xmlrpc extension
- json is now build statically
- use system nikic/php-parser if available to generate
  C headers from PHP stub
- switch from "runselftest" option to %bcond_without tests
- enchant: use libenchant-2 instead of libenchant
- rename 15-php.conf to 20-php.conf to ensure load order
- oci8 version is now 3.0.0

* Tue Sep  1 2020 Remi Collet <remi@remirepo.net> - 7.4.10-1
- Update to 7.4.10 - http://www.php.net/releases/7_4_10.php

* Tue Aug 18 2020 Remi Collet <remi@remirepo.net> - 7.4.10~RC1-1
- update to 7.4.10RC1
- use oracle client library version 19.8 (x86_64)

* Tue Aug  4 2020 Remi Collet <remi@remirepo.net> - 7.4.9-1
- Update to 7.4.9 - http://www.php.net/releases/7_4_9.php

* Tue Jul 21 2020 Remi Collet <remi@remirepo.net> - 7.4.9~RC1-1
- update to 7.4.9RC1
- build using ICU 65

* Thu Jul  9 2020 Remi Collet <remi@remirepo.net> - 7.4.8-2
- Update to 7.4.8 - http://www.php.net/releases/7_4_8.php
  rebuild from new sources

* Tue Jul  7 2020 Remi Collet <remi@remirepo.net> - 7.4.8-1
- Update to 7.4.8 - http://www.php.net/releases/7_4_8.php

* Mon Jul  6 2020 Remi Collet <remi@remirepo.net> - 7.4.8~RC1-2
- display build system and provider in phpinfo (from 8.0)

* Tue Jun 23 2020 Remi Collet <remi@remirepo.net> - 7.4.8~RC1-1
- update to 7.4.8RC1
- drop patch to fix PHP_UNAME

* Tue Jun  9 2020 Remi Collet <remi@remirepo.net> - 7.4.7-1
- Update to 7.4.7 - http://www.php.net/releases/7_4_7.php
- rebuild using oniguruma5php
- build phpdbg only once

* Tue May 26 2020 Remi Collet <remi@remirepo.net> - 7.4.7~RC1-1
- update to 7.4.7RC1

* Wed May 20 2020 Remi Collet <remi@remirepo.net> - 7.4.6-2
- use php-config from embed SAPI to reduce used libs

* Tue May 12 2020 Remi Collet <remi@remirepo.net> - 7.4.6-1
- Update to 7.4.6 - http://www.php.net/releases/7_4_6.php

* Wed Apr 29 2020 Remi Collet <remi@remirepo.net> - 7.4.6~RC1-1
- update to 7.4.6RC1

* Tue Apr 14 2020 Remi Collet <remi@remirepo.net> - 7.4.5-1
- Update to 7.4.5 - http://www.php.net/releases/7_4_5.php

* Tue Mar 31 2020 Remi Collet <remi@remirepo.net> - 7.4.5~RC1-1
- update to 7.4.5RC1

* Tue Mar 17 2020 Remi Collet <remi@remirepo.net> - 7.4.4-1
- Update to 7.4.4 - http://www.php.net/releases/7_4_4.php
- use oracle client library version 19.6 (18.5 on EL-6)

* Tue Mar  3 2020 Remi Collet <remi@remirepo.net> - 7.4.4~RC1-1
- update to 7.4.4RC1

* Tue Feb 18 2020 Remi Collet <remi@remirepo.net> - 7.4.3-1
- Update to 7.4.3 - http://www.php.net/releases/7_4_3.php

* Tue Feb  4 2020 Remi Collet <remi@remirepo.net> - 7.4.3~RC1-1
- update to 7.4.3RC1

* Tue Jan 28 2020 Remi Collet <remi@remirepo.net> - 7.4.2-2
- make sodium mandatory on EL-7, to avoid user confusion
  https://github.com/remicollet/remirepo/issues/137

* Tue Jan 21 2020 Remi Collet <remi@remirepo.net> - 7.4.2-1
- Update to 7.4.2 - http://www.php.net/releases/7_4_2.php

* Tue Jan  7 2020 Remi Collet <remi@remirepo.net> - 7.4.2~RC1-1
- update to 7.4.2RC1

* Wed Dec 18 2019 Remi Collet <remi@remirepo.net> - 7.4.1-1
- Update to 7.4.1 - http://www.php.net/releases/7_4_1.php

* Wed Dec 11 2019 Remi Collet <remi@remirepo.net> - 7.4.1~RC1-1
- update to 7.4.1RC1
- use oracle client library version 19.5

* Wed Nov 27 2019 Remi Collet <remi@remirepo.net> - 7.4.0-1
- update to 7.4.0 GA

* Mon Nov 11 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC6-15
- update to 7.4.0RC6

* Tue Oct 29 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC5-14
- update to 7.4.0RC5
- set opcache.enable_cli in provided default configuration

* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-13
- add /usr/share/php/preload as default ffi.preload configuration

* Thu Oct 24 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-12
- allow wildcards in ffi.preload

* Wed Oct 23 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-11
- fix preload, add more upstream patches for #78713 #78716

* Mon Oct 21 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-10
- fix preload, add upstream patch for #78512
- change dependency on nginx-filesystem to weak

* Tue Oct 15 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC4-9
- update to 7.4.0RC4

* Thu Oct 10 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-8
- fix librt issue on F31 using upstream patch

* Mon Oct  7 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-7
- ensure all shared extensions can be loaded

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-6
- fix broken intl extension on EL-7

* Tue Oct  1 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC3-5
- update to 7.4.0RC3

* Fri Sep 20 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-4
- fix broken gmp extension https://bugs.php.net/78574

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-3
- update to 7.4.0RC2 (new tag)

* Tue Sep 17 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC2-2
- update to 7.4.0RC2
- add tarball signature check
- reduce to 4 concurrent test workers

* Thu Sep  5 2019 Remi Collet <remi@remirepo.net> - 7.4.0~RC1-1
- update to 7.4.0RC1

* Wed Aug 28 2019 Remi Collet <remi@remirepo.net> - 7.3.9-1
- Update to 7.3.9 - http://www.php.net/releases/7_3_9.php

* Mon Aug 19 2019 Remi Collet <remi@remirepo.net> - 7.3.9~RC1-1
- update to 7.3.9RC1

* Tue Jul 30 2019 Remi Collet <remi@remirepo.net> - 7.3.8-1
- Update to 7.3.8 - http://www.php.net/releases/7_3_8.php

* Tue Jul 16 2019 Remi Collet <remi@remirepo.net> - 7.3.8~RC1-1
- update to 7.3.8RC1
- add upstream patch for #78297
- main package now recommends commonly used extensions
  (json, mbstring, opcache, pdo, xml)

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 7.3.7-3
- rebuild 7.3.7 (new tag)

* Wed Jul  3 2019 Remi Collet <remi@remirepo.net> - 7.3.7-2
- add upstream patch for https://bugs.php.net/78230
  segfault with opcache enabled

* Tue Jul  2 2019 Remi Collet <remi@remirepo.net> - 7.3.7-1
- Update to 7.3.7 - http://www.php.net/releases/7_3_7.php
- disable opcache.huge_code_pages in default configuration

* Thu Jun 20 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC3-1
- update to 7.3.7RC3

* Tue Jun 18 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC2-1
- update to 7.3.7RC2

* Mon Jun 17 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC1-2
- use oracle client library version 19.3

* Tue Jun 11 2019 Remi Collet <remi@remirepo.net> - 7.3.7~RC1-1
- update to 7.3.7RC1

* Tue May 28 2019 Remi Collet <remi@remirepo.net> - 7.3.6-3
- Update to 7.3.6 - http://www.php.net/releases/7_3_6.php

* Thu May 16 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-3
- add httpd and nginx configuration files for FPM in documentation

* Wed May 15 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-2
- update to 7.3.6RC1 (new tag)

* Tue May 14 2019 Remi Collet <remi@remirepo.net> - 7.3.6~RC1-1
- update to 7.3.6RC1

* Wed May  1 2019 Remi Collet <remi@remirepo.net> - 7.3.5-1
- Update to 7.3.5 - http://www.php.net/releases/7_3_5.php

* Tue Apr 16 2019 Remi Collet <remi@remirepo.net> - 7.3.5~RC1-1
- update to 7.3.5RC1

* Fri Apr  5 2019 Remi Collet <remi@remirepo.net> - 7.3.4-2
- build with system oniguruma5

* Tue Apr  2 2019 Remi Collet <remi@remirepo.net> - 7.3.4-1
- Update to 7.3.4 - http://www.php.net/releases/7_3_4.php

* Thu Mar 21 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-2
- update to 7.3.4RC1 new tag
- add upstream patches for failed tests

* Tue Mar 19 2019 Remi Collet <remi@remirepo.net> - 7.3.4~RC1-1
- update to 7.3.4RC1

* Tue Mar  5 2019 Remi Collet <remi@remirepo.net> - 7.3.3-1
- Update to 7.3.3 - http://www.php.net/releases/7_3_3.php
- add upstream patch for OpenSSL 1.1.1b

* Fri Feb 22 2019 Remi Collet <remi@remirepo.net> - 7.3.3~RC1-2
- php-devel: drop dependency on libicu-devel

* Tue Feb 19 2019 Remi Collet <remi@remirepo.net> - 7.3.3~RC1-1
- update to 7.3.3RC1
- adapt systzdata patch (v18)

* Mon Feb 18 2019 Remi Collet <remi@remirepo.net> - 7.3.2-2
- pdo_oci: backport PDOStatement::getColumnMeta from 7.4
- rebuild using libicu62
- drop configuration for ZTS mod_php (Fedora >= 27)

* Wed Feb  6 2019 Remi Collet <remi@remirepo.net> - 7.3.2-1
- Update to 7.3.2 - http://www.php.net/releases/7_3_2.php

* Tue Jan 22 2019 Remi Collet <remi@remirepo.net> - 7.3.2~RC1-1
- update to 7.3.2RC1
- update system tzdata patch for timelib 2018.01

* Tue Jan  8 2019 Remi Collet <remi@remirepo.net> - 7.3.1-1
- Update to 7.3.1 - http://www.php.net/releases/7_3_1.php

* Tue Dec 18 2018 Remi Collet <remi@remirepo.net> - 7.3.1~RC1-1
- update to 7.3.1RC1
- oci8 version is now 2.1.8

* Tue Dec  4 2018 Remi Collet <remi@remirepo.net> - 7.3.0-1
- update to 7.3.0 GA
- update FPM configuration from upstream

* Fri Nov 30 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc6-2
- EL-8 build

* Tue Nov 20 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc6-1
- update to 7.3.0RC6

* Tue Nov  6 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc5-1
- update to 7.3.0RC5

* Wed Oct 24 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc4-1
- update to 7.3.0RC4

* Tue Oct  9 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc3-1
- update to 7.3.0RC3

* Tue Sep 25 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc2-1
- update to 7.3.0RC2
- use oracle client library version 18.3

* Tue Sep 11 2018 Remi Collet <remi@remirepo.net> - 7.3.0~rc1-1
- update to 7.3.0RC1
- with oniguruma 6.9.0

* Tue Aug 28 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta3-1
- update to 7.3.0beta3

* Wed Aug 22 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta2-2
- drop -mstackrealign option, workaround to #1593144

* Tue Aug 21 2018 Remi Collet <remi@remirepo.net> - 7.3.0~beta2-1
- update to 7.3.0beta2
- bump API numbers

* Wed Aug 15 2018 Remi Collet <remi@remirepo.net> - 7.2.9-1
- Update to 7.2.9 - http://www.php.net/releases/7_2_9.php

* Tue Jul 17 2018 Remi Collet <remi@remirepo.net> - 7.2.8-1
- Update to 7.2.8 - http://www.php.net/releases/7_2_8.php

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-2
- FPM: add getallheaders, backported from 7.3

* Tue Jul  3 2018 Remi Collet <remi@remirepo.net> - 7.2.8~RC1-1
- update to 7.2.8RC1

* Wed Jun 20 2018 Remi Collet <remi@remirepo.net> - 7.2.7-1
- Update to 7.2.7 - http://www.php.net/releases/7_2_7.php

* Wed Jun  6 2018 Remi Collet <remi@remirepo.net> - 7.2.7~RC1-1
- update to 7.2.7RC1

* Wed May 23 2018 Remi Collet <remi@remirepo.net> - 7.2.6-1
- Update to 7.2.6 - http://www.php.net/releases/7_2_6.php

* Mon May 14 2018 Remi Collet <remi@remirepo.net> - 7.2.6~RC1-2
- rebuild against EL 7.5

* Sun May 13 2018 Remi Collet <remi@remirepo.net> - 7.2.6~RC1-1
- update to 7.2.6RC1

* Tue Apr 24 2018 Remi Collet <remi@remirepo.net> - 7.2.5-1
- Update to 7.2.5 - http://www.php.net/releases/7_2_5.php

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 7.2.5~RC1-1
- update to 7.2.5RC1

* Tue Apr  3 2018 Remi Collet <remi@remirepo.net> - 7.2.4-2
- add upstream patch for oniguruma 6.8.1, FTBFS #1562583

* Tue Mar 27 2018 Remi Collet <remi@remirepo.net> - 7.2.4-1
- Update to 7.2.4 - http://www.php.net/releases/7_2_4.php
- FPM: update default pool configuration for process.dumpable

* Wed Mar 21 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-3
- use systemd RuntimeDirectory instead of /etc/tmpfiles.d

* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-2
- add file trigger to restart the php-fpm service
  when new pool or new extension installed (F27+)

* Tue Mar 13 2018 Remi Collet <remi@remirepo.net> - 7.2.4~RC1-1
- update to 7.2.4RC1

* Fri Mar  2 2018 Remi Collet <remi@remirepo.net> - 7.2.3-2
- devel: drop dependency on devtoolset

* Wed Feb 28 2018 Remi Collet <remi@remirepo.net> - 7.2.3-1
- Update to 7.2.3 - http://www.php.net/releases/7_2_3.php
- FPM: revert pid file removal
- improve devel dependencies

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-2
- rebuild for new tag and drop patch merged upstream
- drop ldconfig scriptlets on F28

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 7.2.3~RC1-1
- update to 7.2.3RC1
- adapt systzdata, fixheader and ldap_r patches
- apply upstream patch for date ext

* Tue Jan 30 2018 Remi Collet <remi@remirepo.net> - 7.2.2-1
- Update to 7.2.2 - http://www.php.net/releases/7_2_2.php

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-2
- dba: revert drop gdbm support

* Tue Jan 16 2018 Remi Collet <remi@remirepo.net> - 7.2.2~RC1-1
- update to 7.2.2RC1
- define SOURCE_DATE_EPOCH for reproducible build
- dba: drop gdbm support

* Wed Jan 10 2018 Remi Collet <remi@remirepo.net> - 7.2.1-2
- rebuild for gdbm 1.14 BC break (see rhbz#1532997)

* Wed Jan  3 2018 Remi Collet <remi@remirepo.net> - 7.2.1-1
- Update to 7.2.1 - http://www.php.net/releases/7_2_1.php

* Wed Dec 13 2017 Remi Collet <remi@remirepo.net> - 7.2.1~RC1-1
- update to 7.2.1RC1

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-2
- refresh patch for https://bugs.php.net/75514

* Tue Nov 28 2017 Remi Collet <remi@remirepo.net> - 7.2.0-1
- update to 7.2.0 GA

* Tue Nov  7 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC6-1
- update to 7.2.0RC6

* Tue Oct 24 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC5-1
- update to 7.2.0RC5

* Wed Oct 18 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC4-2
- enable argon2 password hash

* Tue Oct 10 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC4-1
- update to 7.2.0RC4
- oci8 version is now 2.1.8
- dont obsolete php-pecl-libsodium

* Tue Sep 26 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC3-1
- update to 7.2.0RC2

* Mon Sep 25 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-3
- F27: php now requires php-fpm and start it with httpd / nginx

* Thu Sep 14 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-2
- update builder from RHEL 7.3 to RHEL 7.4

* Wed Sep 13 2017 Remi Collet <remi@remirepo.net> - 7.2.0~RC2-1
- update to 7.2.0RC2

* Thu Aug 31 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC1-2
- add patch for EL-6, fix undefined symbol: sqlite3_errstr

* Wed Aug 30 2017 Remi Collet <remi@fedoraproject.org> - 7.2.0~RC1-1
- update to 7.2.0RC1

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

