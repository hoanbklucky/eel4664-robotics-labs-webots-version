# Lab 4 Answers

## Expected observations

Trial 1 has a substantially larger minimum singular value, a lower condition number, moderate joint rates, and a measured tool displacement close to the requested 6 cm.

Trials 2 and 3 start from the same almost straight-elbow pose. Their minimum singular value is much smaller and their condition number is much larger. In Trial 2, the raw undamped inverse requests roughly 6 rad/s in joint-rate-vector norm and is uniformly rate-limited before execution. In Trial 3, damping produces a much smaller joint command without requiring the safety limiter, but the tool still completes only a small part of the Cartesian request.

## Question 1

The configuration used in Trials 2 and 3 is closer to a singularity. Its minimum singular value is near zero and its condition number is much larger, showing that the Jacobian is nearly rank deficient.

## Question 2

The raw undamped inverse divides by the Jacobian's very small singular value. This amplifies a modest Cartesian request into large, opposing joint rates even though the requested translation is only 6 cm.

## Question 3

Trial 2 retains the undamped inverse direction but uniformly scales it to satisfy the rate limit, so the joints still move much more than in Trial 3. Damping changes the inverse calculation itself, producing smaller joint motion while accepting a large Cartesian tracking error.

## Question 4

The raw Trial 2 command includes a peak joint rate of roughly 5 rad/s and would create a large configuration change during the two-second test. Rate limiting makes the comparison controlled and repeatable while still exposing the excessive command numerically and preserving its joint-space direction.
