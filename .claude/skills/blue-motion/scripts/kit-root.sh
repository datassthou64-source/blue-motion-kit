#!/usr/bin/env bash
# Print the blue-motion repo root (KIT), resolving any symlink to this skill.
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
cd "$script_dir/../../../.." && pwd -P
