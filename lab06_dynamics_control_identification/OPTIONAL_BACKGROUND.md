# Lab 6 Optional Background

This page develops the core ideas behind feedback control, model-based tracking, and one-joint parameter identification. Read Sections 1 through 6 for the main concepts. The later sections explain integral action, stability, and experimental interpretation in more detail.

Return to the [Lab 6 instructions](README.md) when you are ready to complete the required activity.

## 1. Why a robot needs feedback

A trajectory generator supplies the desired motion. It does not guarantee that the real or simulated robot follows that motion. Gravity, inertia, friction, modeling error, disturbances, and actuator limits can all create tracking error.

Feedback repeatedly performs four actions:

```text
measure the joint
    -> compare it with the desired motion
    -> calculate a corrective torque
    -> apply the torque and measure again
```

The controller does not need to predict every disturbance in advance. It observes the error produced by those effects and reacts to it.

For one joint, let

- $\theta_d$ be the desired angle;
- $\theta$ be the measured angle;
- $e=\theta_d-\theta$ be the position error; and
- $\tau$ be the commanded motor torque.

A positive error means the measured angle is smaller than the desired angle, so the controller should generally create positive torque under the sign convention used in this lab.

## 2. The one-joint plant model

The **plant** is the physical system being controlled. A focused model for one revolute joint is

$$
I\ddot{\theta}+b\dot{\theta}+G\sin\theta=\tau+d.
$$

Each term has a physical meaning:

| Term | Meaning |
|---|---|
| $I\ddot{\theta}$ | torque associated with angular acceleration |
| $b\dot{\theta}$ | modeled viscous-friction torque |
| $G\sin\theta$ | gravity torque |
| $\tau$ | commanded motor torque |
| $d$ | unmodeled disturbance torque |

The equation is a balance of torques. If the commanded torque is larger than the opposing gravity and friction terms, the remaining torque accelerates the joint.

Solving for acceleration gives the forward-dynamics form

$$
\ddot{\theta}
=\frac{\tau+d-b\dot{\theta}-G\sin\theta}{I}.
$$

This equation explains why a torque command does not directly specify angle. Torque first changes acceleration; acceleration changes velocity; velocity changes angle.

## 3. Position error and velocity error

Position error is

$$
e=\theta_d-\theta.
$$

Differentiate it to obtain velocity error:

$$
\dot e=\dot{\theta}_d-\dot{\theta}.
$$

For a fixed setpoint, $\dot{\theta}_d=0$, so

$$
\dot e=-\dot{\theta}.
$$

This sign is important. If the arm is already moving toward a fixed target, the velocity-error term acts against that motion and supplies damping.

The controller must use consistent units. Angles should be in radians when multiplied by gains. If $K_P$ has units $\mathrm{N\,m/rad}$, multiplying it by an error in degrees produces the wrong torque by a factor of $180/\pi$.

Measured velocity is often estimated from sampled position:

$$
\dot{\theta}_{\mathrm{est}}(t_k)
\approx\frac{\theta(t_k)-\theta(t_{k-1})}{\Delta t}.
$$

Differentiation amplifies measurement noise. Filtering can reduce noise but adds delay, so the filter and sample period are part of the controller design.

## 4. Proportional control

A proportional controller commands torque in proportion to position error:

$$
\tau_P=K_Pe.
$$

A larger $K_P$ produces a stronger correction for the same error. This usually makes the response faster, but excessive gain can create oscillation, overshoot, or saturation.

Proportional control behaves like a virtual torsional spring. The desired angle is the spring's neutral position, and the error determines how strongly it pulls the joint back toward that position.

Proportional control alone does not automatically remove steady error. If gravity applies a constant load, a nonzero position error may be required to generate enough proportional torque to hold the arm.

At a stationary equilibrium without gravity compensation,

$$
K_P(\theta_d-\theta)=G\sin\theta.
$$

The left side is controller torque and the right side is the torque needed to balance gravity.

## 5. Derivative action and PD control

A proportional-derivative controller uses both position and velocity error:

$$
\tau_{PD}=K_Pe+K_D\dot e.
$$

For a fixed target,

$$
\tau_{PD}=K_P(\theta_d-\theta)-K_D\dot{\theta}.
$$

The derivative term behaves like a virtual damper. It opposes motion and removes energy from oscillation. Increasing $K_D$ usually reduces overshoot, although too much derivative action can slow the response and make measurement noise more visible in the torque command.

Proportional and derivative gains play different roles:

- $K_P$ mainly sets how strongly position error is corrected;
- $K_D$ mainly sets how strongly motion is damped.

They interact, so tune and evaluate them as a pair rather than treating each gain independently.

## 6. Gravity compensation

If the gravity model is known, add the predicted gravity torque to the feedback command:

$$
\tau=K_Pe+K_D\dot e+G\sin\theta.
$$

