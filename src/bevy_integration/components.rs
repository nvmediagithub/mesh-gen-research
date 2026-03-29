//! ECS компоненты

use bevy::prelude::*;
use crate::core::SdfField;

/// Маркер для сущности с генерируемым мешем
#[derive(Component, Default)]
pub struct GeneratedMesh {
    pub algorithm_name: String,
    pub triangle_count: usize,
}

/// Компонент для хранения SDF поля
#[derive(Component)]
pub struct VoxelField {
    pub sdf: SdfField,
    pub iso_level: f32,
    pub dirty: bool,
}

impl Default for VoxelField {
    fn default() -> Self {
        Self {
            sdf: SdfField::generate_sphere([0.0; 3], 0.5),
            iso_level: 0.0,
            dirty: true,
        }
    }
}

/// Ресурс для выбора алгоритма
#[derive(Resource, Default)]
pub struct AlgorithmSelector {
    pub current: usize,
    pub names: Vec<String>,
}