# LLM CONTEXT FOR PROJECT

**Project Root:** `C:\Repositories\mesh-gen-research`

---

## 📁 PROJECT STRUCTURE

================================================================================
PROJECT STRUCTURE FOR LLM
Root: C:\Repositories\mesh-gen-research
================================================================================

📁 DIRECTORY STRUCTURE:
--------------------------------------------------------------------------------
📁 mesh-gen-research/
├── │   📁 benches/
│   ├── │   │   📄 algorithm_compare.rs (761.0B)
│   └── │       📄 mesh_generation.rs (1.3KB)
├── │   📁 scripts/
│   ├── │   │   📄 extract_rust_docs.py (20.8KB)
│   ├── │   │   📄 generate_llm_context.py (2.6KB)
│   └── │       📄 generate_project_structure.py (9.3KB)
├── │   📁 src/
│   ├── │   │   📁 algorithms/
│   │   ├── │   │   │   📄 marching_cubes.rs (24.9KB)
│   │   └── │   │       📄 mod.rs (803.0B)
│   ├── │   │   📁 bevy_integration/
│   │   ├── │   │   │   📄 camera_controller.rs (3.6KB)
│   │   ├── │   │   │   📄 components.rs (866.0B)
│   │   ├── │   │   │   📄 mesh_converter.rs (1.1KB)
│   │   ├── │   │   │   📄 mod.rs (308.0B)
│   │   └── │   │       📄 systems.rs (1.8KB)
│   ├── │   │   📁 core/
│   │   ├── │   │   │   📄 algorithm.rs (615.0B)
│   │   ├── │   │   │   📄 mesh_data.rs (1.3KB)
│   │   ├── │   │   │   📄 mod.rs (224.0B)
│   │   └── │   │       📄 sdf.rs (3.6KB)
│   ├── │   │   📁 utils/
│   │   ├── │   │   │   📄 mesh_builder.rs (1.4KB)
│   │   ├── │   │   │   📄 mod.rs (35.0B)
│   │   └── │   │       📄 sdf.rs (650.0B)
│   └── │       📄 main.rs (1.8KB)
├── │   📁 tests/
│   └── │       📄 correctness.rs (1.3KB)
├── │   📄 Cargo.toml (1.1KB)
├── │   📄 PROJECT_STRUCTURE.txt (2.8KB)
└── 📄 RUST_DOCS.md (12.3KB)


================================================================================
END OF PROJECT STRUCTURE
================================================================================


---

## 🦀 RUST CODE DOCUMENTATION

🔍 Found 18 Rust files
  ✅ benches\algorithm_compare.rs: 1 items
  ✅ benches\mesh_generation.rs: 2 items
  ✅ src\algorithms\marching_cubes.rs: 16 items
  ✅ src\algorithms\mod.rs: 4 items
  ✅ src\bevy_integration\camera_controller.rs: 7 items
  ✅ src\bevy_integration\components.rs: 5 items
  ✅ src\bevy_integration\mesh_converter.rs: 2 items
  ✅ src\bevy_integration\mod.rs: 0 items
  ✅ src\bevy_integration\systems.rs: 0 items
  ✅ src\core\algorithm.rs: 2 items
  ✅ src\core\mesh_data.rs: 8 items
  ✅ src\core\mod.rs: 0 items
  ✅ src\core\sdf.rs: 8 items
  ✅ src\main.rs: 1 items
  ✅ src\utils\mesh_builder.rs: 4 items
  ✅ src\utils\mod.rs: 0 items
  ✅ src\utils\sdf.rs: 2 items
  ✅ tests\correctness.rs: 3 items

📊 Total: 65 items extracted
# Rust Code Documentation

**Root:** `C:\Repositories\mesh-gen-research`

**Total Items:** 65



## 📄 benches\algorithm_compare.rs


### Function: `bench_marching_cubes` 🔒 `private`

**Location:** `benches\algorithm_compare.rs:5`


