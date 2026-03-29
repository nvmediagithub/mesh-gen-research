//! Конвертация MeshData в bevy::Mesh
use bevy::asset::{RenderAssetUsages};
use bevy::prelude::*;
use bevy::mesh::{Indices, PrimitiveTopology};
use crate::core::MeshData;

pub struct MeshConverter;

impl MeshConverter {
    pub fn to_bevy_mesh(data: MeshData) -> Mesh {
        Mesh::new(PrimitiveTopology::TriangleList, RenderAssetUsages::MAIN_WORLD | RenderAssetUsages::RENDER_WORLD)
            .with_inserted_attribute(Mesh::ATTRIBUTE_POSITION, data.positions)
            .with_inserted_attribute(Mesh::ATTRIBUTE_NORMAL, data.normals)
            .with_inserted_indices(Indices::U32(data.indices))
    }
}