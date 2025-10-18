mod config;
mod simulator;

use anyhow::Result;
use config::Config;
use simulator::Simulator;
use std::time::Instant;

fn main() -> Result<()> {
    let config = Config::from_file("config.toml")?;
    println!("Loaded configuration: {:?}", config);

    let mut sim = Simulator::new(config);
    println!("Initialised simulator with {} oscillators.", sim.config.N);

    println!("Running simulation...");
    let start = Instant::now();
    sim.run()?;
    let duration = start.elapsed();
    
    println!("Simulation completed successfully in {:.2}s", duration.as_secs_f64());
    println!("Output written to kuramoto.pq");
    
    Ok(())
}
