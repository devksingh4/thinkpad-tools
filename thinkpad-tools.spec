%define name thinkpad-tools
%define version 0.10.1
%define unmangled_version 0.10.1
%define unmangled_version 0.10.1
%define release 1

Summary: Tools for ThinkPads
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Dev Singh <dev@singhk.dev>

%description
Tools created to manage thinkpad properties such as TrackPoint, Undervolt, and Battery

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
/usr/bin/python3 setup.py build

%install
/usr/bin/python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
