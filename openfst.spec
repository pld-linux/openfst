#
# Conditional build:
%bcond_without	python		# python extensions
%bcond_without	static_libs	# static library
#
Summary:	OpenFst - library for finite state transducers development
Summary(pl.UTF-8):	OpenFst - biblioteka do programowania automatów skończonych z wyjściem
Name:		openfst
Version:	1.5.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: http://www.openfst.org/twiki/bin/view/FST/FstDownload
Source0:	http://www.openfst.org/twiki/pub/FST/FstDownload/%{name}-%{version}.tar.gz
# Source0-md5:	a24fee5ffe28744c6fb7b1a49e0006c4
Patch0:		%{name}-link.patch
Patch1:		%{name}-python.patch
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
%patch1 -p1

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
	%{?with_python:$RPM_BUILD_ROOT%{py_sitedir}/fst.la}
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/fst/*.a \
	%{?with_python:$RPM_BUILD_ROOT%{py_sitedir}/fst.a}
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
%attr(755,root,root) %ghost %{_libdir}/libfst.so.1
%attr(755,root,root) %{_libdir}/libfstscript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfstscript.so.1
%dir %{_libdir}/fst
%attr(755,root,root) %{_libdir}/fst/*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfst.so
%attr(755,root,root) %{_libdir}/libfstscript.so
%{_libdir}/libfst.la
%{_libdir}/libfstscript.la
%{_includedir}/fst

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfst.a
%{_libdir}/libfstscript.a
%endif

%if %{with python}
%files -n python-openfst
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/fst.so
%endif
