//! Ядро проекта - без зависимостей от Bevy

pub mod mesh_data;
pub mod algorithm;
pub mod sdf;

pub use mesh_data::MeshData;
pub use algorithm::IsosurfaceExtractor;
pub use sdf::SdfField;