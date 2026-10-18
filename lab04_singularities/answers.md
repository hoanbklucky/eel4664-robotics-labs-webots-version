# Lab 4 Answers

## Cartesian path controller solution

```python
desired_twist = feedforward_twist + gain * pose_error
return np.linalg.solve(J, desired_twist)
```

The feedforward term requests motion along the supplied path, while the proportional error term corrects tracking lag and drift. Solving the Jacobian equation converts that Cartesian command into the undamped joint-rate request whose growth students observe near singularities.

## Expected observations

Trial 1 moves away from the straight-elbow singularity and maintains moderate joint rates over the 20 cm path.

Trial 2 approaches and slightly crosses the straight-elbow configuration, finishing about 1 degree from straight on the other elbow branch. As the elbow straightens, the minimum singular value decreases, the condition number increases, and the undamped joint-rate curve rises sharply. Its checkpoint occurs at condition number 200.

Trial 3 begins in a different well-conditioned pose and crosses a shoulder-singular region without pausing. The elbow remains bent and wrist joint 2 remains away from zero, while the wrist-center radius decreases from about 15 cm during the first half of the path and increases again during the second half. Joint 1 must rotate increasingly fast near the middle, and the display marks condition number 500 while motion continues. Exact constant-speed tracking at the singular configuration would require an unbounded joint rate, so the limited robot briefly lags before catching up beyond it.

The jerk during the crossing is an expected consequence of the 3.00 rad/s limit. The undamped inverse requests a much larger joint command, Webots clips it, and the stylus temporarily lags even though the requested Cartesian path remains smooth.

The shoulder singularity connects two valid inverse-kinematic branches. A run with little net shoulder rotation and a run with a large rotation can therefore reach the same Cartesian path using different joint configurations. The supplied controller adds a consistent component along the Jacobian's weak joint-space direction after condition number 500 so the large-rotation branch is selected reproducibly; near singularity, this large joint motion causes very little Cartesian motion.

The generated SVG should show a moderate green Trial 1 curve, a sharply rising red Trial 2 elbow-singularity curve, and a purple Trial 3 curve that rises near the middle and falls after crossing the shoulder-singular region.

## Singularity question

Near a singularity, the robot has very little leverage in at least one Cartesian direction: moving the joints produces almost no tool motion in that direction. The inverse Jacobian must therefore request a large joint motion to produce even a small Cartesian motion. For example, the requested stylus speed stayed small and constant in Trial 2, but the joint-rate request rose sharply as the elbow became nearly straight.
