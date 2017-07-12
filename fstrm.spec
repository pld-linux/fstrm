#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	C implementation of the Frame Streams transport protocol
Summary(pl.UTF-8):	Implementacja protokołu transportowego Frame Streams w języku C
Name:		fstrm
Version:	0.3.2
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/farsightsec/fstrm/releases
Source0:	https://dl.farsightsecurity.com/dist/fstrm/%{name}-%{version}.tar.gz
# Source0-md5:	3ec84f066b5a87f79ef41a30fde88920
URL:		https://github.com/farsightsec/fstrm
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	doxygen
BuildRequires:	libevent-devel >= 2
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Frame Streams is a light weight, binary clean protocol that allows for
the transport of arbitrarily encoded data payload sequences with
minimal framing overhead - just four bytes per data frame. Frame
Streams does not specify an encoding format for data frames and can be
used with any data serialization format that produces byte sequences,
such as Protocol Buffers, XML, JSON, MessagePack, YAML, etc.

fstrm is an optimized C implementation of Frame Streams that includes
a fast, lockless circular queue implementation and exposes library
interfaces for setting up a dedicated Frame Streams I/O thread and
asynchronously submitting data frames for transport from worker
threads. It was originally written to facilitate the addition of high
speed binary logging to DNS servers written in C using the dnstap log
format.

%description -l pl.UTF-8
Frame Streams to lekki, bezpieczny dla binariów protokół pozwalający
na przesyłanie dowolnie zakodowanych sekwencji danych z minimalnym
narzutem na ramki - tylko cztery bajty na jedną. Frame Streams nie
określają formatu kodowania ramek danych i mogą być używane z dowolnym
formatem serializacji tworzącym sekwencje bajtów, takim jak Protocol
Buffers, XML, JSON, MessagePack, YAML itp.

fstrm to zoptymalizowana implementacja Frame Streams w języku C,
zawierająca szybką, pozbawioną blokad kolejkę cykliczną; udostępnia
interfejsy biblioteczne do ustawiania dedykowanego wątku we/wy oraz
asynchronicznego przekazywania ramek danych do przesłania z wątków
roboczych. Pierwotnie powstała, aby ułatwić dodanie bardzo szybkiego,
binarnego logowania w serwerach DNS, napisanych w C, przy użyciu
formatu logu dnstap.

%package devel
Summary:	Header files for fstrm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki fstrm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for fstrm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki fstrm.

%package static
Summary:	Static fstrm library
Summary(pl.UTF-8):	Statyczna biblioteka fstrm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static fstrm library.

%description static -l pl.UTF-8
Statyczna biblioteka fstrm.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libfstrm.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README.md
%attr(755,root,root) %{_bindir}/fstrm_capture
%attr(755,root,root) %{_bindir}/fstrm_dump
%attr(755,root,root) %{_libdir}/libfstrm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstrm.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfstrm.so
%{_includedir}/fstrm
%{_includedir}/fstrm.h
%{_pkgconfigdir}/libfstrm.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfstrm.a
%endif
