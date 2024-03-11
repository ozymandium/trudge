use lazy_static::lazy_static;
use polars::prelude::*;
use std::sync::Arc;

/// The minimum effort level
const EFFORT_MIN: u8 = 1;
/// The maximum effort level
const EFFORT_MAX: u8 = 5;

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
pub fn load_csv(file: &std::path::Path) -> Result<DataFrame, PolarsError> {
    CsvReader::from_path(file)?
        .with_schema(Some(SCHEMA.clone()))
        .has_header(true)
        .finish()
}

// fn validate_csv(df: &polars::prelude::DataFrame) -> Result<(), Box<dyn std::error::Error>> {
//     // check the schema
//     let schema = df.schema();
//     if schema != SCHEMA {
//         return Err(format!(
//             "The CSV file has an invalid schema: expected {:?}, got {:?}",
//             SCHEMA, schema
//         )
//         .into());
//     }

//     // check the values in the effort column
//     let effort = df.column("effort").unwrap().u8().unwrap();
//     if effort.min()? < EFFORT_MIN || effort.max()? > EFFORT_MAX {
//         return Err(format!(
//             "The effort column has invalid values: expected {}-{}, got {}-{}",
//             EFFORT_MIN,
//             EFFORT_MAX,
//             effort.min()?,
//             effort.max()?
//         )
//         .into());
//     }

//     Ok(())
// }
