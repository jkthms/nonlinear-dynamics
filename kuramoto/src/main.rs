mod config;

use config::Config;
use anyhow::Result;

fn main() -> Result<()> {
    let config = Config::from_file("config.toml")?;
    println!("Loaded configuration: {:?}", config);
    Ok(())
}
