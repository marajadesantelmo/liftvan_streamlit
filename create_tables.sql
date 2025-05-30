CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    username TEXT,
    nombre_apellido TEXT,
    puesto TEXT,
    asistencia_estimador INTEGER CHECK (asistencia_estimador BETWEEN 1 AND 5),
    cortesia_coordinador INTEGER CHECK (cortesia_coordinador BETWEEN 1 AND 5),
    apoyo_coordinador INTEGER CHECK (apoyo_coordinador BETWEEN 1 AND 5),
    precision_informacion INTEGER CHECK (precision_informacion BETWEEN 1 AND 5),
    servicio_general_coordinador INTEGER CHECK (servicio_general_coordinador BETWEEN 1 AND 5),
    cortesia INTEGER CHECK (cortesia BETWEEN 1 AND 5),
    colaboracion_personal INTEGER CHECK (colaboracion_personal BETWEEN 1 AND 5),
    puntualidad INTEGER CHECK (puntualidad BETWEEN 1 AND 5),
    calidad_empaque INTEGER CHECK (calidad_empaque BETWEEN 1 AND 5),
    recomendaria BOOLEAN,
    comentarios TEXT,
    created_at TIMESTAMP DEFAULT now()
);