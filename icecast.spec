Summary:	Icecast - streaming MP3 server
Summary(es):	Un servidor de streams MP3
Summary(pl):	Icecast - Serwer strumieni MP3
Summary(pt_BR):	Um servidor de streams MP3
Name:		icecast
Version:	1.3.12
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.icecast.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	69ba36d30722884ea538b70628f1de80
Source1:	%{name}.init
Patch0:		%{name}-am15.patch
Patch1:		%{name}-errno.patch
URL:		http://www.icecast.org/
BuildRequires:	readline-devel
BuildRequires:	autoconf
BuildRequires:	automake
PreReq:		rc-scripts
Requires(pre): /bin/id
Requires(pre): /usr/bin/getgid
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(postun):      /usr/sbin/groupdel
Requires(postun):      /usr/sbin/userdel
Requires(post,preun):	/sbin/chkconfig
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Icecast is an Internet based broadcasting system based on the Mpeg
Layer III streaming technology. It was originally inspired by
Nullsoft's Shoutcast and also mp3serv by Scott Manley. The icecast
project was started for several reasons: a) all broadcasting systems
were pretty much closed source, non-free software implementations, b)
Shoutcast doesn't allow you to run your own directory servers, or
support them, and c) we thought it would be a lot of fun.

%description -l es
Icecast es un sistema de Transmisión (broadcast) en Internet que
utiliza la tecnología MP3.

%description -l pl
Icecast to Internetowy serwer rozsy³aj±cy strumienie MPEG Layer III.
Oryginalnie zainspirowany przez Shoutcast firmy Nullsoft oraz program
mp3serv autorstwa Scotta Manleya. Projekt icecast zosta³ rozpoczêty z
kilku powodów: a) wszystkie systemy broadcastowe by³y ³adnymi,
zamkniêtymi programami, non-free, b) Shoutcast nie pozwala na
wystartowanie swoich w³asnych directory servers czy wspieraæ ich, c)
to niez³a zabawa.

%description -l pt_BR
O Icecast é um sistema de broadcast na Internet que utiliza a
tecnologia MP3.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
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
%doc doc/manual.html
%dir %{_sysconfdir}/icecast
%attr(640,root,icecast) %{_sysconfdir}/icecast/*
%attr(754,root,root) /etc/rc.d/init.d/icecast
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/icecast
%attr(770,root,icecast) /var/log/icecast