At a stationary desired pose with an exact model, the gravity term supplies the holding torque while the feedback terms approach zero. The robot no longer needs a deliberate position error just to balance gravity.

Gravity compensation does not replace feedback. A model can be inaccurate, and an external disturbance may not be included in $G\sin\theta$. Feedback corrects the remaining error.

Gravity compensation also cannot overcome an actuator limit. If a pose requires $9\ \mathrm{N\,m}$ but the joint is limited to $6\ \mathrm{N\,m}$, no choice of feedback gains can make that stationary hold feasible.

## 7. Tracking a changing trajectory

For a moving target, the trajectory generator supplies

$$
\theta_d(t),\qquad \dot{\theta}_d(t),\qquad \ddot{\theta}_d(t).
$$

A model-based tracking law combines feedforward and feedback:

$$
\tau
=I\ddot{\theta}_d+b\dot{\theta}_d+G\sin\theta
+K_Pe+K_D\dot e.
$$

The first three terms are **feedforward**. They estimate the torque the desired motion should require even if tracking were perfect. The last two terms are **feedback**. They correct the difference between desired and measured motion.

This division is useful:

- feedforward handles predictable dynamics;
- feedback handles initial error, model mismatch, and disturbances.

With perfect tracking and a perfect model, the feedback terms become small. In a real experiment they rarely become exactly zero.

## 8. Integral action and PID control

Integral action accumulates error over time:

$$
z(t)=\int_0^t e(\lambda)\,d\lambda.
$$

A PID controller with gravity compensation can be written as

$$
\tau=K_Pe+K_D\dot e+K_Iz+G\sin\theta.
$$

Integral action is useful when a persistent disturbance or model error leaves a steady offset. Even a small error accumulates, increasing the integral torque until the offset is reduced.

The same memory creates a risk called **integral windup**. If the actuator saturates, the requested torque cannot be applied, but the integral can continue growing. When the joint finally leaves saturation, the stored integral may cause large overshoot.

A common anti-windup rule stops or limits integration when the actuator is saturated and the current error would push it farther into saturation. Anti-windup improves recovery; it cannot make an infeasible torque demand feasible.

## 9. The closed-loop error model

With PD control, exact gravity compensation, a fixed desired angle, and no disturbance, substitution into the plant model gives

$$
I\ddot e+(b+K_D)\dot e+K_Pe=0.
$$

This has the familiar form of a second-order mass-spring-damper system:

- $I$ acts like mass;
- $K_P$ acts like spring stiffness;
- $b+K_D$ acts like damping.

The natural frequency and damping ratio are

$$
\omega_n=\sqrt{\frac{K_P}{I}},
$$

$$
\zeta=\frac{b+K_D}{2\sqrt{IK_P}}.
$$

These equations explain the trends seen in simulation. Raising $K_P$ tends to increase response speed, while raising $K_D$ tends to increase damping. They are local design guides because saturation, nonlinear gravity, discrete sampling, and filtering can change the actual response.

With integral action, stability depends on all three gains. More integral gain is not automatically better.

## 10. Parameter identification as an experiment

The same plant equation can be used to estimate unknown parameters. Rearrange measured samples into a linear regression form:

$$
\tau_k
=I_{\mathrm{eff}}\ddot q_k
+b_{\mathrm{eff}}\dot q_k
+g_{\mathrm{eff}}(q_k).
$$

For a simple gravity model $g_{\mathrm{eff}}(q)=G\sin q$, define

$$
\boldsymbol\phi_k=
\begin{bmatrix}
\ddot q_k & \dot q_k & \sin q_k
\end{bmatrix},
\qquad
\boldsymbol\beta=
\begin{bmatrix}
I_{\mathrm{eff}} & b_{\mathrm{eff}} & G
\end{bmatrix}^{T}.
$$

Then

$$
\tau_k\approx\boldsymbol\phi_k\boldsymbol\beta.
$$

Stack many samples and solve a least-squares problem. Good parameter estimates require motion that excites the different terms. A nearly stationary experiment cannot identify inertia well because acceleration is too small. A narrow angle range may not reveal gravity clearly.

Validate the model on data that were not used for fitting. A model that only matches its training trial may be fitting noise rather than dynamics.

## 11. What to look for in the plots

When comparing controllers, do not judge only by whether the final angle looks correct. Examine:

- rise time and settling time;
- overshoot and oscillation;
- steady-state error;
- RMS and maximum tracking error;
- peak and RMS torque;
- time spent in saturation; and
- sensitivity to disturbances or payload changes.

A controller that tracks slightly better but spends most of the experiment saturated may not be robust. A very smooth torque trace may correspond to a response that is too slow. State the tradeoff shown by the measurements.

The complete control workflow is

```text
generate a desired trajectory
        -> measure position and estimate velocity
        -> calculate feedforward and feedback torque
        -> enforce actuator limits
        -> apply the command
        -> log and evaluate the response
```

That loop connects the equations on this page to the Webots experiment in Lab 6.
