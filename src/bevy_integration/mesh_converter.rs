// ✅ mesh_converter.rs — фикс за 1 минуту
use bevy::asset::{RenderAssetUsages};
use bevy::prelude::*;
use bevy::mesh::{Indices, PrimitiveTopology};
use crate::core::MeshData;
use glam::Vec3;  // ← если ещё не импортирован

pub struct MeshConverter;

impl MeshConverter {
    pub fn to_bevy_mesh(data: MeshData) -> Mesh {
        // Конвертируем Vec3 → [f32; 3] для совместимости с Bevy
        let positions: Vec<[f32; 3]> = data.positions.iter()
            .map(|v: &Vec3| v.to_array())  // glam::Vec3 → [f32; 3]
            .collect();
        
        let normals: Vec<[f32; 3]> = data.normals.iter()
            .map(|v: &Vec3| v.to_array())
            .collect();

        Mesh::new(PrimitiveTopology::TriangleList, RenderAssetUsages::MAIN_WORLD | RenderAssetUsages::RENDER_WORLD)
            .with_inserted_attribute(Mesh::ATTRIBUTE_POSITION, positions)
            .with_inserted_attribute(Mesh::ATTRIBUTE_NORMAL, normals)
            .with_inserted_indices(Indices::U32(data.indices))
    }
}