#!/bin/bash

PKG="docker_auth-packages"

mkdir ${PKG}
cd ${PKG}
export GOPATH="${PWD}"
go get github.com/tools/godep
go get github.com/jteeuwen/go-bindata
go get gopkg.in/yaml.v2
go get github.com/go-fsnotify/fsnotify
go get github.com/jmoiron/sqlx
go get github.com/lib/pq
go get github.com/spf13/cobra
go get github.com/spf13/pflag
go get github.com/go-sql-driver/mysql
go get github.com/deckarep/golang-set
go get github.com/facebookgo/httpdown
go get github.com/golang/glog
go get github.com/dchest/uniuri
go get github.com/docker/distribution/registry/auth/token
go get github.com/docker/libtrust
go get github.com/go-ldap/ldap
go get github.com/syndtr/goleveldb/leveldb
go get golang.org/x/crypto/bcrypt
go get gopkg.in/fsnotify.v1
go get gopkg.in/mgo.v2

find . -type d -name .git | xargs rm -rf
rm -rf pkg

cd ..
tar czf ${PKG}.tar.gz ${PKG}
rm -rf ${PKG}
ls -lh ${PKG}.tar.gz

