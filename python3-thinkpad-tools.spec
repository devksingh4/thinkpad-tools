# Created by pyp2rpm-3.3.2
%global pypi_name thinkpad-tools

Name:           python-%{pypi_name}
Version:        0.11.2
Release:        1%{?dist}
Summary:        Tools for ThinkPads

License:        GPLv3
URL:            None
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
Tools created to manage thinkpad properties such as TrackPoint, Undervolt, and
Battery

%package -n     %{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n %{pypi_name}
Tools created to manage thinkpad properties such as TrackPoint, Undervolt, and
Battery


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files
%doc README.md
%{_bindir}/thinkpad-tools
%{python3_sitelib}/assets
%{python3_sitelib}/thinkpad_tools-%{version}-py?.?.egg-info
/etc/thinkpad-tools-persistence.sh
/lib/systemd/system/thinkpad-tools.service