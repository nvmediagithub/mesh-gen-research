/// Простые функции подписанного расстояния для тестов
use bevy::prelude::*;

/// Сфера
pub fn sphere(x: f32, y: f32, z: f32, cx: f32, cy: f32, cz: f32, r: f32) -> f32 {
    let dx = x - cx;
    let dy = y - cy;
    let dz = z - cz;
    (dx*dx + dy*dy + dz*dz).sqrt() - r
}

/// Box (AABB)
pub fn box_sdf(x: f32, y: f32, z: f32, half_size: f32) -> f32 {
    let qx = x.abs() - half_size;
    let qy = y.abs() - half_size;
    let qz = z.abs() - half_size;
    let e = Vec3::new(qx.max(0.0), qy.max(0.0), qz.max(0.0));
    e.length() + qx.min(0.0).max(qy.min(0.0).max(qz.min(0.0)))
}