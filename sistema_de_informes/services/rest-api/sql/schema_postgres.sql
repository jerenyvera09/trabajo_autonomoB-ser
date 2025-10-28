-- Schema PostgreSQL - Semana 6 (REST API)
-- Ejecutar en Supabase/PostgreSQL antes de iniciar la API si se usa DATABASE_URL de PG
create table if not exists roles (
    id_rol serial primary key,
    nombre_rol varchar not null,
    descripcion varchar null,
    permisos text null
);
create table if not exists usuarios (
    id_usuario serial primary key,
    nombre varchar not null,
    email varchar not null unique,
    password_hash varchar not null,
    estado varchar default 'ACTIVO',
    id_rol integer null references roles(id_rol)
);
create table if not exists categorias (
    id_categoria serial primary key,
    nombre varchar not null,
    descripcion text null,
    prioridad varchar null,
    estado varchar default 'ACTIVO'
);
create table if not exists areas (
    id_area serial primary key,
    nombre_area varchar not null,
    responsable varchar null,
    ubicacion varchar null,
    descripcion text null
);
create table if not exists estados_reporte (
    id_estado serial primary key,
    nombre varchar not null,
    descripcion text null,
    color varchar null,
    orden integer null,
    es_final boolean default false
);
create table if not exists reportes (
    id_reporte serial primary key,
    id_usuario integer not null references usuarios(id_usuario),
    titulo varchar not null,
    descripcion text null,
    ubicacion varchar null,
    id_categoria integer null references categorias(id_categoria),
    id_area integer null references areas(id_area),
    id_estado integer null references estados_reporte(id_estado),
    creado_en timestamp without time zone default now()
);
create table if not exists archivos_adjuntos (
    id_archivo serial primary key,
    id_reporte integer not null references reportes(id_reporte) on delete cascade,
    nombre_archivo varchar not null,
    tipo varchar null,
    url varchar not null
);
create table if not exists comentarios (
    id_comentario serial primary key,
    id_usuario integer not null references usuarios(id_usuario),
    id_reporte integer not null references reportes(id_reporte) on delete cascade,
    contenido text not null,
    fecha timestamp without time zone default now()
);
create table if not exists puntuaciones (
    id_puntuacion serial primary key,
    id_usuario integer not null references usuarios(id_usuario),
    id_reporte integer not null references reportes(id_reporte) on delete cascade,
    valor integer not null check (
        valor between 1 and 5
    ),
    fecha timestamp without time zone default now()
);
create table if not exists etiquetas (
    id_etiqueta serial primary key,
    nombre varchar not null,
    color varchar null
);
-- Indexes útiles
create index if not exists idx_reportes_usuario on reportes(id_usuario);
create index if not exists idx_reportes_estado on reportes(id_estado);
create index if not exists idx_puntuaciones_reporte on puntuaciones(id_reporte);