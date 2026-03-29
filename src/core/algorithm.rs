//! Общий трейт для всех алгоритмов изосурфейсинга

use crate::core::{MeshData, SdfField};

/// Трейт для экстракторов изосурфейсов
pub trait IsosurfaceExtractor: Send + Sync {
    /// Название алгоритма
    fn name(&self) -> &'static str;

    /// Извлечение меша из SDF поля
    fn extract(&self, sdf: &SdfField, iso_level: f32) -> MeshData;

    /// Поддерживает ли параллельную генерацию
    fn supports_parallel(&self) -> bool {
        true
    }
}