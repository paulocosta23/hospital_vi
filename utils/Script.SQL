-- Criar banco
CREATE DATABASE hospital_db;
USE hospital_db;

-- =========================
-- Plano
-- =========================
CREATE TABLE Plano (
    id_plano INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    PRIMARY KEY (id_plano)
) ENGINE=InnoDB;

-- =========================
-- Consultorio
-- =========================
CREATE TABLE Consultorio (
    id_consultorio INT AUTO_INCREMENT,
    numero INT NOT NULL,
    andar INT,
    bloco VARCHAR(10),
    PRIMARY KEY (id_consultorio)
) ENGINE=InnoDB;

-- =========================
-- Ala
-- =========================
CREATE TABLE Ala (
    id_ala INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    PRIMARY KEY (id_ala)
) ENGINE=InnoDB;

-- =========================
-- Procedimento
-- =========================
CREATE TABLE Procedimento (
    id_procedimento INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_procedimento)
) ENGINE=InnoDB;

-- =========================
-- Paciente
-- =========================
CREATE TABLE Paciente (
    id_paciente INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    endereco VARCHAR(200),
    cpf VARCHAR(14) UNIQUE,
    telefone VARCHAR(20),
    id_plano INT,
    PRIMARY KEY (id_paciente),

    CONSTRAINT fk_paciente_plano
    FOREIGN KEY (id_plano)
    REFERENCES Plano(id_plano)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- Medico
-- =========================
CREATE TABLE Medico (
    id_medico INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100),
    crm VARCHAR(20) UNIQUE,
    id_consultorio INT NOT NULL,
    PRIMARY KEY (id_medico),

    CONSTRAINT fk_medico_consultorio
    FOREIGN KEY (id_consultorio)
    REFERENCES Consultorio(id_consultorio)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- Enfermeira
-- =========================
CREATE TABLE Enfermeira (
    id_enfermeira INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cre VARCHAR(20) UNIQUE,
    id_ala INT NOT NULL,
    PRIMARY KEY (id_enfermeira),

    CONSTRAINT fk_enfermeira_ala
    FOREIGN KEY (id_ala)
    REFERENCES Ala(id_ala)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB;

-- =========================
-- Consulta
-- =========================
CREATE TABLE Consulta (
    id_consulta INT AUTO_INCREMENT,
    data DATE NOT NULL,
    tipo_atendimento ENUM('plano', 'particular') NOT NULL,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    PRIMARY KEY (id_consulta),

    CONSTRAINT fk_consulta_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES Paciente(id_paciente)
    ON DELETE CASCADE,

    CONSTRAINT fk_consulta_medico
    FOREIGN KEY (id_medico)
    REFERENCES Medico(id_medico)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- =========================
-- Paciente_Procedimento
-- =========================
CREATE TABLE Paciente_Procedimento (
    id INT AUTO_INCREMENT,
    data DATE NOT NULL,
    id_paciente INT NOT NULL,
    id_procedimento INT NOT NULL,
    PRIMARY KEY (id),

    CONSTRAINT fk_pp_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES Paciente(id_paciente)
    ON DELETE CASCADE,

    CONSTRAINT fk_pp_procedimento
    FOREIGN KEY (id_procedimento)
    REFERENCES Procedimento(id_procedimento)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- =========================
-- Internacao
-- =========================
CREATE TABLE Internacao (
    id_internacao INT AUTO_INCREMENT,
    data_entrada DATE NOT NULL,
    data_saida DATE,
    id_paciente INT NOT NULL,
    id_ala INT NOT NULL,
    PRIMARY KEY (id_internacao),

    CONSTRAINT fk_internacao_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES Paciente(id_paciente)
    ON DELETE CASCADE,

    CONSTRAINT fk_internacao_ala
    FOREIGN KEY (id_ala)
    REFERENCES Ala(id_ala)
    ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('atendente', 'medico', 'admin') NOT NULL
) ENGINE=InnoDB;

INSERT INTO Usuario (username, senha, tipo) VALUES
('atendente1', '123', 'atendente'),
('medico1', '123', 'medico'),
('admin', '123', 'admin');
