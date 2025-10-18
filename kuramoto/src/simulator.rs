use crate::config::Config;
use rand::Rng;
use rand_distr::{Distribution, Normal};

pub struct Simulator {
    pub config: Config,
    pub phases: Vec<f64>, // The phases (theta_i) of the oscillators
    pub frequencies: Vec<f64>, // The frequencies (omega_i) of the oscillators
}

impl Simulator {
    pub fn new(config: Config) -> Self {
        let mut rng = rand::thread_rng();

        // Initialise the phases of the oscillators randomly between 0 and 2π
        let phases: Vec<f64> = (0..config.N).map(|_| rng.gen_range(0.0..2.0 * std::f64::consts::PI)).collect();

        // Initialise the frequencies of the oscillators randomly from a normal distribution
        // with mean 1.0 and variance 0.1
        let normal_distribution = Normal::new(1.0, 0.1).unwrap();
        let frequencies: Vec<f64> = (0..config.N).map(|_| normal_distribution.sample(&mut rng)).collect();

        Self {
            config,
            phases,
            frequencies,
        }
    }

    // Non-vectorised update step for all oscillators
    pub fn step(&mut self) {
        let mut new_phases = Vec::with_capacity(self.config.N);

        for i in 0..self.config.N {
            // Calculate the coupling term for the i-th oscillator
            let mut coupling = 0.0;
            for j in 0..self.config.N {
                coupling += (self.phases[j] - self.phases[i]).sin();
            }

            let coupling_increment  = (self.config.K / self.config.N as f64) * coupling;

            // Update the phase of the i-th oscillator
            let new_phase = self.phases[i] + self.config.dt * (self.frequencies[i] + coupling_increment);
            new_phases.push(new_phase.rem_euclid(2.0 * std::f64::consts::PI));
        }

        self.phases = new_phases;
    }

    pub fn run(&mut self) {
        for _ in 0..self.config.n_steps {
            self.step();
        }
    }
}