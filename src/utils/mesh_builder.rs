use bevy::prelude::*;
use bevy::mesh::{Indices, VertexAttributeValues};
use bevy::render::render_resource::PrimitiveTopology;

pub struct CustomMeshBuilder {
    positions: Vec<[f32; 3]>,
    normals: Vec<[f32; 3]>,
    uvs: Vec<[f32; 2]>,
    indices: Vec<u32>,
}

impl CustomMeshBuilder {
    pub fn new() -> Self {
        Self {
            positions: Vec::new(),
            normals: Vec::new(),
            uvs: Vec::new(),
            indices: Vec::new(),
        }
    }

    pub fn with_triangle(&mut self, v0: [f32;3], v1: [f32;3], v2: [f32;3], 
                         n0: [f32;3], n1: [f32;3], n2: [f32;3]) -> &mut Self {
        let base = self.positions.len() as u32;
        self.positions.extend([v0, v1, v2]);
        self.normals.extend([n0, n1, n2]);
        self.uvs.extend([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]]);
        self.indices.extend([base, base + 1, base + 2]);
        self
    }

    pub fn build(self) -> Mesh {
        Mesh::new(PrimitiveTopology::TriangleList, 
                 bevy::asset::RenderAssetUsages::MAIN_WORLD | bevy::asset::RenderAssetUsages::RENDER_WORLD)
            .with_inserted_attribute(Mesh::ATTRIBUTE_POSITION, self.positions)
            .with_inserted_attribute(Mesh::ATTRIBUTE_NORMAL, self.normals)
            .with_inserted_attribute(Mesh::ATTRIBUTE_UV_0, self.uvs)
            .with_inserted_indices(Indices::U32(self.indices))
    }
}