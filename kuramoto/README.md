# Kuramoto

This package is a Rust implementation of the Kuramoto model, which is a mathematical model of synchronisation in a system of coupled oscillators. It is governed by the following set of equations:

$$
\dot{\theta}_i = \omega_i + \frac{K}{N} \sum_{j=1}^{N} \sin(\theta_j - \theta_i)
$$

where $\theta_i$ is the phase of the $i$-th oscillator, $\omega_i$ is the natural frequency of the $i$-th oscillator, $K$ is the coupling strength, and $N$ is the number of oscillators.

## Discretisation

This differential equation can be discretised in time to give the following forward-Euler update:

$$
\theta_i(t + \Delta t) = \theta_i(t) + \Delta t \left( \omega_i + \frac{K}{N} \sum_{j=1}^{N} \sin(\theta_j(t) - \theta_i(t)) \right)
$$

The package contained herein contains a simple implementation of a simulator for the Kuramoto model.
