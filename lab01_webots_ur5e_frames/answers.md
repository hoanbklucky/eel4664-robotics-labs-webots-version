# Lab 1 Answers

## Step 2 - Quick Diagnostics

Record whether `diagnostic_minimal` and `diagnostic_devices` passed. List any missing required device.

## Step 3 - One-Joint Motion and Alignment Data

- Predicted moving links and direction:
- Actual result:
- Final measured `q_align` [rad]:
- Measured tool position [m]:
- Measured tool `[roll, pitch, yaw]` [rad]:
- Measured tool-test-point position [m]:

## Step 4 - Transform-Code Understanding

Predict and then verify:

| Expression | Prediction | Program result | Explanation |
|---|---|---|---|
| `rotz(pi/2) @ [1, 0, 0]` | | | |
| point `[0.1, 0.2, 0.3]` under translation `[1, 2, 3]` | | | |
| direction `[1, 0, 0]` under the same translation | | | |

Explain why inverse translation is `-R.T @ p` and why points and directions use different homogeneous coordinates.

## Step 5 - FK Convention and Offline Test

State the joint order, standard-DH definition of `A_i`, multiplication order, and frame meanings. Include the zero and nonsymmetric FK test output, rotation orthogonality error, and determinant.

## Step 6 - Fixed Tool Transform

Record the one 4-by-4 `T_6_tool` calculated from the Step 3 alignment data. Explain what it maps and why it must remain fixed.

## Steps 7-8 - Held-Out Robot Results

Complete one table with the alignment pose and held-out Poses A-C. Include measured `q`, predicted/measured tool position, position error, and orientation error. Clearly mark the alignment row and do not include it in held-out statistics.

For Pose C, include the predicted and measured world position of `p_tool = [0.05, 0, 0]` m and its Euclidean error.

## Quantitative Summary

Report mean/maximum position error, mean/maximum orientation error, the required error plot, and a short interpretation of the residuals.

## Engineering Questions

Answer the six Engineering Questions in the Lab 1 README.
