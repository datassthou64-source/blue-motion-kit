#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: bootstrap-project.sh OUTPUT_DIR AUDIO [AUDIO ...]" >&2
  exit 2
fi

target_dir="$1"
shift
kit_root="$(bash "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/kit-root.sh")"
template_root="$kit_root/library"

if [[ ! -d "$template_root/starter" || ! -f "$template_root/assets/blue-gradient-loop.mp4" ]]; then
  echo "Missing canonical template: $template_root" >&2
  exit 1
fi

if [[ -d "$target_dir" ]] && find "$target_dir" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
  echo "Refusing to overwrite non-empty directory: $target_dir" >&2
  exit 1
fi

mkdir -p "$target_dir/assets/logos" "$target_dir/compositions" "$target_dir/_scene-templates" "$target_dir/_pattern-library"
cp -R "$template_root/starter/." "$target_dir/"
cp "$template_root/assets/blue-gradient-loop.mp4" "$target_dir/assets/blue-gradient-loop.mp4"
cp -R "$template_root/assets/logos/." "$target_dir/assets/logos/"
cp -R "$template_root/scenes/." "$target_dir/_scene-templates/"
cp -R "$template_root/patterns/." "$target_dir/_pattern-library/"
cp -R "$template_root/.media" "$target_dir/.media"
find "$target_dir" -name .DS_Store -delete

project_name="$(basename "$target_dir")"
project_slug="$(printf '%s' "$project_name" | tr '[:upper:] _' '[:lower:]--' | tr -cd 'a-z0-9.-')"
perl -pi -e "s/blue-motion-starter/$project_slug/g" "$target_dir/package.json" "$target_dir/meta.json"

audio_index=1
for audio_source in "$@"; do
  if [[ ! -f "$audio_source" ]]; then
    echo "Missing audio: $audio_source" >&2
    exit 1
  fi
  extension="${audio_source##*.}"
  destination="$target_dir/assets/audio-$(printf '%02d' "$audio_index").$extension"
  cp "$audio_source" "$destination"
  duration="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$destination")"
  echo "audio-$(printf '%02d' "$audio_index").$extension  $duration seconds"
  audio_index=$((audio_index + 1))
done

echo "Created: $target_dir"
echo "Next: transcribe the copied audio, replace the placeholder timeline, then run npm run check."
echo "Preview: cd \"$target_dir\" && npm run dev"
