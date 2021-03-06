# ffmpeg uses aom, wine uses ffmpeg
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s
%define lib32name %mklib32name %{name} %{major}
%define devel32name %mklib32name %{name} -d
%define static32name %mklib32name %{name} -d -s

# Use latest git, until regular and standardized releases will be available.
# We can't download (for now) download release tarball or last. Thats why we need download git by hand.
# Use the YYYY.MM.DD format to make sure the number always goes up, not down (31.1.2020 > 10.4.2020)
#define gitdate 2020.06.11

Name:		aom
Version:	2.0.2
Release:	1%{?gitdate:.%{gitdate}}
Summary:	Royalty-free next-generation video format
Group:		System/Libraries
License:	BSD
URL:		http://aomedia.org/
# Source for git snapshots should be taken from: https://aomedia.googlesource.com/aom/
# d67d4cb2.... is the commit hash for the v2.0.2 tag
Source0:	https://aomedia.googlesource.com/aom/+archive/d67d4cb2993891fa4e60f5aa7c18c80a98ccc506.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	perl(Getopt::Long)
BuildRequires:	wxgtku3.0-devel
BuildRequires:	yasm
Provides:	av1 = %{version}-%{release}
# aomanalyzer has been removed upstream
Obsoletes:	%{name}-extra-tools < %{EVRD}

%description
The Alliance for Open Media’s focus is to deliver a next-generation
video format that is:

 - Interoperable and open;
 - Optimized for the Internet;
 - Scalable to any modern device at any bandwidth;
 - Designed with a low computational footprint and optimized for hardware;
 - Capable of consistent, highest-quality, real-time video delivery; and
 - Flexible for both commercial and non-commercial content, including
   user-generated content.

This package contains the reference encoder and decoder.

%package -n %{libname}
Summary:	Library files for aom
Group:		System/Libraries

%description -n %{libname}
Library files for aom, the royalty-free next-generation 
video format.

%package -n %{develname}
Summary:	Development files for aom
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files for aom, the royalty-free next-generation 
video format.

%package -n %{staticname}
Summary:	Static library files for aom
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}

%description -n %{staticname}
Static library files for aom, the royalty-free next-generation 
video format.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library files for aom (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
Library files for aom, the royalty-free next-generation 
video format.

%package -n %{devel32name}
Summary:	Development files for aom (32-bit)
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{devel32name}
Development files for aom, the royalty-free next-generation 
video format.

%package -n %{static32name}
Summary:	Static library files for aom (32-bit)
Group:		Development/C
Requires:	%{devel32name} = %{version}-%{release}

%description -n %{static32name}
Static library files for aom, the royalty-free next-generation 
video format.
%endif

%prep
%autosetup -p1 -c -n %{name}%{?gitdate:-%{gitdate}}

%if %{with compat32}
%cmake32 \
	-Wno-dev -DENABLE_CCACHE=1 \
	-DCMAKE_SKIP_RPATH=1 \
	-DAOM_TARGET_CPU=x86 \
	-DCONFIG_WEBM_IO=1 \
	-DENABLE_DOCS=0 \
	-DCONFIG_ANALYZER=0 \
	-DCONFIG_LOWBITDEPTH=1 \
	-G Ninja
cd ..
%endif

%cmake \
	-Wno-dev -DENABLE_CCACHE=1 \
	-DCMAKE_SKIP_RPATH=1 \
%ifnarch aarch64 %{arm} %{ix86} %{x86_64}
	-DAOM_TARGET_CPU=generic \
%endif
%ifarch %{arm}
	-DAOM_TARGET_CPU=arm \
%endif
%ifarch aarch64 riscv64
	-DAOM_TARGET_CPU=arm64 \
%endif
%ifarch %{ix86}
	-DAOM_TARGET_CPU=x86 \
%endif
%ifarch %{x86_64}
	-DAOM_TARGET_CPU=x86_64 \
%endif
	-DCONFIG_WEBM_IO=1 \
	-DENABLE_DOCS=1 \
	-DCONFIG_ANALYZER=1 \
	-DCONFIG_LOWBITDEPTH=1 \
	-G Ninja


%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc

%files -n %{libname}
%license LICENSE PATENTS
%{_libdir}/libaom.so.%{major}{,.*}

%files -n %{develname}
%doc build/docs/html/
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{staticname}
%{_libdir}/libaom.a

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libaom.so.%{major}{,.*}

%files -n %{devel32name}
%{_prefix}/lib/libaom.so
%{_prefix}/lib/pkgconfig/%{name}.pc

%files -n %{static32name}
%{_prefix}/lib/libaom.a
%endif
