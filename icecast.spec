Summary:   Icecast - streaming MP3 server
Name:      icecast
Version:   1.3.0
Release:   2mdk
Serial:    1301
URL:       http://www.icecast.org
Source0:   http://www.icecast.org/releases/%{name}-%{version}.tar.bz2
Source1:   icecast.init
Patch:     icecast-config.patch.bz2
Copyright: GPL
Group:     System Environment/Daemons
Buildroot: /tmp/%{name}-%{version}-root

%description
Icecast is an Internet based broadcasting system based on the Mpeg Layer III
streaming technology.  It was originally inspired by Nullsoft's Shoutcast
and also mp3serv by Scott Manley.  The icecast project was started for several
reasons: a) all broadcasting systems were pretty much closed source,
non-free software implementations, b) Shoutcast doesn't allow you to run your
own directory servers, or support them, and c) we thought it would be a
lot of fun.

%prep
%setup -q -n %{name}-1.3

%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --with-libwrap

( cd liveice
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr )

make
make -C liveice

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/usr/share/icecast/files
install -d $RPM_BUILD_ROOT/usr/share/icecast/templates
install -d $RPM_BUILD_ROOT/usr/sbin

make prefix=$RPM_BUILD_ROOT/usr \
     templatedir=$RPM_BUILD_ROOT/usr/share/icecast \
     etcdir=$RPM_BUILD_ROOT/etc \
     logdir=$RPM_BUILD_ROOT/var/log/icecast \
     install

install -m755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/icecast
install -m755 shout/iceplay $RPM_BUILD_ROOT/usr/bin

mv -f $RPM_BUILD_ROOT/usr/bin/icecast $RPM_BUILD_ROOT/usr/sbin
mv -f $RPM_BUILD_ROOT/usr/bin/liveice $RPM_BUILD_ROOT/usr/sbin

strip $RPM_BUILD_ROOT/usr/{bin/*,sbin/*} || :

%post
chkconfig --add icecast

%preun
if [ "$1" = 0 ] ; then
  chkconfig --del icecast
fi

%clean
rm -r $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc doc/* icedir liveice/README.* liveice/livepipe.c liveice/mpg123_liveice.diff
%doc shout/*.example shout/README.*
%attr(600,root,root) %config /etc/icecast.conf
%attr(600,root,root) %config /etc/liveice.cfg
%config /etc/rc.d/init.d/icecast
/usr/bin/*
/usr/sbin/*
/usr/share/icecast
/var/log/icecast

%changelog
* Mon Jul 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Adaptations for Mandrake distribution.

* Fri Jul 16 1999 Arne Coucheron <arneco@online.no>
  [1.3.0-1]
- added more documentation
- deactivation of icecast init file moved to %preun
- some changes in the %install section
- changed Group: tag

* Tue Apr 13 1999 Arne Coucheron <arneco@online.no>
  [1.1.4-1]
- added serial tag to let it make it into RH contrib

* Mon Mar 13 1999 Arne Coucheron <arneco@online.no>
  [1.1.3-1]
- added liveice program and config file

* Fri Mar 05 1999 Arne Coucheron <arneco@online.no>
  [1.1.2-1]

* Wed Mar 03 1999 Arne Coucheron <arneco@online.no>
  [1.1.0-2]
- a small change in the init script

* Tue Mar 02 1999 Arne Coucheron <arneco@online.no>
  [1.1.0-1]
- first RPM build