```rust
fn bench_marching_cubes(c: &mut Criterion)
```


## 📄 benches\mesh_generation.rs


### Function: `bench_marching_cubes` 🔒 `private`

**Location:** `benches\mesh_generation.rs:4`


```rust
fn bench_marching_cubes(c: &mut Criterion)
```


### Function: `generate_test_sdf` 🔒 `private`

**Location:** `benches\mesh_generation.rs:18`


```rust
fn generate_test_sdf(x: usize, y: usize, z: usize) -> Vec<f32>
```


## 📄 src\algorithms\marching_cubes.rs


### Function: `new` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:339`


```rust
fn new(p0: Vertex, p1: Vertex, p2: Vertex) -> Self
```


### Function: `vertex_interp` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:346`


```rust
fn vertex_interp(isolevel: f32, p1: Vec3, p2: Vec3, val1: f32, val2: f32) -> Vec3
```


**Documentation:**

> Линейная интерполяция точки пересечения изоповерхности с ребром


### Function: `new` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:363`


```rust
fn new() -> Self
```


### Function: `with_parallel` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:366`


```rust
fn with_parallel(use_parallel: bool) -> Self
```


### Function: `compute_normal` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:372`


```rust
fn compute_normal(sdf: &SdfField, x: usize, y: usize, z: usize) -> Vec3
```


**Documentation:**

> Вычисление нормали через центральные разности


### Function: `default` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:393`


```rust
fn default() -> Self
```


### Function: `name` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:399`


```rust
fn name(&self) -> &'static str
```


### Function: `extract` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:402`


```rust
fn extract(&self, sdf: &SdfField, iso_level: f32) -> MeshData
```


### Function: `supports_parallel` 🔒 `private`

**Location:** `src\algorithms\marching_cubes.rs:495`


```rust
fn supports_parallel(&self) -> bool
```


### Struct: `GridCell` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:324`


```rust
pub struct GridCell { /// Позиции 8 вершин куба pub p: [Vertex; 8], /// Скалярные значения в вершинах (например, SDF)
```


**Documentation:**

> Ячейка сетки: 8 вершин + 8 скалярных значений


### Struct: `Triangle` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:333`


```rust
pub struct Triangle { pub p: [Vertex; 3], } impl Triangle
```


**Documentation:**

> Треугольник из 3 вершин


### Struct: `MarchingCubes` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:358`


```rust
pub struct MarchingCubes { use_parallel: bool, } impl MarchingCubes
```


**Documentation:**

> Marching Cubes экстрактор


### Impl: `Triangle` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:336`


```rust
impl Triangle
```


### Impl: `MarchingCubes` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:361`


```rust
impl MarchingCubes
```


### Impl: `Default` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:391`


```rust
impl Default
```


### Impl: `IsosurfaceExtractor` 🌍 `pub`

**Location:** `src\algorithms\marching_cubes.rs:397`


```rust
impl IsosurfaceExtractor
```


## 📄 src\algorithms\mod.rs


### Function: `default` 🔒 `private`

**Location:** `src\algorithms\mod.rs:14`


```rust
fn default() -> Self
```


### Struct: `MeshData` 🌍 `pub`

**Location:** `src\algorithms\mod.rs:7`


```rust
pub struct MeshData { pub positions: Vec<[f32; 3]>, pub normals: Vec<[f32; 3]>, pub indices: Vec<u32>, } impl Default for MeshData
```


### Trait: `IsosurfaceExtractor` 🌍 `pub`

**Location:** `src\algorithms\mod.rs:2`


```rust
trait IsosurfaceExtractor
```


### Impl: `Default` 🌍 `pub`

**Location:** `src\algorithms\mod.rs:12`


```rust
impl Default
```


## 📄 src\bevy_integration\camera_controller.rs


### Function: `default` 🔒 `private`

**Location:** `src\bevy_integration\camera_controller.rs:27`


```rust
fn default() -> Self
```


