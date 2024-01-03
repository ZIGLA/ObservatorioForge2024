-- Crear la base de datos
CREATE DATABASE db_observatorio;
GO

-- Usar la base de datos reci�n creada
USE Observatorio;
GO

-- Crear la tabla "bumeran"
CREATE TABLE bumeran (
    link_bm             VARCHAR(900) PRIMARY KEY NOT NULL,
    id_publicacion      INT,
    id_empresa          INT,
    titulo              TEXT,
    empresa             TEXT,
    descripcion         TEXT,
    fecha_publ          TEXT,
    pais                TEXT,
    provincia           TEXT,
    localidad           TEXT,
    area                TEXT,
    subarea             TEXT,
    industria           TEXT,
    modalidad           TEXT,
    jornada             TEXT,
    nivel               TEXT,
    tipo_contrato       TEXT,
    puesto              TEXT,
    vacantes            INT,
    provincia_empr      TEXT,
    ciudad_empr         TEXT,
    descripcion_empr    TEXT,
    fecha_fin           TEXT,
    estado              TEXT,
    confidencial        BIT,
    cant_empleados      TEXT,
    plataforma_origen   TEXT,
    apto_disc           BIT,
    r_edad              TEXT,
    r_residencia        TEXT,
    r_experiencia       TEXT,
    r_genero            TEXT,
    r_educacion         TEXT,
    r_salario           TEXT,
    r_conocimientos     TEXT,
    r_idiomas           TEXT
);
GO

-- Crear la tabla "computrabajo"
CREATE TABLE computrabajo (
    link_ct             VARCHAR(900) PRIMARY KEY NOT NULL,
    link_empresa        TEXT,
    titulo              TEXT,
    empresa             TEXT,
    descripcion         TEXT,
    descripcion_empresa TEXT,
    requisitos          TEXT,
    tipo_contrato       TEXT,
    jornada             TEXT,
    salario             TEXT,
    pais                TEXT,
    provincia           TEXT,
    modalidad           TEXT,
    localidad           TEXT,
    fecha_publ          TEXT,
    rating              INT,
    cant_eval           INT,
    palabras_clave      TEXT,
    p_amb_trab          DECIMAL,
    p_sal_prest         DECIMAL,
    p_oport_carr        DECIMAL,
    p_direc_general     DECIMAL
);
GO

-- Crear la tabla "indeed"
CREATE TABLE indeed (
    link_in            VARCHAR(900) PRIMARY KEY NOT NULL,
    link_empresa        TEXT,
    titulo              TEXT,
    empresa             TEXT,
    descripcion         TEXT,
    pais                TEXT,
    provincia           TEXT,
    localidad              TEXT,
    salario             TEXT,
    tipo_contrato       TEXT,
    jornada             TEXT
);
GO

-- Crear la tabla "consolidado"
CREATE TABLE consolidado (
    link                VARCHAR(900) PRIMARY KEY NOT NULL,
    titulo              TEXT,
    empresa             TEXT,
    descripcion         TEXT,
    link_empresa        TEXT,
    pais                TEXT,
    provincia           TEXT,
    localidad           TEXT,
    jornada             TEXT,
    tipo_contrato       TEXT,
    salario        TEXT,
    
    -- Claves for�neas
    FOREIGN KEY (link) REFERENCES bumeran(link_bm),
    FOREIGN KEY (link) REFERENCES computrabajo(link_ct),
    FOREIGN KEY (link) REFERENCES indeed(link_in)
);
GO

