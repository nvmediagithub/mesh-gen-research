//! ECS системы

use bevy::prelude::*;
use crate::core::algorithm::IsosurfaceExtractor;
use crate::algorithms::MarchingCubes;
use crate::bevy_integration::{MeshConverter, VoxelField, GeneratedMesh, AlgorithmSelector};

/// Система генерации меша
pub fn generate_mesh_system(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    query: Query<(Entity, &VoxelField), Or<(Without<GeneratedMesh>, Changed<VoxelField>)>>,
) {
    let extractor = MarchingCubes::new();

    for (entity, voxel_field) in query.iter() {
        if !voxel_field.dirty {
            continue;
        }

        let mesh_data = extractor.extract(&voxel_field.sdf, voxel_field.iso_level);
        let bevy_mesh = MeshConverter::to_bevy_mesh(mesh_data.clone());
        let triangle_count = mesh_data.triangle_count();

        // Обновляем или создаём меш
        commands.entity(entity).insert((
            Mesh3d(meshes.add(bevy_mesh)),
            MeshMaterial3d(materials.add(StandardMaterial {
                base_color: Color::srgb(0.2, 0.6, 0.9),
                ..default()
            })),
            GeneratedMesh {
                algorithm_name: extractor.name().to_string(),
                triangle_count,
            },
        ));

        info!(
            "Generated mesh: {} triangles ({})",
            triangle_count,
            extractor.name()
        );
    }
}

/// Система для отладки - вывод статистики
pub fn debug_mesh_system(
    query: Query<&GeneratedMesh>,
    _selector: Option<Res<AlgorithmSelector>>,
) {
    for mesh in query.iter() {
        debug!(
            "Mesh: {} - {} triangles",
            mesh.algorithm_name, mesh.triangle_count
        );
    }
}