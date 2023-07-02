CREATE DATABASE IF NOT EXISTS Oficina;
USE Oficina;

-- VEICULO
CREATE TABLE Veiculo (
    idVeiculo INT auto_increment PRIMARY KEY,
    idRevisão INT,
    Placa CHAR(7) NOT NULL,
    CONSTRAINT placa_idVeiculo UNIQUE (Placa)
);

ALTER TABLE Veiculo ADD CONSTRAINT fk_revisao FOREIGN KEY (idRevisão) REFERENCES Revisao(idRevisão);

-- CLIENTES
CREATE TABLE Clientes (
    idClientes INT auto_increment PRIMARY KEY,
    idVeiculo INT,
    CONSTRAINT fk_veiculo FOREIGN KEY (idVeiculo) REFERENCES Veiculo(idVeiculo)
);

-- PESSOA FISICA
CREATE TABLE PessoaFisica (
    idPessoaFisica INT auto_increment PRIMARY KEY,
    Nome VARCHAR(45) NOT NULL,
    CPF CHAR(11) NOT NULL,
    Endereço VARCHAR(45),
    Contato CHAR(11)
);

ALTER TABLE PessoaFisica ADD CONSTRAINT unique_cpf_PessoaFisica UNIQUE (CPF);

-- PESSOA JURIDICA
CREATE TABLE PessoaJuridica (
    idPessoaJuridica INT auto_increment PRIMARY KEY,
    RazaoSocial VARCHAR(45) NOT NULL,
    CNPJ CHAR(15) NOT NULL,
    Endereço VARCHAR(45),
    Contato CHAR(11)
);

ALTER TABLE PessoaJuridica ADD CONSTRAINT unique_cnpj_PessoaJuridica UNIQUE (CNPJ);

-- CONSERTO
CREATE TABLE Conserto (
    idConserto INT auto_increment PRIMARY KEY,
    Descrição VARCHAR(45) NOT NULL
);

-- REVISÃO
CREATE TABLE Revisao (
    idRevisão INT auto_increment PRIMARY KEY,
    Descrição VARCHAR(45) NOT NULL
);

-- MECANICO
CREATE TABLE Mecanico (
    idMecanico INT auto_increment PRIMARY KEY,
    Nome VARCHAR(45) NOT NULL,
    Endereço VARCHAR(45) NOT NULL,
    Especialidade VARCHAR(45) NOT NULL
);

-- EQUIPE MECÂNICOS
CREATE TABLE EqpMecanicos (
    idEqpMecanico INT auto_increment PRIMARY KEY,
    idMecanico INT,
    CONSTRAINT fk_eqp_mecanicos FOREIGN KEY (idMecanico) REFERENCES Mecanico(idMecanico)
);

-- ORDEM DE SERVIÇO
CREATE TABLE OdServiço (
    idOdServiço INT auto_increment PRIMARY KEY,
    DataEmissão DATE,
    ValorServiço FLOAT NOT NULL,
    ValorPeça FLOAT NOT NULL,
    ValorTotal FLOAT NOT NULL,
    Status ENUM('AGUARDANDO', 'EM ANDAMENTO', 'CONCLUIDO', 'CANCELADO'),
    DataConclusão DATE,
    idEqpMecanico INT,
    idConserto INT,
    CONSTRAINT fk_eqp_mecanicos FOREIGN KEY (idEqpMecanico) REFERENCES EqpMecanicos(idEqpMecanico),
    CONSTRAINT fk_conserto FOREIGN KEY (idConserto) REFERENCES Conserto(idConserto)
);

-- REFERENCIA DE PREÇOS
CREATE TABLE ReferenciaPreços (
    idReferenciaPreços INT auto_increment PRIMARY KEY,
    idOdServiço INT,
    CONSTRAINT fk_referencia_precos FOREIGN KEY (idOdServiço) REFERENCES OdServiço(idOdServiço)
);

-- AUTORIZAÇÃO CLIENTE
CREATE TABLE Autorização (
    idAutorização INT auto_increment PRIMARY KEY,
    Autorizado BOOL DEFAULT FALSE,
    idClientes INT,
    idVeiculo INT,
    idOdServiço INT,
    CONSTRAINT fk_autorização_cliente FOREIGN KEY (idClientes) REFERENCES Clientes(idClientes),
    CONSTRAINT fk_autorização_veiculo FOREIGN KEY (idVeiculo) REFERENCES Veiculo(idVeiculo),
    CONSTRAINT fk_autorização_OdServiço FOREIGN KEY (idOdServiço) REFERENCES OdServiço(idOdServiço)
);

-- PEÇAS
CREATE TABLE Pecas (
    idPecas INT auto_increment PRIMARY KEY,
    Descrição VARCHAR(45),
    Valor FLOAT NOT NULL
);

-- OS PEÇAS
CREATE TABLE OsPecas (
    idOsPecas INT auto_increment PRIMARY KEY,
    idPecas INT,
    idOdServiço INT,
    CONSTRAINT fk_pecas FOREIGN KEY (idPecas) REFERENCES Pecas(idPecas),
    CONSTRAINT fk_os_pecas FOREIGN KEY (idOdServiço) REFERENCES OdServiço(idOdServiço)
);

-- SERVIÇOS
CREATE TABLE Serviços (
    idServiços INT auto_increment PRIMARY KEY,
    Descrição VARCHAR(45),
    Valor FLOAT NOT NULL
);

-- ORDEM DE SERVIÇO - SERVIÇOS
CREATE TABLE OdServiço_Serviços (
    idOdServiço INT,
    idServiços INT,
    PRIMARY KEY (idOdServiço, idServiços),
    CONSTRAINT fk_os_serviços FOREIGN KEY (idOdServiço) REFERENCES OdServiço(idOdServiço),
    CONSTRAINT fk_serviços FOREIGN KEY (idServiços) REFERENCES Serviços(idServiços)
);
