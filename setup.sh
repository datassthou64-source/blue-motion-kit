#!/usr/bin/env bash
# One-time setup for the Blue Motion kit. Safe to re-run: it only installs what is missing.
#   bash setup.sh            install + verify
#   bash setup.sh --check    verify only, install nothing
set -uo pipefail

kit="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
check_only=0; [[ "${1:-}" == "--check" ]] && check_only=1
missing=()
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; missing+=("$1"); }
note() { printf '  · %s\n' "$1"; }

echo "Blue Motion kit — setup"
echo "kit: $kit"
echo

# --- 1. System tools -------------------------------------------------------
os="$(uname -s)"
brew_install() {
  [[ $check_only == 1 ]] && return 1
  if [[ "$os" == "Darwin" ]] && command -v brew >/dev/null; then
    echo "  installing $1 with Homebrew…"; brew install "$1" >/dev/null && return 0
  fi
  return 1
}
if [[ "$os" == "Darwin" ]] && ! command -v brew >/dev/null; then
  note "Homebrew not found — install it from https://brew.sh, then re-run this script."
fi

need_tool() { # command, brew formula, label
  if command -v "$1" >/dev/null || brew_install "$2"; then
    command -v "$1" >/dev/null && ok "$3" || bad "$3 (install: brew install $2)"
  else
    bad "$3 (install: brew install $2)"
  fi
}
need_tool node node "Node.js"
need_tool ffmpeg ffmpeg "FFmpeg + FFprobe"
need_tool whisper-cli whisper-cpp "whisper-cpp (transcription)"
need_tool git git "git"

if command -v node >/dev/null; then
  major="$(node -p 'process.versions.node.split(".")[0]')"
  [[ "$major" -ge 20 ]] && ok "Node $major (≥ 20)" || bad "Node $major is too old — need 20+"
fi

if command -v python3 >/dev/null; then
  ok "Python 3"
  if python3 -c 'import numpy' 2>/dev/null; then ok "numpy (HDR footage fix)"
  elif [[ $check_only == 0 ]] && python3 -m pip install --user --quiet numpy 2>/dev/null; then ok "numpy (installed)"
  else note "numpy missing — only needed if a project uses iPhone HDR footage (pip3 install numpy)"; fi
else
  bad "Python 3"
fi

# Faster, more accurate transcription on Apple Silicon. Optional.
if [[ "$os" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
  command -v parakeet-mlx >/dev/null && ok "parakeet-mlx (fast transcription)" \
    || note "optional: pip3 install parakeet-mlx for faster, more accurate transcription"
fi

# --- 2. HyperFrames CLI, Chrome, and agent skills --------------------------
echo
pin="$(grep -o 'hyperframes@[0-9.]*' "$kit/library/starter/package.json" | head -1)"
if command -v npx >/dev/null; then
  if npx --yes "$pin" --version >/dev/null 2>&1; then ok "HyperFrames CLI ($pin, pinned by the starter)"; else bad "HyperFrames CLI ($pin)"; fi
  if [[ $check_only == 0 ]]; then npx --yes "$pin" browser ensure >/dev/null 2>&1; fi
  npx --yes "$pin" browser path >/dev/null 2>&1 && ok "Chrome for rendering" || bad "Chrome for rendering (npx $pin browser ensure)"

  # The HyperFrames agent skills (hyperframes, -core, -cli, -animation, -creative, media-use,
  # motion-graphics, general-video). Installed globally for Claude Code and Codex.
  if [[ $check_only == 0 ]]; then
    echo "  installing/updating HyperFrames agent skills…"
    npx --yes hyperframes@latest skills update general-video motion-graphics media-use >/dev/null 2>&1 \
      || npx --yes skills add heygen-com/hyperframes --all -g -y >/dev/null 2>&1
  fi
  skills_out="$(npx --yes hyperframes@latest skills check 2>&1 | sed 's/\x1b\[[0-9;]*m//g')"
  if grep -qi "missing\|not installed\|incomplete" <<<"$skills_out" || ! grep -q "current" <<<"$skills_out"; then
    bad "HyperFrames agent skills (npx hyperframes@latest skills update general-video motion-graphics media-use)"
  elif grep -qi "outdated:" <<<"$skills_out"; then
    ok "HyperFrames agent skills (some outdated — bash setup.sh updates them)"
  else
    ok "HyperFrames agent skills"
  fi
fi

# --- 3. Kit wiring ----------------------------------------------------------
echo
[[ -L "$kit/AGENTS.md" ]] && ok "AGENTS.md → CLAUDE.md (Codex)" || bad "AGENTS.md symlink"
[[ -L "$kit/.agents/skills" ]] && ok ".agents/skills → .claude/skills (Codex)" || bad ".agents/skills symlink"
[[ -f "$kit/library/assets/blue-gradient-loop.mp4" ]] && ok "blue gradient loop" || bad "library/assets/blue-gradient-loop.mp4"
mkdir -p "$kit/projects" "$kit/inbox"
chmod +x "$kit"/.claude/skills/blue-motion/scripts/* 2>/dev/null

# --- 4. Smoke test: scaffold a throwaway project and run check --------------
if [[ $check_only == 0 && ${#missing[@]} -eq 0 ]]; then
  echo
  echo "  smoke test: scaffold + hyperframes check…"
  tmp="$(mktemp -d)/smoke"
  ffmpeg -v error -f lavfi -i sine=frequency=440:duration=3 "$tmp.wav" \
    && bash "$kit/.claude/skills/blue-motion/scripts/bootstrap-project.sh" "$tmp" "$tmp.wav" >/dev/null \
    && (cd "$tmp" && npx --yes "$pin" check >/dev/null 2>&1) \
    && ok "starter project scaffolds and passes check" || bad "smoke test (scaffold + check) failed — see $tmp"
fi

echo
if [[ ${#missing[@]} -eq 0 ]]; then
  echo "Ready. Open this folder in Claude Code (claude) or Codex and give it an audio file."
else
  echo "Not ready — fix these, then re-run bash setup.sh:"
  printf '  - %s\n' "${missing[@]}"
  exit 1
fi
