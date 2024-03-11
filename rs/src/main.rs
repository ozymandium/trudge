use trudge::csv::load_csv;

use clap::{Parser, ValueHint};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the CSV file with raw set logs
    #[clap(short = 'i', long = "in", value_parser, value_hint = ValueHint::FilePath)]
    csv_in: PathBuf,

    /// Path to output CSV file with 1 rep maxes
    #[clap(short = 'o', long = "out", value_parser, value_hint = ValueHint::FilePath)]
    csv_out: PathBuf,

    /// Name of the lift
    #[clap(short, long)]
    name: String,
}

fn main() {
    let args = Args::parse();

    if !args.csv_in.exists() {
        eprintln!("The specified CSV file does not exist: {:?}", args.csv_in);
        std::process::exit(1);
    }

    println!("Processing CSV file: {:?}", args.csv_in);
    println!("Lift name: {}", args.name);

    match load_csv(&args.csv_in) {
        Ok(df) => {
            println!("Loaded {} rows and {} columns", df.height(), df.width());
            println!("{:?}", df);
        }
        Err(e) => eprintln!("Error loading the CSV file: {}", e),
    }
}
