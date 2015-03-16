Name:           giflossy
Version:        1.82.1
Release:        1%{?dist}
Summary:        Powerful program for manipulating GIF images and animations

Group:          Applications/File
License:        GPLv2+
URL:            https://pornel.net/lossygif
Source0:        https://github.com/pornel/giflossy/archive/lossy/%{version}.tar.gz

BuildRequires:  autoconf, automake, libtool
BuildRequires:  libX11-devel


%description
Gifsicle is a command-line tool for creating, editing, and getting
information about GIF images and animations.

Some more gifsicle features:

    * Batch mode for changing GIFs in place.
    * Prints detailed information about GIFs, including comments.
    * Control over interlacing, comments, looping, transparency...
    * Creates well-behaved GIFs: removes redundant colors, only uses local
      color tables if it absolutely has to (local color tables waste space
      and can cause viewing artifacts), etc.
    * It can shrink colormaps and change images to use the Web-safe palette
      (or any colormap you choose).
    * It can optimize your animations! This stores only the changed portion
      of each frame, and can radically shrink your GIFs. You can also use
      transparency to make them even smaller. Gifsicle?s optimizer is pretty
      powerful, and usually reduces animations to within a couple bytes of
      the best commercial optimizers.
    * Unoptimizing animations, which makes them easier to edit.
    * A dumb-ass name.

One other program is included with gifsicle
and gifdiff compares two GIFs for identical visual appearance.

This is a fork which includes lossy (re)compression.


%prep
%setup -q -n giflossy-lossy-%{version}


%build
./bootstrap.sh
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc COPYING NEWS README.md
%{_bindir}/gifdiff
%{_bindir}/gifsicle
%{_mandir}/man1/gifdiff.1*
%{_mandir}/man1/gifsicle.1*

#files -n gifview
#doc COPYING NEWS README.md
%exclude %{_bindir}/gifview
%exclude %{_mandir}/man1/gifview.1*


%changelog
* Mon Mar 16 2015 Matthias Saou <matthias@saou.eu> 1.82.1-1
- Initial RPM release based on gifsicle package.

