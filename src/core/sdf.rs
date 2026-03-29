//! Поле знаковых расстояний (Signed Distance Field)

#[derive(Debug, Clone)]
pub struct SdfField {
    pub data: Vec<f32>,
    pub resolution: [usize; 3],
    pub size: [f32; 3],
}

impl SdfField {
    pub fn new(resolution: [usize; 3], size: [f32; 3]) -> Self {
        let total = resolution[0] * resolution[1] * resolution[2];
        Self {
            data: vec![0.0; total],
            resolution,
            size,
        }
    }

    #[inline]
    pub fn index(&self, x: usize, y: usize, z: usize) -> usize {
        x + y * self.resolution[0] + z * self.resolution[0] * self.resolution[1]
    }

    #[inline]
    pub fn get(&self, x: usize, y: usize, z: usize) -> f32 {
        if x >= self.resolution[0] || y >= self.resolution[1] || z >= self.resolution[2] {
            return f32::MAX;
        }
        self.data[self.index(x, y, z)]
    }

    #[inline]
    pub fn set(&mut self, x: usize, y: usize, z: usize, value: f32) {
        if x < self.resolution[0] && y < self.resolution[1] && z < self.resolution[2] {
            // Сначала вычисляем индекс, чтобы избежать конфликта борров
            let idx = self.index(x, y, z);
            self.data[idx] = value;
        }
    }

    /// Генерация SDF сферы
    pub fn generate_sphere(center: [f32; 3], radius: f32) -> Self {
        let resolution = [32, 32, 32];
        let size = [2.0, 2.0, 2.0];
        let mut field = Self::new(resolution, size);

        let step = [
            size[0] / resolution[0] as f32,
            size[1] / resolution[1] as f32,
            size[2] / resolution[2] as f32,
        ];

        for z in 0..resolution[2] {
            for y in 0..resolution[1] {
                for x in 0..resolution[0] {
                    let px = x as f32 * step[0] - size[0] / 2.0;
                    let py = y as f32 * step[1] - size[1] / 2.0;
                    let pz = z as f32 * step[2] - size[2] / 2.0;

                    let dx = px - center[0];
                    let dy = py - center[1];
                    let dz = pz - center[2];
                    let dist = (dx * dx + dy * dy + dz * dz).sqrt() - radius;

                    field.set(x, y, z, dist);
                }
            }
        }
        field
    }

    /// Генерация SDF куба
    pub fn generate_cube(half_size: f32) -> Self {
        let resolution = [32, 32, 32];
        let size = [2.0, 2.0, 2.0];
        let mut field = Self::new(resolution, size);

        let step = [
            size[0] / resolution[0] as f32,
            size[1] / resolution[1] as f32,
            size[2] / resolution[2] as f32,
        ];

        for z in 0..resolution[2] {
            for y in 0..resolution[1] {
                for x in 0..resolution[0] {
                    let px = x as f32 * step[0] - size[0] / 2.0;
                    let py = y as f32 * step[1] - size[1] / 2.0;
                    let pz = z as f32 * step[2] - size[2] / 2.0;

                    let qx = px.abs() - half_size;
                    let qy = py.abs() - half_size;
                    let qz = pz.abs() - half_size;

                    let ax = qx.max(0.0);
                    let ay = qy.max(0.0);
                    let az = qz.max(0.0);
                    let dist = (ax * ax + ay * ay + az * az).sqrt()
                        + qx.min(0.0).max(qy.min(0.0).max(qz.min(0.0)));

                    field.set(x, y, z, dist);
                }
            }
        }
        field
    }
}