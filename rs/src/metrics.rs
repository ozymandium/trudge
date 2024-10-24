

/// Enum for the available 1 rep max formulae
pub enum Formula {
    /// Brzycki formula
    Brzycki,
    /// Epley formula
    Epley,
    /// Lander formula
    Lander,
    /// Lombardi formula
    Lombardi,
    /// Mayhew formula
    Mayhew,
    /// O'Conner formula
    OConner,
    /// Wathan formula
    Wathan,
}

/// Compute the 1 rep max using the Brzycki formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn brzycki(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    weight * (36.0 / (37.0 - reps))
}

/// Compute the 1 rep max using the Epley formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn epley(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    weight * (1.0 + reps / 30.0)
}

/// Compute the 1 rep max using the Lander formula
/// 
/// # Arguments
///
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn lander(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    (100.0 * weight) / (101.3 - 2.67123 * reps)
}

/// Compute the 1 rep max using the Lombardi formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn lombardi(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    weight * reps.powf(0.10)
}

/// Compute the 1 rep max using the Mayhew formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn mayhew(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    (100.0 * weight) / (52.2 + 41.9 * std::f32::consts::E.powf(-0.055 * reps))
}

/// Compute the 1 rep max using the O'Conner formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn oconner(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    weight * (1.0 + reps / 40.0)
}

/// Compute the 1 rep max using the Wathan formula
/// 
/// # Arguments
/// 
/// * `weight` - Column of f32 values containing weight that was lifted
/// 
/// * `reps` - Column of f32 values containing the number of reps
/// 
/// # Returns
/// 
/// A new column with the 1 rep max in the same unit as the weight
fn wathan(weight: Float32Chunked, reps: Float32Chunked) -> Float32Chunked {
    (100.0 * weight) / (48.8 + 53.8 * std::f32::consts::E.powf(-0.075 * reps))
}

/// Compute the 1 rep max as a function of the weight and reps columns
///
/// # Arguments
/// 
/// * `df` - The DataFrame with the raw set logs. Must contain the columns `weight` and `reps`, both
/// with type `Float32`.
/// 
/// * `formula` - The formula to use for the 1 rep max calculation. 
pub fn orm(df: DataFrame, formula: Formula) -> Result<DataFrame, PolarsError> {
    let weight = df.column("weight").unwrap().f32().unwrap();
    let reps = df.column("reps").unwrap().f32().unwrap();
    let orm = match formula {
        Formula::Brzycki => brzycki(weight, reps),
        Formula::Epley => epley(weight, reps),
        Formula::Lander => lander(weight, reps),
        Formula::Lombardi => lombardi(weight, reps),
        Formula::Mayhew => mayhew(weight, reps),
        Formula::OConner => oconner(weight, reps),
        Formula::Wathan => wathan(weight, reps),
    };
    let mut df = df.clone();
    df.add_column("orm", orm)?;
    Ok(df)
}