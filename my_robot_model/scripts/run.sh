#!/usr/bin/env bash
set -e
source /opt/ros/jazzy/setup.bash
pkg_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ws_dir="$(cd "$pkg_dir/../.." && pwd)"
if [ "$(basename "$(dirname "$pkg_dir")")" != "src" ]; then
  echo "Place my_robot_model inside <workspace>/src first." >&2
  exit 1
fi
cd "$ws_dir"
colcon build --symlink-install --packages-select my_robot_model
source install/setup.bash
ros2 launch my_robot_model robot.launch.py "$@"
