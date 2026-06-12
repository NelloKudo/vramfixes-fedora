%define debug_package %{nil}

Name:           kcgroups-dmemcg
Version:        %{pkg_version}
Release:        2%{?dist}
Summary:        KDE cgroups library - dmem cgroup fork
License:        LGPL-2.1-or-later
URL:            https://github.com/pixelcluster/kcgroups
Source0:        kcgroups-dmemcg.tar.gz
Source1:        plasma-foreground-booster.tar.gz

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  qt6-qtbase-devel
BuildRequires:  kf6-kwindowsystem-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-kdbusaddons-devel
BuildRequires:  plasma-workspace-devel
BuildRequires:  kf6-kitemmodels-devel

%description
KDE library to manipulate cgroups, fork adding dmem cgroup support.

%package -n plasma-foreground-booster-dmemcg
Summary:        Plasma foreground booster - dmem cgroup fork
Requires:       %{name} = %{version}-%{release}

%description -n plasma-foreground-booster-dmemcg
Plasma plugin to boost foreground apps using cgroups.

%prep
%setup -q -n kcgroups-dmemcg -a 1

%build
mkdir -p kcgroups-build kcgroups-install plasma-booster-build

cmake -S . -B kcgroups-build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_WITH_QT6=ON
%make_build -C kcgroups-build
make -C kcgroups-build DESTDIR="$(pwd)/kcgroups-install" install

CMAKE_PREFIX_PATH="$(pwd)/kcgroups-install%{_prefix}" \
cmake -S plasma-foreground-booster -B plasma-booster-build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_SKIP_INSTALL_RPATH=ON
%make_build -C plasma-booster-build

%install
find %{buildroot} ! -type d 2>/dev/null | sed "s|%{buildroot}||" | sort > %{_builddir}/kcgroups-files.txt
%make_install -C kcgroups-build
find %{buildroot} ! -type d | sed "s|%{buildroot}||" | sort | \
    comm -13 %{_builddir}/kcgroups-files.txt - > %{_builddir}/kcgroups-new-files.txt

%make_install -C plasma-booster-build
find %{buildroot} ! -type d | sed "s|%{buildroot}||" | sort | \
    comm -13 %{_builddir}/kcgroups-new-files.txt - > %{_builddir}/booster-files.txt

%files -f %{_builddir}/kcgroups-new-files.txt
%license LICENSES/

%files -n plasma-foreground-booster-dmemcg -f %{_builddir}/booster-files.txt

%changelog
* Sat Jun 13 2026 NelloKudo <marshnelloosu@gmail.com> - 0.1-2
- initial package
