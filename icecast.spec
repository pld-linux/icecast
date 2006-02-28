# TODO:
# - logrotate file
Summary:	Icecast - streaming MP3 and Ogg server
Summary(es):	Un servidor de streams MP3, Ogg
Summary(pl):	Icecast - serwer strumieni MP3 i Ogg
Summary(pt_BR):	Um servidor de streams MP3, Ogg
Name:		icecast
Version:	2.3.1
Release:	1
Epoch:		2
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.xiph.org/releases/icecast/%{name}-%{version}.tar.gz
# Source0-md5:	2d80a249fa8529f82d018c6216108ea8
Source1:	%{name}.init
URL:		http://www.icecast.org/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.10.0
BuildRequires:	libogg-devel >= 2:1.0
BuildRequires:	libtheora-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel >= 1:1.0
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	speex-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(icecast)
Provides:	user(icecast)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

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
Icecast to internetowy serwer rozsy³aj±cy strumienie MPEG Layer III.
Oryginalnie zainspirowany przez Shoutcast firmy Nullsoft oraz program
mp3serv autorstwa Scotta Manleya. Projekt icecast2 zosta³ rozpoczêty z
kilku powodów: a) wszystkie systemy broadcastowe by³y ³adnymi,
zamkniêtymi programami, non-free, b) Shoutcast nie pozwala na
wystartowanie swoich w³asnych directory servers czy wspieraæ ich, c)
to niez³a zabawa.

%description -l pt_BR
O Icecast é um sistema de broadcast na Internet que utiliza a
tecnologia MP3.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/log/icecast}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/icecast

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 57 icecast
%useradd -u 57 -r -d /dev/null -s /bin/false -c "Streamcast" -g icecast icecast

%post
/sbin/chkconfig --add icecast
%service icecast restart "icecast deamon"

%preun
if [ "$1" = "0" ] ; then
	%service icecast stop
	/sbin/chkconfig --del icecast >&2
fi

%postun
if [ "$1" = "0" ]; then
	%userremove icecast
	%groupremove icecast
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO doc/*.{html,jpg}
%attr(754,root,root) /etc/rc.d/init.d/icecast
%attr(755,root,root) %{_bindir}/*
%attr(750,root,icecast) %dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.xml
%{_datadir}/icecast
%attr(770,root,icecast) %config(noreplace) %verify(not md5 mtime size) /var/log/icecast
