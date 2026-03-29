use criterion::{criterion_group, criterion_main, Criterion};
use mesh_gen_research::core::SdfField;
use mesh_gen_research::algorithms::MarchingCubes;
use mesh_gen_research::core::algorithm::IsosurfaceExtractor;

fn bench_marching_cubes(c: &mut Criterion) {
    let extractor = MarchingCubes::new();
    let mut group = c.benchmark_group("marching_cubes");

    for &size in &[16, 32, 48] {
        let sdf = SdfField::generate_sphere([0.0; 3], 0.5);
        
        group.bench_function(format!("sphere_{}x{}x{}", size, size, size), |b| {
            b.iter(|| {
                extractor.extract(&sdf, 0.0)
            })
        });
    }
    group.finish();
}

criterion_group!(benches, bench_marching_cubes);
criterion_main!(benches);