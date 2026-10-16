# Lab 5 Optional Background

This page explains the main ideas behind trajectory generation and tracking. Read Sections 1 through 5 before the lab if you want a concepts-first introduction. Sections 6 through 10 provide additional detail and are useful when interpreting your plots.

Return to the [Lab 5 instructions](README.md) when you are ready to complete the required activity.

## 1. A path says where; a trajectory also says when

A **path** describes the geometric route taken by the robot. It does not specify how quickly the robot travels along that route.

A **trajectory** assigns a time to every point on the path. It specifies position and usually velocity and acceleration as functions of time:

$$
\mathbf q(t),\qquad \dot{\mathbf q}(t),\qquad \ddot{\mathbf q}(t).
$$

For one joint, imagine drawing a curve of angle versus time. The height of the curve is the joint angle, its slope is angular velocity, and the rate at which the slope changes is angular acceleration.

This distinction matters because two motions can follow the same path but use different durations. The slower motion usually requires smaller velocity and acceleration, even though its start and finish are unchanged.

## 2. From two endpoint angles to a smooth motion

Suppose one joint must move from angle $\theta_0$ at time $0$ to angle $\theta_f$ at time $T_f$. Jumping immediately from one angle command to the other would demand an unrealistically abrupt motion.

A cubic trajectory replaces that jump with a smooth polynomial:

$$
\theta(t)=a_0+a_1t+a_2t^2+a_3t^3.
$$

Differentiate once to obtain velocity:

$$
\dot{\theta}(t)=a_1+2a_2t+3a_3t^2.
$$

Differentiate again to obtain acceleration:

$$
\ddot{\theta}(t)=2a_2+6a_3t.
$$

There are four unknown coefficients, so we need four boundary conditions. A common rest-to-rest motion uses

$$
\theta(0)=\theta_0,\qquad
\theta(T_f)=\theta_f,\qquad
\dot{\theta}(0)=0,\qquad
\dot{\theta}(T_f)=0.
$$

Solving these four equations gives

$$
a_0=\theta_0,\qquad a_1=0,
$$

$$
a_2=\frac{3(\theta_f-\theta_0)}{T_f^2},\qquad
a_3=\frac{-2(\theta_f-\theta_0)}{T_f^3}.
$$

The boundary conditions are not extra checks added after the polynomial is generated. They are what determine the polynomial.

## 3. A normalized clock makes the formula easier to read

Define normalized time

$$
s=\frac{t}{T_f},\qquad 0\le s\le 1,
$$

and the total angle change

$$
\Delta\theta=\theta_f-\theta_0.
$$

The same cubic rest-to-rest trajectory becomes

$$
\theta(t)=\theta_0+\Delta\theta(3s^2-2s^3).
$$

The function $3s^2-2s^3$ starts at zero, ends at one, and has zero slope at both ends. It describes **progress along the path**. The endpoints determine where the robot goes, while $T_f$ determines how quickly it gets there.

For a move from $0^\circ$ to $90^\circ$ in $2$ seconds,

$$
\theta(t)=\frac{3\pi}{8}t^2-\frac{\pi}{8}t^3.
$$

At $t=1$ second, the motion is halfway through its duration and the joint reaches $45^\circ$.

## 4. Why changing duration changes velocity and acceleration

Differentiate the normalized cubic:

$$
\dot{\theta}(t)=\frac{\Delta\theta}{T_f}(6s-6s^2),
$$

$$
\ddot{\theta}(t)=\frac{\Delta\theta}{T_f^2}(6-12s).
$$

These equations reveal the time-scaling rule:

- velocity is proportional to $1/T_f$;
- acceleration is proportional to $1/T_f^2$.

If the same motion takes twice as long, its peak velocity is cut in half and its peak acceleration becomes one quarter as large. If the duration is halved, peak velocity doubles and peak acceleration quadruples.

This is why slowing a motion often reduces actuator demand. It does not, however, change gravity torque at a given pose or make an unreachable pose reachable.

## 5. Cubic, quintic, and trapezoidal profiles

A cubic rest-to-rest trajectory guarantees zero endpoint velocity, but its endpoint acceleration is generally nonzero. Joining that motion directly to a stationary hold can create an acceleration and torque jump.

A quintic time-scaling function has enough coefficients to set position, velocity, and acceleration at both endpoints. A common normalized form is

$$
s(u)=10u^3-15u^4+6u^5,\qquad u=\frac{t}{T_f}.
$$

