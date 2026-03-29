// benches/mesh_generation.rs
use criterion::{criterion_group, criterion_main, Criterion};
use mesh_gen_research::algorithms::marching_cubes::generate_mesh;

fn bench_marching_cubes(c: &mut Criterion) {
    let mut group = c.benchmark_group("marching_cubes");
    
    for &size in &[16, 32, 64] {
        group.bench_function(format!("resolution_{}x{}x{}", size, size, size), |b| {
            b.iter(|| {
                let sdf = generate_test_sdf(size, size, size);
                generate_mesh(&sdf, [size, size, size], 0.0);
            })
        });
    }
    group.finish();
}

fn generate_test_sdf(x: usize, y: usize, z: usize) -> Vec<f32> {
    // Простая сфера для тестов
    let mut data = Vec::with_capacity(x * y * z);
    let cx = x as f32 / 2.0;
    let cy = y as f32 / 2.0;
    let cz = z as f32 / 2.0;
    let radius = (x.min(y).min(z) as f32) / 3.0;
    
    for iz in 0..z {
        for iy in 0..y {
            for ix in 0..x {
                let dx = ix as f32 - cx;
                let dy = iy as f32 - cy;
                let dz = iz as f32 - cz;
                data.push((dx*dx + dy*dy + dz*dz).sqrt() - radius);
            }
        }
    }
    data
}

criterion_group!(benches, bench_marching_cubes);
criterion_main!(benches);