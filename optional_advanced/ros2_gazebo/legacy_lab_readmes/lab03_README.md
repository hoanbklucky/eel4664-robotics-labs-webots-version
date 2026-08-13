# Lab 03 — Homogeneous Transformations

## Learning objectives

Implement rigid-body transformations directly in NumPy and verify them using ROS TF2.

## Part 1 — Complete the functions

Implement `rotx`, `roty`, `rotz`, `homogeneous`, and `invert_transform` in `src/transforms.py`.

Run:

```bash
cd lab03_homogeneous_transforms/src
python3 test_transforms.py
```

## Part 2 — Composition

Construct:

```text
A_T_B: translation 0.40 m along x and +30° rotation about z
B_T_C: translation 0.20 m along x and -20° rotation about y
```

Compute `A_T_C` and transform `p_C=[0.10,0.05,0,1]^T` into A.

## Part 3 — Order matters

Compare translation-then-rotation with rotation-then-translation and explain the difference.

## Part 4 — Connect to UR5e


## Launch the simulator

Terminal 1:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

Leave this terminal running. Use a second terminal for commands and your code.


Query one adjacent UR5e transform with TF2, reconstruct its 4×4 matrix, and verify `T @ inv(T) ≈ I`.

## Questions

1. Why are homogeneous coordinates useful?
2. Why does multiplication order matter?
3. What properties must a rotation matrix satisfy?
4. Derive the inverse rigid transform without `np.linalg.inv`.
