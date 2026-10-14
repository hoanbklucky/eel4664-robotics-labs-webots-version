import numpy as np
import matplotlib.pyplot as plt

m, L, g, b = 2.0, 0.6, 10.0, 0.1
rc = L / 2
I = m * L**2 / 3  # uniform rod inertia ABOUT THE JOINT

def inverse_1r(q, qd=0.0, qdd=0.0, payload=0.0):
    inertia = I + payload * L**2  # point payload at tip
    gravity_coefficient = m*g*rc + payload*g*L
    return inertia*qdd + b*qd + gravity_coefficient*np.sin(q)

def acceleration_1r(q, qd, tau, payload=0.0):
    inertia = I + payload * L**2
    gravity_coefficient = m*g*rc + payload*g*L
    return (tau - b*qd - gravity_coefficient*np.sin(q))/inertia

print(f"I = {I:.3f} kg m^2")
print(f"Holding at 30 deg: {inverse_1r(np.deg2rad(30)):.3f} N m")
print(f"Dynamic example: {inverse_1r(np.deg2rad(60), 2, 3):.3f} N m")


angles_deg = np.linspace(0, 180, 181)
angles_rad = np.deg2rad(angles_deg)
for payload in [0.0, 0.5]:
    torque = inverse_1r(angles_rad, payload=payload)
    plt.plot(angles_deg, torque, label=f"Payload {payload:g} kg")
    print(f"Payload {payload:g} kg: hold at 90 deg = "
          f"{inverse_1r(np.pi/2, payload=payload):.3f} N m")
plt.xlabel("Angle from downward vertical (deg)")
plt.ylabel("Holding torque (N m)")
plt.legend(); plt.grid(); plt.show()


def cubic_trajectory(duration, n=2001, q0=0.0, qf=np.pi/2):
    t = np.linspace(0, duration, n)
    s = t/duration
    dq = qf-q0
    q = q0 + dq*(3*s**2-2*s**3)
    qd = dq*(6*s-6*s**2)/duration
    qdd = dq*(6-12*s)/duration**2
    return t, q, qd, qdd

fig, axes = plt.subplots(4, 1, figsize=(9, 10), sharex=False)
for duration in [2.0, 1.0]:
    t, q, qd, qdd = cubic_trajectory(duration)
    tau = inverse_1r(q, qd, qdd)
    for ax, values, ylabel in zip(axes, [np.rad2deg(q), qd, qdd, tau],
                                 ["Angle (deg)", "Velocity (rad/s)",
                                  "Acceleration (rad/s²)", "Torque (N m)"]):
        ax.plot(t, values, label=f"Duration {duration:g} s")
        ax.set_ylabel(ylabel); ax.set_xlabel("Time (s)"); ax.grid(); ax.legend()
    print(f"Duration={duration:g} s: max |qd|={np.max(abs(qd)):.3f}, "
          f"max |qdd|={np.max(abs(qdd)):.3f}, "
          f"max |inertial torque|={np.max(abs(I*qdd)):.3f}, "
          f"max |total torque|={np.max(abs(tau)):.3f}")
plt.tight_layout(); plt.show()

for payload in [0.0, 0.5]:
    for duration in [2.0, 1.0]:
        t, q, qd, qdd = cubic_trajectory(duration)
        peak = np.max(abs(inverse_1r(q, qd, qdd, payload)))
        # Include the stationary final hold after the cubic ends.
        hold = abs(inverse_1r(q[-1], payload=payload))
        print(f"Payload={payload:g} kg, duration={duration:g} s: "
              f"sampled motion peak={peak:.3f} N m, final hold={hold:.3f} N m, "
              f"feasible incl. final hold={max(peak, hold) <= 6.0}")
