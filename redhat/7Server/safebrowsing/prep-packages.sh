#!/bin/bash
#
# VERY rough around the edges. 'Just works' as ./prep-packages.sh
#

# This gets the version string from the .spec file, so change it there first
VERSION="$(grep "^%define ghscommit" safebrowsing.spec | awk '{print $3}')"

rm -rf safebrowsing-*

git clone git@github.com:google/safebrowsing safebrowsing-${VERSION}
cd safebrowsing-${VERSION}
git checkout "${VERSION}"
# Get the generated go files before getting rid of git artifacts
go generate

rm -rf .git* vendor
cd ..
tar czf safebrowsing-${VERSION}.tar.gz safebrowsing-${VERSION}
rm -rf safebrowsing-${VERSION}
ls -lh safebrowsing-${VERSION}.tar.gz

mkdir safebrowsing-packages
cd safebrowsing-packages
export GOPATH="${PWD}"
go get github.com/golang/protobuf
go get github.com/rakyll/statik
go get golang.org/x/net

find . -type d -name .git | xargs rm -rf
rm -rf pkg

cd ..
tar czf safebrowsing-packages.tar.gz safebrowsing-packages
rm -rf safebrowsing-packages
ls -lh safebrowsing-packages.tar.gz

