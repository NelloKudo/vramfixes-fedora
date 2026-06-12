#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOPDIR=$(rpm --eval '%{_topdir}')

BOOSTER_VER=$(sed -n 's/^version = "\([^"]*\)"/\1/p' "$SCRIPT_DIR/dmemcg-booster/Cargo.toml" | head -1)
KCGROUPS_VER=$(sed -n 's/^set(KF5_VERSION "\([^"]*\)").*/\1/p' "$SCRIPT_DIR/kcgroups/CMakeLists.txt" | head -1)

echo "dmemcg-booster version: $BOOSTER_VER"
echo "kcgroups version: $KCGROUPS_VER"

mkdir -p "$TOPDIR"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

echo "creating kcgroups-dmemcg tarball..."
git -C "$SCRIPT_DIR/kcgroups" archive --prefix=kcgroups-dmemcg/ kcgroups-dmemcg-experimental \
    | gzip > "$TOPDIR/SOURCES/kcgroups-dmemcg.tar.gz"

echo "creating plasma-foreground-booster tarball..."
git -C "$SCRIPT_DIR/kcgroups" archive --prefix=plasma-foreground-booster/ booster-dmemcg-experimental \
    | gzip > "$TOPDIR/SOURCES/plasma-foreground-booster.tar.gz"

echo "creating dmemcg-booster tarball..."
git -C "$SCRIPT_DIR/dmemcg-booster" archive --prefix=dmemcg-booster-$BOOSTER_VER/ HEAD \
    | gzip > "$TOPDIR/SOURCES/dmemcg-booster-$BOOSTER_VER.tar.gz"

echo "creating rust vendor tarball..."
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT
tar -xzf "$TOPDIR/SOURCES/dmemcg-booster-$BOOSTER_VER.tar.gz" -C "$TMPDIR"
pushd "$TMPDIR/dmemcg-booster-$BOOSTER_VER" > /dev/null
cargo vendor vendor --locked
tar -czf "$TOPDIR/SOURCES/dmemcg-booster-$BOOSTER_VER-vendor.tar.gz" vendor/
popd > /dev/null

cp "$SCRIPT_DIR/specs/kcgroups-dmemcg.spec" "$TOPDIR/SPECS/"
cp "$SCRIPT_DIR/specs/dmemcg-booster.spec" "$TOPDIR/SPECS/"

echo "building kcgroups-dmemcg..."
rpmbuild -ba --define "pkg_version $KCGROUPS_VER" "$TOPDIR/SPECS/kcgroups-dmemcg.spec"

echo "building dmemcg-booster..."
rpmbuild -ba --define "pkg_version $BOOSTER_VER" "$TOPDIR/SPECS/dmemcg-booster.spec"

echo "done. rpms are in $TOPDIR/RPMS/"
find "$TOPDIR/RPMS" -name "*.rpm" | sort
