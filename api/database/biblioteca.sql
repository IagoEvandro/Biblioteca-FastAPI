CREATE DATABASE IF NOT EXISTS biblioteca_api
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE biblioteca_api;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash CHAR(64) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS generos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(80) NOT NULL UNIQUE,
    disponivel BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(120) NOT NULL UNIQUE,
    data_publicacao DATE NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_livros_preco CHECK (preco >= 0),
    CONSTRAINT chk_livros_data CHECK (data_publicacao <= CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS enderecos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    logradouro VARCHAR(150) NOT NULL,
    numero INT NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    cep CHAR(8) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_enderecos_cep CHECK (cep REGEXP '^[0-9]{8}$')
);

INSERT IGNORE INTO generos (nome, disponivel) VALUES
('romance', TRUE),
('terror', TRUE),
('aventura', TRUE),
('comedia', FALSE),
('suspense', FALSE),
('drama', FALSE);
