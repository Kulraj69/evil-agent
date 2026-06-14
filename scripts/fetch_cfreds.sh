#!/usr/bin/env bash
#
# fetch_cfreds.sh - Download + verify the NIST CFReDS Data Leakage PC image and
# prepare it for FIND EVIL! on the SIFT Workstation.
#
# Run this ON THE SIFT WORKSTATION (it uses ewfmount/ewf-tools). It:
#   1. Downloads the 3-part 7z PC image from the CFReDS archive
#   2. Verifies each part against NIST's published SHA1
#   3. Extracts the .E01 set
#   4. Mounts the E01 read-only via ewfmount and exposes a raw device path
#
# Output: prints the raw image path to pass to run_real_sift.py --disk
#
# Usage:
#   bash scripts/fetch_cfreds.sh [/path/to/evidence_dir]
#
set -euo pipefail

EVID="${1:-/evidence/cfreds}"
BASE="https://cfreds-archive.nist.gov/data_leakage_case/files"   # archive file path
mkdir -p "$EVID"
cd "$EVID"

# NIST-published SHA1 hashes (from the CFReDS hash_values.html page)
declare -A SHA1=(
  ["cfreds_2015_data_leakage_pc.7z.001"]="F07632FAA66A47088DEB07BDB45CC568E4BF650B"
  ["cfreds_2015_data_leakage_pc.7z.002"]="5DEE46ABF6FA833268E5AE199A13854CCF42689B"
  ["cfreds_2015_data_leakage_pc.7z.003"]="1687686F819092E05047F195F102D8FA0C38ED66"
)

echo "[*] Downloading CFReDS Data Leakage PC image (~5 GB) into $EVID ..."
echo "    If the URL 404s, download manually from:"
echo "    https://cfreds-archive.nist.gov/data_leakage_case/data-leakage-case.html"
for f in "${!SHA1[@]}"; do
  if [[ ! -f "$f" ]]; then
    wget -c "$BASE/$f" -O "$f" || {
      echo "[!] Auto-download failed for $f."
      echo "    Download it manually into $EVID and re-run this script."
      exit 1
    }
  fi
done

echo "[*] Verifying SHA1 integrity ..."
for f in "${!SHA1[@]}"; do
  got="$(sha1sum "$f" | awk '{print toupper($1)}')"
  want="${SHA1[$f]}"
  if [[ "$got" != "$want" ]]; then
    echo "[!] HASH MISMATCH for $f"
    echo "    expected $want"
    echo "    got      $got"
    exit 1
  fi
  echo "    OK  $f"
done

echo "[*] Extracting 7z parts ..."
7z x -y "cfreds_2015_data_leakage_pc.7z.001" >/dev/null

E01="$(ls "$EVID"/*.E01 2>/dev/null | head -n1 || true)"
if [[ -z "$E01" ]]; then
  echo "[!] No .E01 found after extraction. Check the archive contents."
  exit 1
fi
echo "    Extracted: $E01"

echo "[*] Mounting E01 read-only via ewfmount ..."
MNT="$EVID/ewf_mount"
mkdir -p "$MNT"
# ewfmount presents the raw image as $MNT/ewf1 (read-only by design)
if ! mountpoint -q "$MNT"; then
  ewfmount "$E01" "$MNT"
fi
RAW="$MNT/ewf1"

echo ""
echo "============================================================"
echo " READY. Raw read-only image: $RAW"
echo ""
echo " Run FIND EVIL! against it:"
echo "   python3 run_real_sift.py --live \\"
echo "       --disk '$RAW' \\"
echo "       --case CFREDS-LEAK"
echo "============================================================"
