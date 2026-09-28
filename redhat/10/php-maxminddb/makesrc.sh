#!/bin/bash

NAME=$(basename $PWD)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

echo "Cloning..."
rm -rf $PROJECT-$VERSION
git clone --depth 1 --recursive https://github.com/$OWNER/$PROJECT.git -b v$VERSION $PROJECT-$VERSION

echo "Archiving..."
tar czf $NAME-$VERSION.tgz --exclude-vcs .git $PROJECT-$VERSION

echo "Cleaning..."
rm -rf $PROJECT-$VERSION

echo "Done."
