use clap::{Parser, ValueHint};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the CSV file
    #[clap(short, long, value_parser, value_hint = ValueHint::FilePath)]
    file: PathBuf,

    /// Name of the lift
    #[clap(short, long)]
    name: String,
}

fn main() {
    let args = Args::parse();

    if !args.file.exists() {
        eprintln!("The specified CSV file does not exist: {:?}", args.file);
        std::process::exit(1);
    }

    println!("Processing CSV file: {:?}", args.file);
    println!("Hello, {}!", args.name);
}