### Function: `new` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:42`


```rust
fn new(focus: Vec3, radius: f32) -> Self
```


### Function: `calculate_position` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:51`


```rust
fn calculate_position(&self) -> Vec3
```


**Documentation:**

> Вычисляет позицию камеры из сферических координат


### Function: `update_transform` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:59`


```rust
fn update_transform(&self, transform: &mut Transform)
```


**Documentation:**

> Обновляет Transform камеры


### Struct: `OrbitCamera` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:8`


```rust
pub struct OrbitCamera { /// Фокус вращения (точка, вокруг которой вращаемся)
```


**Documentation:**

> Компонент для сущности камеры, позволяющий вращать её вокруг цели


### Impl: `Default` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:25`


```rust
impl Default
```


### Impl: `OrbitCamera` 🌍 `pub`

**Location:** `src\bevy_integration\camera_controller.rs:40`


```rust
impl OrbitCamera
```


## 📄 src\bevy_integration\components.rs


### Function: `default` 🔒 `private`

**Location:** `src\bevy_integration\components.rs:22`


```rust
fn default() -> Self
```


### Struct: `GeneratedMesh` 🌍 `pub`

**Location:** `src\bevy_integration\components.rs:8`


```rust
pub struct GeneratedMesh { pub algorithm_name: String, pub triangle_count: usize, } /// Компонент для хранения SDF поля #[derive(Component)
```


**Documentation:**

> Маркер для сущности с генерируемым мешем


### Struct: `VoxelField` 🌍 `pub`

**Location:** `src\bevy_integration\components.rs:15`


```rust
pub struct VoxelField { pub sdf: SdfField, pub iso_level: f32, pub dirty: bool, } impl Default for VoxelField
```


**Documentation:**

> Компонент для хранения SDF поля


### Struct: `AlgorithmSelector` 🌍 `pub`

**Location:** `src\bevy_integration\components.rs:33`


```rust
struct AlgorithmSelector
```


**Documentation:**

> Ресурс для выбора алгоритма


### Impl: `Default` 🌍 `pub`

**Location:** `src\bevy_integration\components.rs:20`


```rust
impl Default
```


## 📄 src\bevy_integration\mesh_converter.rs


### Function: `to_bevy_mesh` 🌍 `pub`

**Location:** `src\bevy_integration\mesh_converter.rs:11`


```rust
fn to_bevy_mesh(data: MeshData) -> Mesh
```


### Impl: `MeshConverter` 🌍 `pub`

**Location:** `src\bevy_integration\mesh_converter.rs:9`


```rust
impl MeshConverter
```


## 📄 src\core\algorithm.rs


### Function: `supports_parallel` 🔒 `private`

**Location:** `src\core\algorithm.rs:14`


```rust
fn supports_parallel(&self) -> bool
```


**Documentation:**

> Поддерживает ли параллельную генерацию


### Trait: `IsosurfaceExtractor` 🌍 `pub`

**Location:** `src\core\algorithm.rs:6`


```rust
trait IsosurfaceExtractor
```


**Documentation:**

> Трейт для экстракторов изосурфейсов


## 📄 src\core\mesh_data.rs


### Function: `new` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:12`


```rust
fn new() -> Self
```


### Function: `with_capacity` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:19`


```rust
fn with_capacity(positions: usize, indices: usize) -> Self
```


### Function: `triangle_count` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:42`


```rust
fn triangle_count(&self) -> usize
```


### Function: `vertex_count` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:46`


```rust
fn vertex_count(&self) -> usize
```


### Function: `default` 🔒 `private`

**Location:** `src\core\mesh_data.rs:53`


```rust
fn default() -> Self
```


### Struct: `MeshData` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:5`


```rust
pub struct MeshData { pub positions: Vec<Vec3>, pub normals: Vec<Vec3>, pub indices: Vec<u32>, } impl MeshData
```


### Impl: `MeshData` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:10`


```rust
impl MeshData
```


