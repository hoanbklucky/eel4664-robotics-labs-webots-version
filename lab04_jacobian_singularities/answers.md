# Lab 4 Answers

## Expected observations

Both trials start from the same bent, well-conditioned pose. Trial 1 moves away from the straight-elbow singularity and maintains moderate joint rates over the 20 cm path.

Trial 2 reverses direction and approaches the straight-elbow workspace boundary. As the elbow straightens, the minimum singular value decreases, the condition number increases, and the undamped joint-rate curve rises sharply toward the 3.00 rad/s simulation limit.

The automatic checkpoint occurs when the condition number first reaches 200. It freezes the scene close to the singularity and prominently displays the raw requested peak joint rate and the applied peak joint rate. The generated SVG should show a moderate green Trial 1 curve and a sharply rising red Trial 2 curve.

## Question 1

During Trial 2, the minimum singular value decreases toward zero while the condition number grows from a moderate value to 200 and beyond. The nearly straight elbow makes the Jacobian poorly conditioned and the inverse highly sensitive.

## Question 2

The Cartesian speed remains constant, but the undamped inverse effectively divides the weak-direction component by a singular value that is approaching zero. Consequently, the required joint rates grow rapidly as the elbow straightens.

Equivalently, if neighboring Cartesian via points are scheduled `dt` seconds apart, the physical rate is approximately `(q_(k+1) - q_k) / dt`. Near the singularity, a small Cartesian increment requires a large joint increment, so using more IK iterations or more via points does not eliminate the large rate. The trajectory must instead slow down near the boundary.

## Question 3

Near the end of Trial 2, the raw undamped command grows rapidly and would become unbounded in the lost motion direction at the exact singularity. The 3.00 rad/s simulation limit keeps the command below the Webots model's 3.14 rad/s joint limit while preserving a clearly visible rapid joint motion. This setting is for the simulation demonstration and is not a recommended hardware limit.
