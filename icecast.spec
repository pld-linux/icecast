Summary:	Icecast - streaming MP3 server
Summary(pl):	Serwer strumieni MP3
Name:		icecast
Version:	1.3.11
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.icecast.org/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-am15.patch
URL:		http://www.icecast.org/
BuildRequires:	readline-devel
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Icecast is an Internet based broadcasting system based on the Mpeg
Layer III streaming technology. It was originally inspired by
Nullsoft's Shoutcast and also mp3serv by Scott Manley. The icecast
project was started for several reasons: a) all broadcasting systems
were pretty much closed source, non-free software implementations, b)
Shoutcast doesn't allow you to run your own directory servers, or
support them, and c) we thought it would be a lot of fun.

%description -l pl
Icecast to Internetowy serwer rozsy³aj±cy strumienie MPEG Layer III.
Oryginalnie zainspirowany przez Shoutcast firmy Nullsoft oraz program
mp3serv autorswa Scotta Manleya.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c
%configure \
	--with-readline \
	--enable-fsstd

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/icecast

%clean
rm -r $RPM_BUILD_ROOT

%post
chkconfig --add icecast
if [ -f /var/lock/subsys/icecast ]; then
	/etc/rc.d/init.d/icecast restart >&2
else
	echo "Run '/etc/rc.d/init.d/icecast start' to start icecast deamon." >&2
fi

%preun
if [ "$1" = "0" ] ; then
	if [ -f /var/lock/subsys/icecast ]; then
		/etc/rc.d/init.d/icecast stop >&2
	fi
	/sbin/chkconfig --del icecast >&2
fi

%files 
%defattr(644,root,root,755)
%doc doc/manual.html 
%dir %{_sysconfdir}/icecast
%attr(600,root,root) %{_sysconfdir}/icecast/*
%attr(754,root,root) /etc/rc.d/init.d/icecast
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/icecast
/var/log/icecast
