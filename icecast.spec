Summary:	Icecast - streaming MP3 server
Name:		icecast
Version:	1.3.7
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://www.icecast.org/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.init
URL:		http://www.icecast.org/
BuildRequires:	readline-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Icecast is an Internet based broadcasting system based on the Mpeg
Layer III streaming technology. It was originally inspired by
Nullsoft's Shoutcast and also mp3serv by Scott Manley. The icecast
project was started for several reasons: a) all broadcasting systems
were pretty much closed source, non-free software implementations, b)
Shoutcast doesn't allow you to run your own directory servers, or
support them, and c) we thought it would be a lot of fun.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-libwrap \
	--with-readline \
	--enable-fsstd

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/icecast

%post
chkconfig --add icecast

%preun
if [ "$1" = 0 ] ; then
	chkconfig --del icecast
fi

%clean
rm -r $RPM_BUILD_ROOT

%files 
%defattr(644,root,root,755)
%doc doc/manual.html 
%dir %{_sysconfdir}/icecast
%attr(600,root,root) %{_sysconfdir}/icecast/*
%attr(754,root,root) /etc/rc.d/init.d/icecast
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/icecast
/var/log/icecast
