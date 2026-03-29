//! Интеграция с Bevy

pub mod mesh_converter;
pub mod components;
pub mod systems;
pub mod camera_controller;  // <-- Добавлено

pub use mesh_converter::MeshConverter;
pub use components::*;
pub use systems::*;
pub use camera_controller::{OrbitCamera, orbit_camera_controller};