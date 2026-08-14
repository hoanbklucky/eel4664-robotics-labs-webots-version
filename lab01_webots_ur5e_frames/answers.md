# Lab 1 Answers

## Validation Checkpoints

Copy and complete the Step 10 table. Record the last passing stage before diagnosing a failure.

## Devices and Frames

Document the six-joint order, motor/sensor names, basic time step, frame sketch, standard-DH convention, T_world_0, and fixed T_6_tool.

## Transform-Code Reading

Complete the Step 11 prediction table. Explain the right-hand-rule sine signs, why a point uses homogeneous coordinate 1 while a direction uses 0, and why inverse translation is `-R.T @ p`. Compare each prediction with the program output.

## Offline Transform and FK Tests

Include the provided transformation-test output, the zero and nonsymmetric FK structural tests, rotation orthogonality error, and determinant.

## FK Alignment and Held-Out Validation

Identify the one alignment configuration. For Configurations 2-6, tabulate measured q, predicted/measured tool position, position error, and orientation error. Report aggregate held-out metrics.

## Motion and Repeatability

Record the one-joint prediction and results, both repeated multi-joint trials, command-versus-measurement metrics, and final-state repeatability.

## Tool-Point Transformation

State T_world_tool, p_tool = [0.05, 0, 0] m, rotation order, predicted world point, tool_test_point_position measurement, numerical error, and interpretation.

## Engineering Reflection

Answer every Engineering Question in the Lab 1 README and distinguish systematic from configuration-dependent FK residuals.
