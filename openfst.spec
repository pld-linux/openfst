#
# Conditional build:
%bcond_without	python		# python extensions
%bcond_without	static_libs	# static library
#
Summary:	OpenFst - library for finite state transducers development
Summary(pl.UTF-8):	OpenFst - biblioteka do programowania automatów skończonych z wyjściem
Name:		openfst
Version:	1.6.5
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: http://www.openfst.org/twiki/bin/view/FST/FstDownload
Source0:	http://www.openfst.org/twiki/pub/FST/FstDownload/%{name}-%{version}.tar.gz
# Source0-md5:	60bed07f4f5857d9be2e6f1ab3a2f055
Patch0:		%{name}-python.patch
URL:		http://www.openfst.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:1.5
%{?with_python:BuildRequires:	python-devel >= 1:2.7}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# modules dlopened from libfst refer to symbols from the library
%define		skip_post_check_so	.*%{_libdir}/fst/.*\.so.*

%description
OpenFst is a library for constructing, combining, optimizing, and
searching weighted finite-state transducers (FSTs).

%description -l pl.UTF-8
OpenFst to biblioteka do konstruowania, łączenia, optymalizacji i
przeszukiwania automatów skończonych z wyjściem (FST) i wagami.

%package devel
Summary:	Header files for OpenFst library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenFst
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for OpenFst library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenFst.

%package static
Summary:	Static OpenFst library
Summary(pl.UTF-8):	Statyczna biblioteka OpenFst
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenFst library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenFst.

%package -n python-openfst
Summary:	Python binding for OpenFst
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki OpenFst
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.7

%description -n python-openfst
Python binding for OpenFst.

%description -n python-openfst -l pl.UTF-8
Wiązanie Pythona do biblioteki OpenFst.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-compact-fsts \
	--enable-compress \
	--enable-const-fsts \
	--enable-far \
	--enable-linear-fsts \
	--enable-lookahead-fsts \
	--enable-mpdt \
	--enable-ngram-fsts \
	--enable-pdt \
	--enable-python \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/fst/*.la \
	%{?with_python:$RPM_BUILD_ROOT%{py_sitedir}/pywrapfst.la}
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/fst/*.a \
	%{?with_python:$RPM_BUILD_ROOT%{py_sitedir}/pywrapfst.a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_bindir}/far*
%attr(755,root,root) %{_bindir}/fst*
%attr(755,root,root) %{_bindir}/mpdt*
%attr(755,root,root) %{_bindir}/pdt*
%attr(755,root,root) %{_libdir}/libfst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfst.so.8
%attr(755,root,root) %{_libdir}/libfstcompact.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstcompact.so.8
%attr(755,root,root) %{_libdir}/libfstcompressscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstcompressscript.so.8
%attr(755,root,root) %{_libdir}/libfstconst.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstconst.so.8
%attr(755,root,root) %{_libdir}/libfstfar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstfar.so.8
%attr(755,root,root) %{_libdir}/libfstfarscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstfarscript.so.8
%attr(755,root,root) %{_libdir}/libfstlinearscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstlinearscript.so.8
%attr(755,root,root) %{_libdir}/libfstlookahead.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstlookahead.so.8
%attr(755,root,root) %{_libdir}/libfstmpdtscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstmpdtscript.so.8
%attr(755,root,root) %{_libdir}/libfstngram.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstngram.so.8
%attr(755,root,root) %{_libdir}/libfstpdtscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstpdtscript.so.8
%attr(755,root,root) %{_libdir}/libfstscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstscript.so.8
%dir %{_libdir}/fst
%attr(755,root,root) %{_libdir}/fst/*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfst.so
%attr(755,root,root) %{_libdir}/libfstcompact.so
%attr(755,root,root) %{_libdir}/libfstcompressscript.so
%attr(755,root,root) %{_libdir}/libfstconst.so
%attr(755,root,root) %{_libdir}/libfstfar.so
%attr(755,root,root) %{_libdir}/libfstfarscript.so
%attr(755,root,root) %{_libdir}/libfstlinearscript.so
%attr(755,root,root) %{_libdir}/libfstlookahead.so
%attr(755,root,root) %{_libdir}/libfstmpdtscript.so
%attr(755,root,root) %{_libdir}/libfstngram.so
%attr(755,root,root) %{_libdir}/libfstpdtscript.so
%attr(755,root,root) %{_libdir}/libfstscript.so
%{_libdir}/libfst.la
%{_libdir}/libfstcompact.la
%{_libdir}/libfstcompressscript.la
%{_libdir}/libfstconst.la
%{_libdir}/libfstfar.la
%{_libdir}/libfstfarscript.la
%{_libdir}/libfstlinearscript.la
%{_libdir}/libfstlookahead.la
%{_libdir}/libfstmpdtscript.la
%{_libdir}/libfstngram.la
%{_libdir}/libfstpdtscript.la
%{_libdir}/libfstscript.la
%{_includedir}/fst

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfst.a
%{_libdir}/libfstcompact.a
%{_libdir}/libfstcompressscript.a
%{_libdir}/libfstconst.a
%{_libdir}/libfstfar.a
%{_libdir}/libfstfarscript.a
%{_libdir}/libfstlinearscript.a
%{_libdir}/libfstlookahead.a
%{_libdir}/libfstmpdtscript.a
%{_libdir}/libfstngram.a
%{_libdir}/libfstpdtscript.a
%{_libdir}/libfstscript.a
%endif

%if %{with python}
%files -n python-openfst
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pywrapfst.so
%endif
