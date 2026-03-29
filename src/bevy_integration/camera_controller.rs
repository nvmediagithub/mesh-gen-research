//! Контроллер орбитальной камеры (вращение + зум)

use bevy::prelude::*;
use bevy::input::mouse::{AccumulatedMouseMotion, AccumulatedMouseScroll, MouseScrollUnit};

/// Компонент для сущности камеры, позволяющий вращать её вокруг цели
#[derive(Component)]
pub struct OrbitCamera {
    /// Фокус вращения (точка, вокруг которой вращаемся)
    pub focus: Vec3,
    /// Радиус (расстояние от фокуса до камеры)
    pub radius: f32,
    /// Минимальный радиус зума
    pub min_radius: f32,
    /// Максимальный радиус зума
    pub max_radius: f32,
    /// Скорость вращения
    pub sensitivity: Vec2,
    /// Скорость зума
    pub zoom_sensitivity: f32,
    /// Текущие углы (yaw, pitch) в радианах
    pub yaw: f32,
    pub pitch: f32,
}

impl Default for OrbitCamera {
    fn default() -> Self {
        Self {
            focus: Vec3::ZERO,
            radius: 5.0,
            min_radius: 0.5,
            max_radius: 50.0,
            sensitivity: Vec2::new(0.005, 0.005),
            zoom_sensitivity: 0.05,
            yaw: std::f32::consts::FRAC_PI_4, // 45°
            pitch: std::f32::consts::FRAC_PI_4, // 30° (выше горизонта)
        }
    }
}

impl OrbitCamera {
    pub fn new(focus: Vec3, radius: f32) -> Self {
        Self {
            focus,
            radius,
            ..default()
        }
    }

    /// Вычисляет позицию камеры из сферических координат
    pub fn calculate_position(&self) -> Vec3 {
        let x = self.radius * self.pitch.cos() * self.yaw.sin();
        let y = self.radius * self.pitch.sin();
        let z = self.radius * self.pitch.cos() * self.yaw.cos();
        self.focus + Vec3::new(x, y, z)
    }

    /// Обновляет Transform камеры
    pub fn update_transform(&self, transform: &mut Transform) {
        transform.translation = self.calculate_position();
        transform.look_at(self.focus, Vec3::Y);
    }
}

/// Система управления камерой
pub fn orbit_camera_controller(
    mut query: Query<(&mut OrbitCamera, &mut Transform)>,
    mouse_button: Res<ButtonInput<MouseButton>>,
    mouse_motion: Res<AccumulatedMouseMotion>,
    mouse_scroll: Res<AccumulatedMouseScroll>, // ← EventReader → MessageReader
    time: Res<Time>,
) {
    let delta = mouse_motion.delta;  // Vec2
    // Извлекаем Vec2 из enum MouseScrollUnit
    let scroll_delta = mouse_scroll.delta; 

    for (mut orbit, mut transform) in query.iter_mut() {
        // Вращение (ЛКМ + движение мыши)
        if mouse_button.pressed(MouseButton::Left) {
            orbit.yaw -= delta.x * orbit.sensitivity.x;
            orbit.pitch -= delta.y * orbit.sensitivity.y;

            // Ограничение питча (чтобы камера не переворачивалась)
            let max_pitch = std::f32::consts::FRAC_PI_2 - 0.1; // ~1.47 радиан (85°)
            orbit.pitch = orbit.pitch.clamp(-max_pitch, max_pitch);
        }

        // Зум (колесо мыши)
        if scroll_delta.y != 0.0 {
            orbit.radius -= scroll_delta.y * orbit.zoom_sensitivity * orbit.radius;
            orbit.radius = orbit.radius.clamp(orbit.min_radius, orbit.max_radius);
        }

        // Применяем новую позицию
        orbit.update_transform(&mut transform);
    }

}