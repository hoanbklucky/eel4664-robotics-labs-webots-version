# Lab 2 Answers

## Step 2 - Quick Diagnostics

Record whether `diagnostic_minimal` and `diagnostic_devices` passed. List any missing required device.

## Step 3 - One-Joint Motion and Alignment Data

- Final measured `q_align` [rad]:
- Measured tool position [m]:
- Measured tool `[roll, pitch, yaw]` [rad]:
- Measured tool-test-point position [m]:

## Step 5 - FK Convention and Offline Test

State the joint order, the two modified-DH matrix entries you completed, the multiplication order, and the frame meanings. Include the zero and nonsymmetric FK test output, rotation orthogonality error, and determinant.

## Step 6 - Fixed Tool Transform

Record the one 4-by-4 `T_6_tool` calculated from the Step 3 alignment data. Explain what it maps and why it must remain fixed.

## Steps 7-8 - FK Prediction Challenge

Before running Webots, record the commanded-angle tool-position prediction for Poses A-C and your qualitative prediction of the motion along A -> B -> C -> A.

After the run, complete one table with the alignment pose and held-out Poses A-C. Include measured `q`, predicted/measured tool position, position error, and orientation error. Clearly mark the alignment row and do not include it in held-out statistics.

For Pose C, include the predicted and measured world position of `p_tool = [0, 0.13, 0]` m and its Euclidean error.

State whether the air-drawn segments appeared straight or curved, and explain the observation using joint-space interpolation.

## Quantitative Summary

Report mean/maximum position error, mean/maximum orientation error, the required error plot, and a short interpretation of the residuals.

## Engineering Questions

Answer the five Engineering Questions in the Lab 2 README.
