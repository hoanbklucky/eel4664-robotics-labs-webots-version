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

## Question 1

During Trial 2, the minimum singular value decreases toward zero while the condition number grows from a moderate value to 200 and beyond. The nearly straight elbow makes the Jacobian poorly conditioned and the inverse highly sensitive.

## Question 2

The Cartesian speed remains constant, but the undamped inverse effectively divides the weak-direction component by a singular value that is approaching zero. Consequently, the required joint rates grow rapidly as the elbow straightens.

Equivalently, if neighboring Cartesian via points are scheduled `dt` seconds apart, the physical rate is approximately `(q_(k+1) - q_k) / dt`. Near the singularity, a small Cartesian increment requires a large joint increment, so using more IK iterations or more via points does not eliminate the large rate. The trajectory must instead slow down near the boundary.

## Question 3

Trial 3 is a shoulder singularity because the elbow stays visibly bent while the wrist center approaches the vertical base-joint axis. The small wrist-center radius and rapidly increasing base-joint motion distinguish it from Trial 2's straight-elbow geometry and from a wrist singularity, where wrist joint 2 would approach zero.

## Question 4

Near either singularity, the raw undamped command can grow rapidly and would become unbounded in the lost motion direction at the exact singular configuration. The 3.00 rad/s simulation limit keeps the command below the Webots model's 3.14 rad/s joint limit while preserving clearly visible rapid joint motion. This setting is for the simulation demonstration and is not a recommended hardware limit.
