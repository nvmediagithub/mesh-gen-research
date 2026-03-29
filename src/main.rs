//! Mesh Generation Research - Milestone 1
//! Исследование алгоритмов генерации изосурфейсов

use bevy::prelude::*;

mod core;
mod algorithms;
mod bevy_integration;

use bevy_integration::{generate_mesh_system, VoxelField, OrbitCamera, orbit_camera_controller};

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                title: "Mesh Gen Research - M1".into(),
                resolution: (1280u32, 720u32).into(),
                ..default()
            }),
            ..default()
        }))
        .add_systems(Startup, setup_scene)
        .add_systems(Update, (generate_mesh_system, orbit_camera_controller))
        .run();
}

fn setup_scene(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    // Камера с орбитальным контроллером
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(3.0, 3.0, 3.0).looking_at(Vec3::ZERO, Vec3::Y),
        OrbitCamera::new(Vec3::ZERO, 5.0), // <-- Добавлено
    ));

    // Свет
    commands.spawn((
        PointLight::default(),
        Transform::from_xyz(4.0, 8.0, 4.0),
    ));

    // Сфера для генерации
    commands.spawn((
        VoxelField::default(),
        Transform::default(),
    ));

    // Пол для ориентира
    commands.spawn((
        Mesh3d(meshes.add(Plane3d::default().mesh().size(10.0, 10.0))),
        MeshMaterial3d(materials.add(StandardMaterial {
            base_color: Color::srgb(0.3, 0.3, 0.3),
            ..default()
        })),
        Transform::from_xyz(0.0, -2.0, 0.0),
    ));

    info!("🦀 M1: Basic infrastructure ready!");
}