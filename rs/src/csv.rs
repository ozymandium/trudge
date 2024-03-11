use lazy_static::lazy_static;
use polars::prelude::*;
use std::sync::Arc;

/// The minimum effort level
const EFFORT_MIN: u32 = 1;
/// The maximum effort level
const EFFORT_MAX: u32 = 5;

lazy_static! {
    static ref SCHEMA: Arc<Schema> = Arc::new(Schema::from_iter(
        vec![
            Field::new("time", DataType::Datetime(TimeUnit::Milliseconds, None)),
            Field::new("name", DataType::String),
            Field::new("reps", DataType::UInt32),
            Field::new("weight", DataType::Float32),
            Field::new("rest", DataType::Float32),
            Field::new("positive", DataType::Float32),
            Field::new("hold", DataType::Float32),
            Field::new("negative", DataType::Float32),
            Field::new("effort", DataType::UInt32),
            Field::new("heart", DataType::UInt32),
            Field::new("trainer", DataType::Boolean),
            Field::new("unilateral", DataType::Boolean),
            Field::new("notes", DataType::String),
        ]
        .into_iter()
    ));
}

/// Load the CSV file and validate it.
///
/// # Arguments
///
/// * `file` - The path to the CSV file
///
/// # Returns
///
/// A DataFrame with the contents of the CSV file
///
/// # Errors
///
/// If the CSV file has an invalid schema or the effort column has invalid values
pub fn load_csv(file: &std::path::Path) -> Result<DataFrame, PolarsError> {
    let df = CsvReader::from_path(file)?
        .with_schema(Some(SCHEMA.clone()))
        .has_header(true)
        .finish()?;
    validate_csv(&df).unwrap();
    Ok(df)
}

/// Validate the CSV file.
///
/// # Arguments
///
/// * `df` - The DataFrame with the contents of the CSV file
///
/// # Returns
///
/// An empty result if the CSV file is valid
///
/// # Errors
///
/// If the CSV file has an invalid schema or the effort column has invalid values
///
/// # Panics
///
/// If the effort column is not found
fn validate_csv(df: &polars::prelude::DataFrame) -> Result<(), Box<dyn std::error::Error>> {
    // clone the schema arc
    let expected_schema = SCHEMA.clone();

    // check the values in the effort column are within the expected range
    let effort = df.column("effort").unwrap().u32()?;
    // the minimum that was received
    let effort_min = effort.min().unwrap();
    let effort_max = effort.max().unwrap();
    if effort_min < EFFORT_MIN || effort_max > EFFORT_MAX {
        return Err(format!(
            "The CSV file has an invalid effort column:\nExpected: {} <= effort <= {}\nGot: {} <= effort <= {}",
            EFFORT_MIN, EFFORT_MAX, effort_min, effort_max
        )
        .into());
    }

    Ok(())
}
