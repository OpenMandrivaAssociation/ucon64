Summary:	Console ROM backup tool
Name:		ucon64
Version:	2.0.0
Release:	10
Group:		Emulators
License:	GPLv2
URL:		https://ucon64.sf.net/
Source0:	http://prdownloads.sourceforge.net/ucon64/%{name}-%{version}-src.tar.bz2
Source1:	http://prdownloads.sourceforge.net/ucon64/uf-FOX-1.1-src.tgz
Patch0:		uf-FOX-1.1-libfox1.7.patch
Patch1:		uf-FOX-1.1-ptrfix.patch
Patch2:		ucon64-2.0.0-gzfile.patch
Patch3:		ucon64-2.0.0-ovflfix.patch
BuildRequires:	libusb-devel
BuildRequires:	zlib-devel
BuildRequires:	fox1.7-devel
# ld will fail with fatal error, it needs static lib only
BuildConflicts:	ieee1284-devel

%package -n %{name}-gui
Summary:	GUI for Ucon64, a console ROM backup tool
Group:		Emulators
Requires:	%{name}

%description
uCON64 is a console ROM backup tool.

%description -n %{name}-gui
GUI for Ucon64, a console ROM backup tool

%prep
%setup -q -n %{name}-%{version}-src -a 1
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1

#no configure script for the gui :(
perl -pi -e "s/local\///g" uf-FOX-1.1-src/Makefile
LIBFOX_VERSION=1.7
perl -pi -e "s/1\.4/$LIBFOX_VERSION/g" uf-FOX-1.1-src/Makefile

%build
cd src
%configure --enable-libcd64 --with-libusb --enable-ppdev
%make

pushd ../uf-FOX-1.1-src
make
popd

%install
# don't use %%makeinstall here
install -d %{buildroot}%{_bindir}
install -m 755 src/%{name} %{buildroot}%{_bindir}

#install gui
install -m 755 uf-FOX-1.1-src/uf %{buildroot}%{_bindir}
chmod 644 uf-FOX-1.1-src/README.txt
#note : add a icon & menu entry

%files
%doc FILE_ID.DIZ VERSION *.html
%{_bindir}/ucon64

%files -n %{name}-gui
%doc uf-FOX-1.1-src/README.txt uf-FOX-1.1-src/gpl.txt
%{_bindir}/uf

