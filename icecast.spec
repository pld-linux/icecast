%define	snap	20030913
Summary:	Icecast - streaming MP3 server
Summary(es):	Un servidor de streams MP3
Summary(pl):	Icecast - Serwer strumieni MP3
Summary(pt_BR):	Um servidor de streams MP3
Name:		icecast
Version:	2.0b
Release:	0.%{snap}.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.icecast.org/files/icecast_2.0_nightly_snapshot.tgz
# Source0-md5:	3528ed1cc9eeca9ac3c715eea1f5ff87
Source1:	%{name}.init
URL:		http://www.icecast.org/
BuildRequires:	readline-devel
BuildRequires:	curl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
PreReq:		rc-scripts
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
Icecast2 is an Internet based broadcasting system based on the Mpeg
Layer III streaming technology. It was originally inspired by
Nullsoft's Shoutcast and also mp3serv by Scott Manley. The icecast
project was started for several reasons: a) all broadcasting systems
were pretty much closed source, non-free software implementations, b)
Shoutcast doesn't allow you to run your own directory servers, or
support them, and c) we thought it would be a lot of fun. Unstable
version.

%description -l es
Icecast2 es un sistema de Transmisi�n (broadcast) en Internet que
utiliza la tecnolog�a MP3.

%description -l pl
Icecast2 to internetowy serwer rozsy�aj�cy strumienie MPEG Layer III.
Oryginalnie zainspirowany przez Shoutcast firmy Nullsoft oraz program
mp3serv autorstwa Scotta Manleya. Projekt icecast2 zosta� rozpocz�ty z
kilku powod�w: a) wszystkie systemy broadcastowe by�y �adnymi,
zamkni�tymi programami, non-free, b) Shoutcast nie pozwala na
wystartowanie swoich w�asnych directory servers czy wspiera� ich, c)
to niez�a zabawa. Uwaga - to ci�gle wersja unstable.

%description -l pt_BR
O Icecast � um sistema de broadcast na Internet que utiliza a
tecnologia MP3.

%prep
%setup -q -n %{name}

%build
./autogen.sh
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,var/log/icecast}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/icecast

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid icecast`" ]; then
	if [ "`/usr/bin/getgid icecast`" != "57" ]; then
		echo "Error: group icecast doesn't have gid=57. Correct this before installing icecast." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 57 -r -f icecast
fi
if [ -n "`/bin/id -u icecast 2>/dev/null`" ]; then
	if [ "`/usr/bin/getgid icecast`" != "57" ]; then
		echo "Error: user icecast doesn't have uid=57. Correct this before installing icecast." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 57 -r -d /dev/null -s /bin/false -c "Streamcast" -g icecast icecast 1>&2
fi

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

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel icecast 2>/dev/null
	/usr/sbin/groupdel icecast 2>/dev/null
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO doc/*.{html,jpg}
%attr(754,root,root) /etc/rc.d/init.d/icecast
%attr(755,root,root) %{_bindir}/*
%attr(750,root,icecast) %{_sysconfdir}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.xml
%{_datadir}/icecast
%attr(770,root,icecast) /var/log/icecast
