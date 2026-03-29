// Общий трейт для всех алгоритмов генерации
pub trait IsosurfaceExtractor {
    fn extract(&self, sdf: &[f32], resolution: [usize; 3], iso: f32) -> MeshData;
}

#[derive(Debug, Clone)]
pub struct MeshData {
    pub positions: Vec<[f32; 3]>,
    pub normals: Vec<[f32; 3]>,
    pub indices: Vec<u32>,
}

impl Default for MeshData {
    fn default() -> Self {
        Self {
            positions: Vec::new(),
            normals: Vec::new(),
            indices: Vec::new(),
        }
    }
}


pub mod marching_cubes;
pub use marching_cubes::MarchingCubes;

// Заглушки для будущих реализаций
#[cfg(feature = "dual-contouring")]
pub mod dual_contouring;
#[cfg(feature = "surface-nets")]
pub mod surface_nets;