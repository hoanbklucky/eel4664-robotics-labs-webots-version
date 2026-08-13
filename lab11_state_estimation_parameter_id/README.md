# Lab 11 ? State Estimation and Parameter Identification

## Motivation

Sensors provide samples, not perfect state; useful models must be estimated and then tested on data they did not fit.

## Learning objectives

Estimate velocity from sampled position; explain noise amplification; implement filtering; identify a simple parameter by least squares; and validate on held-out Webots data.

## Investigation

1. Generate repeatable Webots position/command/torque logs using simulation timestamps.
2. Complete `src/estimate_velocity.py` with backward and centered differences plus an explicit filter.
3. Compare estimates with a known trajectory derivative or simulator reference reserved for validation.
4. Complete `src/least_squares_id.py`; state the regressor and parameter meaning.
5. Fit on one trial and validate on another speed or payload. Report residuals, not only fitted parameters.

## Submission

Submit source, raw-data description, velocity plots/errors, regression derivation, held-out validation, and `answers.md`.
