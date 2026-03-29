//! Структура для хранения данных меша (агностичная от рендерера)

#[derive(Debug, Clone)]
pub struct MeshData {
    pub positions: Vec<[f32; 3]>,
    pub normals: Vec<[f32; 3]>,
    pub indices: Vec<u32>,
}

impl MeshData {
    pub fn new() -> Self {
        Self {
            positions: Vec::new(),
            normals: Vec::new(),
            indices: Vec::new(),
        }
    }

    pub fn with_capacity(positions: usize, indices: usize) -> Self {
        Self {
            positions: Vec::with_capacity(positions),
            normals: Vec::with_capacity(positions),
            indices: Vec::with_capacity(indices),
        }
    }

    pub fn add_triangle(
        &mut self,
        v0: [f32; 3],
        v1: [f32; 3],
        v2: [f32; 3],
        n0: [f32; 3],
        n1: [f32; 3],
        n2: [f32; 3],
    ) {
        let base = self.positions.len() as u32;
        self.positions.extend([v0, v1, v2]);
        self.normals.extend([n0, n1, n2]);
        self.indices.extend([base, base + 1, base + 2]);
    }

    pub fn triangle_count(&self) -> usize {
        self.indices.len() / 3
    }

    pub fn vertex_count(&self) -> usize {
        self.positions.len()
    }
}

impl Default for MeshData {
    fn default() -> Self {
        Self::new()
    }
}