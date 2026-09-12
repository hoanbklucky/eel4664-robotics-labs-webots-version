# Lab 2 Answers

## Step 2 - Diagnostics

- `diagnostic_minimal`:
- `diagnostic_devices`:
- Missing required devices, if any:

## Step 4 - Modified-DH Entries and Offline Tests

- `row_2_column_1 =`
- `row_3_column_4 =`

### Zero configuration

Paste the 4-by-4 FK matrix, orthogonality error, and determinant:

```text

```

### Nonsymmetric configuration

Paste the 4-by-4 FK matrix, orthogonality error, and determinant:

```text

```

## Step 5 - Predictions Before Webots

Record these outputs from `predict_fk_poses.py` before running `fk_experiment`.

| Pose | Predicted tool position [m] | Predicted tool RPY [rad] |
|---|---|---|
| A | | |
| B | | |
| C | | |

## Step 6 - Webots Motion and FK Comparison

### Joint tracking check

| Pose | Target $\mathbf q_{goal}$ [rad] | Measured $\mathbf q$ [rad] | Maximum joint error [rad] |
|---|---|---|---:|
| A | `[0.0, -1.20, 1.20, -1.50, -1.57, 0.0]` | | |
| B | `[0.20, -0.80, 1.00, -1.10, -0.70, 0.30]` | | |
| C | `[-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]` | | |

### Tool-pose comparison

| Pose | FK position [m] | Webots position [m] | Position error [mm] | FK RPY [rad] | Webots RPY [rad] | Orientation error [deg] |
|---|---|---|---:|---|---|---:|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |

- Mean position error [mm]:
- Maximum position error [mm]:
- Mean orientation error [deg]:
- Maximum orientation error [deg]:

Interpret the tracking and tool-pose errors in two or three sentences: