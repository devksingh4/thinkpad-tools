%global pypi_name thinkpad-tools

Name:           python-%{pypi_name}
Version:        0.14
Release:        1%{?dist}
Summary:        Tools for ThinkPads

License:        GPLv3
URL:            https://github.com/devksingh4/thinkpad-tools
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
%if 0%{?rhel} < 8 || 0%{?fedora} <= 30
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%endif

%description
Tools created to manage thinkpad properties such as TrackPoint, Undervolt, and
Battery.

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
%license LICENSE
%{_bindir}/thinkpad-tools
%{python3_sitelib}/thinkpad_tools_assets
%{python3_sitelib}/thinkpad_tools-%{version}-py?.?.egg-info
%config(noreplace) /etc/thinkpad-tools.ini
/usr/lib/systemd/system/thinkpad-tools.service

%changelog
* Sun April 11 2021 Dev Singh <dev@devksingh.com> 0.14
- Add ability to read undervolt status
* Tue May 05 2020 Dev Singh <dev@singhk.dev> 0.13
- Implement true persistence with /etc/thinkpad-tools.ini
* Mon Apr 20 2020 Dev Singh <dev@singhk.dev> 0.12.2
- Fix error with the TrackPoint script
* Mon Apr 13 2020 Dev Singh <dev@singhk.dev> 0.12.1
- Comply with Fedora packaging guidelines
* Sun Apr 12 2020 Dev Singh <dev@singhk.dev> 0.12.0
- Patch documentation strings for persistence mode to show correct options
* Sat Apr 11 2020 Dev Singh <dev@singhk.dev> 0.11.0
- Initial RPM Release
