CREATE DATABASE IF NOT EXISTS agrologic
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE agrologic;

CREATE TABLE IF NOT EXISTS bois (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    raca VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    peso_kg FLOAT NOT NULL,
    idade_meses INT NOT NULL,
    valor_arroba FLOAT NOT NULL,
    preco_estimado FLOAT NOT NULL,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO bois (nome, raca, categoria, peso_kg, idade_meses, valor_arroba, preco_estimado) VALUES
('Boi 01', 'Nelore', 'Boi Gordo', 480, 36, 300.00, 9600.00),
('Boi 02', 'Angus', 'Garrote', 320, 18, 310.00, 6613.33);
