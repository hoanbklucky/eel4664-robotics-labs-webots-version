#!/usr/bin/env bash
set -u
pass() { printf '[PASS] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1"; }
info() { printf '[INFO] %s\n' "$1"; }

command -v ros2 >/dev/null 2>&1 && pass 'ros2 command found' || fail 'ros2 command not found'
command -v gz >/dev/null 2>&1 && pass 'gz command found' || fail 'gz command not found'
command -v colcon >/dev/null 2>&1 && pass 'colcon command found' || fail 'colcon command not found'
python3 -c 'import numpy' >/dev/null 2>&1 && pass 'Python NumPy available' || fail 'Python NumPy missing'

if command -v ros2 >/dev/null 2>&1; then
  ros2 pkg list 2>/dev/null | grep -q '^ur_simulation_gz$' && pass 'ur_simulation_gz package found' || fail 'ur_simulation_gz package not found; source the workspace'
  ros2 pkg list 2>/dev/null | grep -q '^tf2_ros$' && pass 'tf2_ros package found' || fail 'tf2_ros missing'
fi

info 'If Gazebo is already running, also check:'
echo '  ros2 control list_controllers'
echo '  ros2 action list'