### Impl: `Default` 🌍 `pub`

**Location:** `src\core\mesh_data.rs:51`


```rust
impl Default
```


## 📄 src\core\sdf.rs


### Function: `new` 🌍 `pub`

**Location:** `src\core\sdf.rs:11`


```rust
fn new(resolution: [usize; 3], size: [f32; 3]) -> Self
```


### Function: `index` 🌍 `pub`

**Location:** `src\core\sdf.rs:21`


```rust
fn index(&self, x: usize, y: usize, z: usize) -> usize
```


### Function: `get` 🌍 `pub`

**Location:** `src\core\sdf.rs:26`


```rust
fn get(&self, x: usize, y: usize, z: usize) -> f32
```


### Function: `set` 🌍 `pub`

**Location:** `src\core\sdf.rs:34`


```rust
fn set(&mut self, x: usize, y: usize, z: usize, value: f32)
```


### Function: `generate_sphere` 🌍 `pub`

**Location:** `src\core\sdf.rs:43`


```rust
fn generate_sphere(center: [f32; 3], radius: f32) -> Self
```


**Documentation:**

> Генерация SDF сферы


### Function: `generate_cube` 🌍 `pub`

**Location:** `src\core\sdf.rs:74`


```rust
fn generate_cube(half_size: f32) -> Self
```


**Documentation:**

> Генерация SDF куба


### Struct: `SdfField` 🌍 `pub`

**Location:** `src\core\sdf.rs:4`


```rust
pub struct SdfField { pub data: Vec<f32>, pub resolution: [usize; 3], pub size: [f32; 3], } impl SdfField
```


**Documentation:**

> Поле знаковых расстояний (Signed Distance Field)


### Impl: `SdfField` 🌍 `pub`

**Location:** `src\core\sdf.rs:9`


```rust
impl SdfField
```


## 📄 src\main.rs


### Function: `main` 🔒 `private`

**Location:** `src\main.rs:11`


```rust
fn main()
```


## 📄 src\utils\mesh_builder.rs


### Function: `new` 🌍 `pub`

**Location:** `src\utils\mesh_builder.rs:13`


```rust
fn new() -> Self
```


### Function: `build` 🌍 `pub`

**Location:** `src\utils\mesh_builder.rs:31`


```rust
fn build(self) -> Mesh
```


### Struct: `CustomMeshBuilder` 🌍 `pub`

**Location:** `src\utils\mesh_builder.rs:4`


```rust
pub struct CustomMeshBuilder { positions: Vec<[f32; 3]>, normals: Vec<[f32; 3]>, uvs: Vec<[f32; 2]>, indices: Vec<u32>, } impl CustomMeshBuilder
```


### Impl: `CustomMeshBuilder` 🌍 `pub`

**Location:** `src\utils\mesh_builder.rs:11`


```rust
impl CustomMeshBuilder
```


## 📄 src\utils\sdf.rs


### Function: `sphere` 🌍 `pub`

**Location:** `src\utils\sdf.rs:5`


```rust
fn sphere(x: f32, y: f32, z: f32, cx: f32, cy: f32, cz: f32, r: f32) -> f32
```


**Documentation:**

> Сфера


### Function: `box_sdf` 🌍 `pub`

**Location:** `src\utils\sdf.rs:13`


```rust
fn box_sdf(x: f32, y: f32, z: f32, half_size: f32) -> f32
```


**Documentation:**

> Box (AABB)


## 📄 tests\correctness.rs


### Function: `test_sphere_generation` 🔒 `private`

**Location:** `tests\correctness.rs:7`


```rust
fn test_sphere_generation()
```


### Function: `test_cube_generation` 🔒 `private`

**Location:** `tests\correctness.rs:19`


```rust
fn test_cube_generation()
```


### Function: `test_mesh_data_integrity` 🔒 `private`

**Location:** `tests\correctness.rs:30`


```rust
fn test_mesh_data_integrity()
```

