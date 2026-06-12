# vramfixes-fedora

Repository to package [Valve AMDGPU VRAM fixes](https://pixelcluster.github.io/VRAM-Mgmt-fixed/) for Fedora-based systems.

## download

You can grab the .rpm files built from GitHub Actions in [releases](https://github.com/NelloKudo/vramfixes-fedora/releases).

## packages

- **kcgroups-dmemcg** + **plasma-foreground-booster-dmemcg**
- **dmemcg-booster**

## dependencies

```
cmake extra-cmake-modules qt6-qtbase-devel
kf6-kwindowsystem-devel kf6-kconfig-devel kf6-kdbusaddons-devel kf6-kitemmodels-devel
plasma-workspace-devel cargo rust dbus-devel
```

## building locally

```sh
git clone --recurse-submodules https://github.com/NelloKudo/vramfixes-fedora
cd vramfixes-fedora
./build-rpms.sh
```

RPMs end up in `~/rpmbuild/RPMS/`.
