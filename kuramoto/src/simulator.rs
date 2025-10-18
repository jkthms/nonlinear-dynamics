use crate::config::Config;
use rand::Rng;
use rand_distr::{Distribution, Normal};
use anyhow::Result;
use std::fs::File;
use std::sync::Arc;
use arrow::array::{Float64Array, UInt64Array};
use arrow::datatypes::{DataType, Field, Schema};
use arrow::record_batch::RecordBatch;
use parquet::arrow::ArrowWriter;
use parquet::file::properties::WriterProperties;


pub struct Simulator {
    pub config: Config,
    pub phases: Vec<f64>, // The phases (theta_i) of the oscillators
    pub frequencies: Vec<f64>, // The frequencies (omega_i) of the oscillators
}

impl Simulator {
    pub fn new(config: Config) -> Self {
        let mut rng = rand::rng();

        // Initialise the phases of the oscillators randomly between 0 and 2π
        let phases: Vec<f64> = (0..config.N).map(|_| rng.random_range(0.0..2.0 * std::f64::consts::PI)).collect();

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

    pub fn run(&mut self) -> Result<()> {
        // Define the schema for the output .pq file
        let schema = Schema::new(
            vec![
                Field::new("time", DataType::UInt64, false),
                Field::new("oscillator", DataType::UInt64, false),
                Field::new("phase", DataType::Float64, false),
                Field::new("frequency", DataType::Float64, false),
            ]
        );

        // Create the output file
        let file = File::create("kuramoto.pq")?;
        let props = WriterProperties::builder().build();
        let mut writer = ArrowWriter::try_new(file, Arc::new(schema.clone()), Some(props))?;

        // Run the step-wise simulation and collect data at each step
        for step in 0..self.config.n_steps {
            self.step();

            // Prepare the output data for this time step
            let timestamps: Vec<u64> = vec![step as u64; self.config.N];
            let oscillator_ids: Vec<u64> = (0..self.config.N as u64).collect();
            let phases: Vec<f64> = self.phases.clone();
            let frequencies: Vec<f64> = self.frequencies.clone();

            // Create the record batch using the Arrow array types
            let time_array = UInt64Array::from(timestamps);
            let oscillator_array = UInt64Array::from(oscillator_ids);
            let phase_array = Float64Array::from(phases);
            let frequency_array = Float64Array::from(frequencies);

            let record_batch = RecordBatch::try_new(Arc::new(schema.clone()), vec![
                Arc::new(time_array),
                Arc::new(oscillator_array),
                Arc::new(phase_array),
                Arc::new(frequency_array),
            ])?;

            writer.write(&record_batch)?;
        }

        writer.close()?;
        Ok(())
    }
}