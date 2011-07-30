%define name ucon64
%define version 2.0.0
#define subversion 4
#define release	4.3plf
%define release %mkrel 5

Summary: Console ROM backup tool
Name: %{name}
Version: %{version}
Release: %{release}
Group: Emulators
License: GPLv2
URL: http://ucon64.sf.net/
#Source0: http://prdownloads.sourceforge.net/ucon64/%{name}-%{version}-%{subversion}-src.tar.bz2
Source0: http://prdownloads.sourceforge.net/ucon64/%{name}-%{version}-src.tar.bz2
Source1: http://prdownloads.sourceforge.net/ucon64/uf-FOX-1.1-src.tgz
Patch0: uf-FOX-1.1-libfox1.7.patch
BuildRequires: libusb-devel
BuildRequires: zlib-devel
BuildRequires: perl
BuildRoot: %{_tmppath}/%{name}-root

%package -n %{name}-gui
Summary: GUI for Ucon64, a console ROM backup tool
Group: Emulators
BuildRequires: fox1.7-devel
Requires: %{name}

%description
uCON64 is a console ROM backup tool.

%description -n %{name}-gui
GUI for Ucon64, a console ROM backup tool

%prep
#setup -q -n %{name}-%{version}-%{subversion}-src
%setup -q -n %{name}-%{version}-src -a 1
%patch0 -p0

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
rm -rf %{buildroot}
# don't use %%makeinstall here
install -d %{buildroot}%{_bindir}
install -m 755 src/%{name} %{buildroot}%{_bindir}

#install gui
install -m 755 uf-FOX-1.1-src/uf %{buildroot}%{_bindir}
chmod 644 uf-FOX-1.1-src/README.txt
#note : add a icon & menu entry

%files
%defattr(-,root,root)
%doc FILE_ID.DIZ VERSION *.html
%{_bindir}/ucon64

%files -n %{name}-gui
%defattr(-,root,root)
%doc uf-FOX-1.1-src/README.txt uf-FOX-1.1-src/gpl.txt
%{_bindir}/uf

%clean
rm -rf %{buildroot}

