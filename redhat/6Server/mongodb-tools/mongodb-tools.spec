%global mongoarch x86_64
%global mongodist rhel70

Name:		mongodb-tools
Version:	3.0.6
Release:	0%{?dist}
Summary:	MongoDB tools

Group:		Applications/Databases
License:	AGPL 3.0
URL:		http://www.mongodb.org
Source0:	https://fastdl.mongodb.org/linux/mongodb-linux-%{mongoarch}-%{mongodist}-%{version}.tgz

%description
This package contains standard utilities for interacting with MongoDB.


%prep
%setup -q -n mongodb-linux-%{mongoarch}-%{mongodist}-%{version}


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 bin/* %{buildroot}%{_bindir}/


%files
%doc README THIRD-PARTY-NOTICES GNU-AGPL-3.0
%{_bindir}/*
%exclude %{_bindir}/mongo
%exclude %{_bindir}/mongod
%exclude %{_bindir}/mongoperf
%exclude %{_bindir}/mongos


%changelog
* Mon Sep 21 2015 Matthias Saou <matthias@saou.eu> 3.0.6-0
- Update to 3.0.6.

* Mon Jun 29 2015 Matthias Saou <matthias@saou.eu> 3.0.4-0
- Update to 3.0.4.

* Tue May 19 2015 Matthias Saou <matthias@saou.eu> 3.0.3-0
- Initial RPM build.
- Use binaries until those Go binaries can be easily built...

