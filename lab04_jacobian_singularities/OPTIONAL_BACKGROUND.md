# Lab 4 Optional Background

This page explains the ideas behind differential kinematics and singularities before the detailed implementation. Read Sections 1 through 6 for the core concepts. The remaining sections help interpret the numerical experiment.

Return to the [Lab 4 instructions](README.md) when you are ready to complete the required activity.

## 1. The Jacobian is a local motion map

Forward kinematics maps joint angles to a tool pose:

$$
\mathbf x=f(\mathbf q).
$$

Near the current configuration, a small joint change produces an approximately linear tool-pose change:

$$
\Delta\mathbf x\approx J(\mathbf q)\Delta\mathbf q.
$$

Dividing by a small time interval gives the velocity form:

$$
\begin{bmatrix}\mathbf v\\\boldsymbol\omega\end{bmatrix}
=J(\mathbf q)\dot{\mathbf q}.
$$

The Jacobian plays the role of a multivariable derivative. It is local: after the robot moves, the Jacobian must be recalculated at the new configuration.

## 2. Why one revolute-joint column contains a cross product

For revolute joint $i$, let $\mathbf z_i$ be its axis direction, $\mathbf p_i$ a point on the axis, and $\mathbf p_e$ the endpoint position, all expressed in the base frame.

A small positive joint rotation produces tangential endpoint velocity:

$$
\mathbf v_i=\mathbf z_i\times(\mathbf p_e-\mathbf p_i)\dot q_i.
$$

The same joint produces angular velocity along its axis:

$$
\boldsymbol\omega_i=\mathbf z_i\dot q_i.
$$

Therefore,

$$
J_i=
\begin{bmatrix}
\mathbf z_i\times(\mathbf p_e-\mathbf p_i)\\
\mathbf z_i
\end{bmatrix}.
$$

Each column answers: “If only this joint moves at one radian per second, what instantaneous linear and angular tool velocity results?”

## 3. A singularity is a lost motion direction

Away from a singularity, the robot can create small tool motion in every task direction represented by the Jacobian. At a singularity, the Jacobian loses rank. At least one desired Cartesian direction can no longer be produced instantaneously, regardless of how the joints are combined.

This is a geometric limitation, not merely a failed matrix calculation. Near a singularity, the direction may still be approximated, but doing so can require impractically large joint rates.

## 4. SVD reveals strong and weak directions

The singular value decomposition is

$$
J=U\Sigma V^T.
$$

The columns of $V$ describe joint-velocity directions. The columns of $U$ describe corresponding tool-twist directions. The singular values describe how strongly each joint direction produces its associated tool motion:

$$
J\mathbf v_i=\sigma_i\mathbf u_i.
$$

A large $\sigma_i$ means the robot produces that tool direction efficiently. A small $\sigma_i$ identifies weak motion capability. Thus:

- $\sigma_{\min}$ measures the weakest local motion direction;
- $\mathbf u_{\min}$ identifies the degraded tool-twist direction; and
- $\mathbf v_{\min}$ identifies the associated joint-motion combination.

At an exact singularity, $\sigma_{\min}=0$.

## 5. Why the pseudoinverse can request extreme joint rates

A common inverse differential solution is

$$
\dot{\mathbf q}=J^+\mathbf v_d.
$$

In SVD form, the pseudoinverse divides by each nonzero singular value. A requested component aligned with $\mathbf u_{\min}$ is amplified approximately by $1/\sigma_{\min}$. As $\sigma_{\min}$ approaches zero, the requested joint-rate norm can become very large.

## 6. Damped least squares limits amplification

Damped least squares uses

$$
\dot{\mathbf q}
=J^T\left(JJ^T+\lambda^2I\right)^{-1}\mathbf v_d.
$$

The damping parameter $\lambda$ prevents division by a nearly zero singular value. Small damping preserves accuracy when the robot is well conditioned. Larger damping bounds joint-rate amplification near a singularity but accepts Cartesian tracking error.

Damping does not remove the singularity or restore the lost physical motion direction.

## 7. Metrics describe different aspects of conditioning

Common metrics include

$$
\kappa(J)=\frac{\sigma_{\max}}{\sigma_{\min}}
$$

and Yoshikawa manipulability

$$
w=\sqrt{\det(JJ^T)}=\prod_i\sigma_i.
$$

Near a singularity, $\sigma_{\min}$ and $w$ approach zero, while the condition number grows. Rank depends on a numerical tolerance, so report the tolerance used. A determinant alone does not identify the lost direction and is not defined for a nonsquare Jacobian.

## 8. Translation and rotation use different units

A 6D geometric Jacobian contains translational rows and rotational rows. Changing meters to millimeters changes raw singular values and condition number even though the physical robot is unchanged.

Use the stated SI-unit convention consistently in this lab. For more general comparisons, report a characteristic length or analyze position and orientation blocks separately. Never compare conditioning values produced with different unit scalings.

## 9. Verify before interpreting a singularity

A centered finite difference estimates each column:

$$
J[:,i]\approx
\frac{\operatorname{poseDifference}(T(\mathbf q-\varepsilon\mathbf e_i),
T(\mathbf q+\varepsilon\mathbf e_i))}
{2\varepsilon}.
$$

Both Jacobians must use the same endpoint and frame. A frame, sign, or endpoint mismatch creates error broadly. A real singularity instead appears with analytical/numerical agreement, a small singular value, and amplified inverse motion.

```text
verify FK
    -> verify one Jacobian column
    -> verify all columns
    -> inspect singular values
    -> command a very small differential motion
    -> approach the singularity conservatively
```
