CREATE DATABASE IF NOT EXISTS agrologic
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE agrologic;

CREATE TABLE IF NOT EXISTS bois (
    id INT AUTO_INCREMENT PRIMARY KEY,
    raca VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    peso_kg FLOAT NOT NULL,
    idade_meses INT NOT NULL,
    valor_arroba FLOAT NOT NULL,
    preco_estimado FLOAT NOT NULL,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO bois (raca, categoria, peso_kg, idade_meses, valor_arroba, preco_estimado) VALUES
('Nelore', 'Boi Gordo', 480, 36, 300.00, 9600.00),
('Angus', 'Garrote', 320, 18, 310.00, 6613.33);
