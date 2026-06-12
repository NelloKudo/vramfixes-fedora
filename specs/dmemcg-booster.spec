%define debug_package %{nil}

Name:           dmemcg-booster
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Service for dmem cgroup limits for boosting foreground games
License:        MIT
URL:            https://gitlab.steamos.cloud/holo/dmemcg-booster
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  dbus-devel
BuildRequires:  pkg-config
BuildRequires:  systemd-rpm-macros

Requires:       dbus-libs

%description
Service for enabling and controlling dmem cgroup limits for boosting foreground games.

%prep
%setup -q
%setup -q -T -D -a 1
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --frozen --release

%install
install -Dm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 dmemcg-booster-system.service \
    %{buildroot}%{_unitdir}/dmemcg-booster-system.service
install -Dm644 dmemcg-booster-user.service \
    %{buildroot}%{_userunitdir}/dmemcg-booster-user.service

%post
%systemd_post dmemcg-booster-system.service

%preun
%systemd_preun dmemcg-booster-system.service

%postun
%systemd_postun_with_restart dmemcg-booster-system.service

%files
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/dmemcg-booster-system.service
%{_userunitdir}/dmemcg-booster-user.service

%changelog
* Sat Jun 13 2026 NelloKudo <marshnelloosu@gmail.com> - 0.1.2-1
- initial package