Use it in

$$
\theta(t)=\theta_0+(\theta_f-\theta_0)s(u).
$$

The quintic begins and ends with zero velocity and zero acceleration, so it connects more smoothly to a stationary hold.

A trapezoidal velocity profile uses three phases: accelerate, travel at approximately constant speed, then decelerate. It is easy to interpret and can directly reflect velocity and acceleration limits. The corners of an ideal trapezoid imply acceleration changes; practical controllers may round them.

No profile is universally best. The choice depends on endpoint smoothness, motion time, actuator limits, and how the reference will be tracked.

## 6. Synchronizing several joints

For a multi-joint robot, use the same progress function $s(t)$ for every joint:

$$
q_i(t)=q_{i,0}+\left(q_{i,f}-q_{i,0}\right)s(t).
$$

All joints start and finish together because they share the same duration and normalized clock. Each joint still travels a different angular distance and therefore has its own peak velocity and acceleration.

The duration must satisfy the limits of every joint. One slow or heavily loaded joint can determine the minimum feasible duration for the whole synchronized move.

## 7. Joint-space motion and Cartesian motion are different

A MoveJ-style motion interpolates joint angles. It is simple and usually produces smooth joint commands, but the end effector generally follows a curved path because forward kinematics is nonlinear:

$$
\mathbf x(t)=f\!\left(\mathbf q(t)\right).
$$

Even when every component of $\mathbf q(t)$ changes smoothly, $f(\mathbf q)$ does not usually map that motion to a straight Cartesian line.

A practical MoveL-style motion begins with a desired Cartesian path. For a straight position segment,

$$
\mathbf p(t)=\mathbf p_0+\left(\mathbf p_f-\mathbf p_0\right)s(t).
$$

The program samples this path and solves IK at each waypoint. The previous joint solution should seed the next IK solve so the solver tends to remain on the same solution branch.

A straight Cartesian path can therefore require a complicated joint-space path. Joint limits, singularities, reachability, and discontinuous IK solutions must still be checked.

## 8. Waypoints and continuity

A waypoint is an intermediate desired configuration or pose. Stopping at every waypoint is easy because each segment can use zero endpoint velocity. Passing smoothly through a waypoint is harder because adjacent segments must agree on velocity and preferably acceleration.

Smaller waypoint spacing can represent a Cartesian line more accurately, but it increases the number of IK solves and commands. Very coarse spacing can produce visible corner cutting or large interpolation error. Very fine spacing does not automatically improve tracking if the controller or simulation step cannot follow the commands.

## 9. A generated trajectory is a reference, not a measurement

The generated trajectory describes what the robot should do. Sensors and FK describe what it actually did. For joint $i$, define tracking error as

$$
e_i(t)=q_{\mathrm{des},i}(t)-q_{\mathrm{meas},i}(t).
$$

A useful summary is root-mean-square error:

$$
\operatorname{RMSE}_i
=\sqrt{\frac{1}{N}\sum_{k=1}^{N}e_i(t_k)^2}.
$$

RMSE describes typical error but can hide a short large deviation, so also report maximum absolute error.

For a desired Cartesian line from $\mathbf p_0$ to $\mathbf p_f$, straightness error is the shortest distance from each measured FK point to that line segment. Use the same physical point for the desired and measured paths. In this lab, that means comparing the visible stylus tip with the desired stylus-tip path, not mixing the tool origin with the tip.

Use Webots simulation time rather than wall-clock time. Wall-clock time depends on computer speed and simulation rendering; simulation time represents the experiment.

## 10. Feasibility checks before motion

A mathematically smooth trajectory can still be unsafe or impossible. Check at least:

1. joint position limits;
2. joint velocity and acceleration limits;
3. IK convergence and continuity;
4. singularity or poor-conditioning warnings;
5. collision and workspace constraints; and
6. actuator torque limits when a dynamics model is available.

For a cubic rest-to-rest move, increasing $T_f$ reduces velocity and acceleration demand. It does not change the path geometry, the final pose, or the stationary torque required to hold that final pose.

The core workflow is therefore:

```text
choose endpoints and a path
        -> choose a time-scaling law
        -> sample position, velocity, and acceleration
        -> check limits and IK continuity
        -> execute the reference
        -> measure and evaluate the result
```

That sequence connects trajectory generation to the tracking measurements required in Lab 5.
