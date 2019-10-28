%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

# Use latest git, until regular and standardized releases will be available.
# We can't download (for now) download release tarball or last. Thats why we need download git by hand.

%define gitdate 28.10.2019

Name:       aom
Version:    1.0.0
Release:    0.%{gitdate}
Summary:    Royalty-free next-generation video format
Group:      System/Libraries
License:    BSD
URL:        http://aomedia.org/
#Source should be taken from: https://aomedia.googlesource.com/aom/
Source0:    %{name}-%{gitdate}.tar.xz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  perl(Getopt::Long)
BuildRequires:  wxgtku3.0-devel
BuildRequires:  yasm

Provides:       av1 = %{version}-%{release}

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


%package extra-tools
Summary:        Extra tools for aom
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description extra-tools
This package contains the aom analyzer.


%package -n %{libname}
Summary:        Library files for aom
Group:          System/Libraries

%description -n %{libname}
Library files for aom, the royalty-free next-generation 
video format.


%package -n %{develname}
Summary:        Development files for aom
Group:          Development/C
Requires:       %{name} = %{version}-%{release}

%description -n %{develname}
Development files for aom, the royalty-free next-generation 
video format.


%prep
%autosetup -p1 -n %{name}-%{gitdate}


%build
%cmake -Wno-dev -DENABLE_CCACHE=1 \
            -DCMAKE_SKIP_RPATH=1 \
%ifnarch aarch64 %{arm} %{ix86} x86_64
            -DAOM_TARGET_CPU=generic \
%endif
%ifarch %{arm}
            -DAOM_TARGET_CPU=arm \
%endif
%ifarch aarch64
            -DAOM_TARGET_CPU=arm64 \
%endif
%ifarch %{ix86}
            -DAOM_TARGET_CPU=x86 \
%endif
%ifarch x86_64
            -DAOM_TARGET_CPU=x86_64 \
%endif
            -DCONFIG_WEBM_IO=1 \
            -DENABLE_DOCS=1 \
            -DCONFIG_ANALYZER=1 \
            -DCONFIG_LOWBITDEPTH=1
%make_build


%install
%make_install -C build

install -pm 0755 build/examples/analyzer %{buildroot}%{_bindir}/aomanalyzer


%files
%doc AUTHORS CHANGELOG README.md
%license LICENSE PATENTS
%{_bindir}/aomdec
%{_bindir}/aomenc


%files extra-tools
%{_bindir}/aomanalyzer


%files -n %{libname}
%license LICENSE PATENTS
%{_libdir}/libaom.so.%{major}{,.*}


%files -n %{develname}
%doc build/docs/html/
%{_includedir}/%{name}
%{_libdir}/libaom.so
%{_libdir}/pkgconfig/%{name}.pc
