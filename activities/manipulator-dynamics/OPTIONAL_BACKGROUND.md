# Manipulator Dynamics Optional Background

This page develops the main ideas behind manipulator dynamics before the detailed derivations and activities. The goal is to connect each equation to a physical question: **What torque is needed, and what motion will that torque produce?**

Return to the [Manipulator Dynamics activity](README.md) when you are ready to work through the calculations and code.

## 1. Kinematics describes motion; dynamics explains its cause

Kinematics relates joint variables to robot motion. For example, forward kinematics finds the arm pose from its joint angles, and a Jacobian relates joint velocity to tool velocity. These calculations do not require the link masses.

Dynamics connects motion to forces and torques. It answers two complementary questions:

- **Inverse dynamics:** If the desired motion is known, what motor torque is required?
- **Forward dynamics:** If a motor torque is applied, what acceleration and motion result?

The distinction is similar to planning a car's speed versus determining how much engine and braking force are required to follow that plan.

## 2. A one-joint torque balance

For the vertical 1R arm in this activity, the joint equation is

$$
\tau=I\ddot{\theta}+b\dot{\theta}+mgr_c\sin\theta.
$$

Read the equation as a torque budget:

| Contribution | Physical meaning |
|---|---|
| $I\ddot{\theta}$ | torque used to accelerate the rotating mass |
| $b\dot{\theta}$ | torque used to overcome modeled viscous friction |
| $mgr_c\sin\theta$ | torque used to oppose gravity |

The motor supplies the sum of all three contributions. Which term dominates depends on what the arm is doing.

- When the arm is stationary, velocity and acceleration are zero, so only gravity remains.
- During a fast acceleration, the inertia term may be large.
- At steady nonzero speed, acceleration is zero, but friction and gravity may still require torque.

## 3. Why gravity torque depends on angle

Gravity acts downward at the center of mass. Its turning effect about the joint equals force times the perpendicular moment arm.

The gravitational force magnitude is $mg$, and the perpendicular moment arm is $r_c\sin\theta$. Therefore,

$$
\tau_g=mgr_c\sin\theta.
$$

This agrees with physical intuition:

- At $\theta=0^\circ$, the link hangs downward. Gravity acts through the joint axis, so the moment arm and gravity torque are zero.
- At $\theta=90^\circ$, the link is horizontal. The moment arm is largest, so the gravity torque magnitude is largest.
- At $\theta=180^\circ$, the link points upward. The ideal gravity torque is again zero, although this equilibrium is unstable.

Holding a pose is therefore a dynamics problem even when the arm is not moving.

## 4. Rotational inertia depends on where the mass is located

Mass measures resistance to linear acceleration. Rotational inertia measures resistance to angular acceleration. Mass farther from the joint contributes more because distance enters as a square.

For a uniform slender rod of length $L$, the inertia about its own center of mass is

$$
I_{\mathrm{COM}}=\frac{mL^2}{12}.
$$

The joint is $L/2$ from the center of mass. The parallel-axis theorem shifts the inertia to the joint:

$$
I_{\mathrm{joint}}
=I_{\mathrm{COM}}+m\left(\frac{L}{2}\right)^2
=\frac{mL^2}{3}.
$$

A point payload of mass $m_p$ at distance $r_p$ adds

$$
I_p=m_pr_p^2.
$$

Because of the squared distance, moving the same payload twice as far from the joint produces four times its rotational-inertia contribution. Payload **location**, not only payload mass, matters.

## 5. Inverse and forward dynamics use the same model differently

Inverse dynamics begins with a desired angle, velocity, and acceleration and calculates torque:

$$
\tau(t)
=I\ddot{\theta}(t)
+b\dot{\theta}(t)
+mgr_c\sin\theta(t).
$$

This is useful for checking whether a planned trajectory demands more torque than the actuator can provide.

Forward dynamics rearranges the same equation to calculate acceleration from applied torque:

$$
\ddot{\theta}
=\frac{\tau-b\dot{\theta}-mgr_c\sin\theta}{I}.
$$

A simulator repeatedly evaluates this acceleration and integrates it to update velocity and position. In short:

```text
inverse dynamics: desired motion -> required torque
forward dynamics: applied torque -> resulting motion
```

## 6. The energy method explains the same equation

The Lagrange method builds the equation of motion from energy.

The link's kinetic energy is

$$
K=\frac{1}{2}I\dot{\theta}^{\,2}.
$$

With the activity's downward-zero angle convention, its gravitational potential energy can be written as

$$
P=mgr_c(1-\cos\theta).
$$

Lagrange's equation is

$$
\frac{d}{dt}\left(\frac{\partial K}{\partial\dot{\theta}}\right)
-\frac{\partial K}{\partial\theta}
+\frac{\partial P}{\partial\theta}
=\tau-b\dot{\theta}.
$$

Evaluating the derivatives gives the same torque balance:

$$
I\ddot{\theta}+b\dot{\theta}+mgr_c\sin\theta=\tau.
$$

The energy method becomes especially valuable for multi-link robots, where drawing and summing every force and moment is more difficult.

## 7. Why a slower trajectory usually requires less peak torque

Suppose the arm follows the same geometric motion but the duration is increased. Time scaling changes the derivatives approximately as

$$
\dot{\theta}\propto\frac{1}{T_f},
\qquad
\ddot{\theta}\propto\frac{1}{T_f^2}.
$$

Doubling the duration therefore halves the velocity-related term and reduces the acceleration-related term to about one quarter. The gravity term does not automatically shrink because it depends mainly on pose, not speed.

This leads to an important engineering lesson: slowing a trajectory can reduce dynamic torque, but it does not eliminate the torque required to hold a horizontal load.

## 8. A torque limit must be checked throughout the task

A trajectory is not feasible merely because the arm reaches its final angle. The required torque should satisfy

$$
|\tau(t)|\le\tau_{\max}
$$

throughout the motion and at the final hold.

The largest torque may occur while accelerating, while passing through a gravity-demanding pose, or after motion stops and the motor must hold the load. Plotting the inertia, friction, gravity, and total-torque terms separately helps reveal the cause of a limit violation.

## 9. What the simple model leaves out

The 1R model is intentionally small enough to understand completely. A real manipulator can also include multiple moving links, coupling between joints, nonlinear friction, motor and gearbox dynamics, flexibility, backlash, contact forces, and parameter uncertainty.

For a multi-joint robot, the same ideas are commonly collected into

$$
\boldsymbol{\tau}
=\mathbf M(\mathbf q)\ddot{\mathbf q}
+\mathbf C(\mathbf q,\dot{\mathbf q})\dot{\mathbf q}
+\mathbf g(\mathbf q)
+\boldsymbol{\tau}_{f}.
$$

The symbols are larger, but the physical story is unchanged: motor torque must account for acceleration, velocity-dependent effects, gravity, and friction. The one-joint activity is the simplest useful version of that general manipulator equation.
