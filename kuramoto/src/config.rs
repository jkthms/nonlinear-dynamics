use anyhow::Result;
use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub N: usize,       // Number of oscillators (N)
    pub K: f64,         // Coupling strength of the oscillators to each other (K)
    pub dt: f64,        // Discretisation time step in seconds
    pub n_steps: usize, // The number of discrete time steps to simulate
}

impl Config {
    /// Load the configuration from a TOML file
    pub fn from_file(path: &str) -> Result<Self> {
        let contents = fs::read_to_string(path)?;
        let config: Self = toml::from_str(&contents)?;
        Ok(config)
    }
}
