//! Тесты корректности генерации

use mesh_gen_research::core::{SdfField, MeshData};
use mesh_gen_research::algorithms::MarchingCubes;

#[test]
fn test_sphere_generation() {
    let sdf = SdfField::generate_sphere([0.0; 3], 0.5);
    let extractor = MarchingCubes::new();
    let mesh = extractor.extract(&sdf, 0.0);

    assert!(mesh.triangle_count() > 0, "Sphere should have triangles");
    assert!(mesh.vertex_count() > 0, "Sphere should have vertices");
    println!("Sphere: {} triangles, {} vertices", 
             mesh.triangle_count(), mesh.vertex_count());
}

#[test]
fn test_cube_generation() {
    let sdf = SdfField::generate_cube(0.5);
    let extractor = MarchingCubes::new();
    let mesh = extractor.extract(&sdf, 0.0);

    assert!(mesh.triangle_count() > 0, "Cube should have triangles");
    println!("Cube: {} triangles, {} vertices", 
             mesh.triangle_count(), mesh.vertex_count());
}

#[test]
fn test_mesh_data_integrity() {
    let mut mesh = MeshData::new();
    mesh.add_triangle(
        [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0],
    );

    assert_eq!(mesh.vertex_count(), 3);
    assert_eq!(mesh.triangle_count(), 1);
}