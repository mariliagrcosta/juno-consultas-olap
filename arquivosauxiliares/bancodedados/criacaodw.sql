-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema junodwvazio
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `junodwvazio` ;

-- -----------------------------------------------------
-- Schema juno
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `junodwvazio` DEFAULT CHARACTER SET utf8 ;
USE `junodwvazio` ;

-- -----------------------------------------------------
-- Table `junodwvazio`.`DimVeiculo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`DimVeiculo` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`DimVeiculo` (
  `dimveiculo_codigo` INT NOT NULL,
  `veiculo_id` INT NOT NULL,
  `tipo` INT DEFAULT NULL,
  `placa` VARCHAR(10) DEFAULT NULL,
  `ano` YEAR DEFAULT NULL,
  `marca` VARCHAR(50) DEFAULT NULL,
  `modelo` VARCHAR(50) DEFAULT NULL,
  `cor` VARCHAR(20) DEFAULT NULL,
  `version` INT DEFAULT NULL,
  `date_from` TIMESTAMP DEFAULT NULL,
  `date_to` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`dimveiculo_codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junodwvazio`.`DimEndereco`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`DimEndereco` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`DimEndereco` (
  `dimendereco_codigo` INT NOT NULL,
  `endereco_id` INT NOT NULL,
  `cep` VARCHAR(8) DEFAULT '00000000',
  `rua` VARCHAR(255) DEFAULT NULL,
  `bairro` VARCHAR(45) DEFAULT NULL,
  `tiposubdivisao` VARCHAR(45) DEFAULT NULL,
  `subdivisao` VARCHAR(100) DEFAULT NULL,
  `municipio` VARCHAR(45) DEFAULT NULL,
  `estado` VARCHAR(45) DEFAULT NULL,
  `complemento` VARCHAR(45) DEFAULT NULL,
  `latitude`VARCHAR(50) DEFAULT NULL,
  `longitude` VARCHAR(50) DEFAULT NULL,
  `version` INT DEFAULT NULL,
  `date_from` TIMESTAMP DEFAULT NULL,
  `date_to` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`dimendereco_codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junodwvazio`.`DimAluno`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`DimAluno` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`DimAluno` (
  `dimaluno_codigo` INT NOT NULL,
  `aluno_id` INT NOT NULL,
  `sigaa_id` INT NOT NULL,
  `matricula` INT NOT NULL DEFAULT '000000000',
  `periodo` INT DEFAULT NULL,
  `nome` VARCHAR(20) DEFAULT NULL,
  `sobrenome` VARCHAR(255) DEFAULT NULL,
  `cpf` VARCHAR(20) NOT NULL DEFAULT '00000000000',
  `datanascimento` DATE DEFAULT NULL,
  `telefonecelular` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  `senha` VARCHAR(45) DEFAULT NULL,
  `endereco_id` INT NOT NULL,
  `cep` VARCHAR(8) DEFAULT '00000000',
  `rua` VARCHAR(255) DEFAULT NULL,
  `bairro` VARCHAR(45) DEFAULT NULL,
  `municipio` VARCHAR(45) DEFAULT NULL,
  `estado` VARCHAR(45) DEFAULT NULL,
  `curso_id` INT NOT NULL,
  `nomecurso` VARCHAR(100) DEFAULT NULL,
  `turno` INT DEFAULT NULL,
  `version` INT DEFAULT NULL,
  `date_from` TIMESTAMP DEFAULT NULL,
  `date_to` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`dimaluno_codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junodwvazio`.`DimData`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`DimData` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`DimData` (
  `dimdata_codigo` INT NOT NULL,
  `data_id` INT NOT NULL,
  `data` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dia_ediautil` INT(11) DEFAULT NULL,
  `dia_numeronasemana` INT(11) DEFAULT NULL,
  `dia_numeronome` INT(11) DEFAULT NULL,
  `dia_numeronoano` INT(11) DEFAULT NULL,
  `semana_id` INT(11) DEFAULT NULL,
  `semana_nome` VARCHAR(255) DEFAULT NULL,
  `semana_texto` VARCHAR(255) DEFAULT NULL,
  `semana_numeronoano` INT(11) DEFAULT NULL,
  `mes_id` INT(11) DEFAULT NULL,
  `mes_nome` VARCHAR(255) DEFAULT NULL,
  `mes_texto` VARCHAR(255) DEFAULT NULL,
  `mes_numeronoano` VARCHAR(255) DEFAULT NULL,
  `trimestre_id` INT(11) DEFAULT NULL,
  `trimestre_nome` VARCHAR(255) DEFAULT NULL,
  `trimestre_texto` VARCHAR(255) DEFAULT NULL,
  `trimestre_numeronoano` INT(11) DEFAULT NULL,
  `semestre_id` INT(11) DEFAULT NULL,
  `semestre_nome` VARCHAR(255) DEFAULT NULL,
  `semestre_texto` VARCHAR(255) DEFAULT NULL,
  `semestre_numeronoano` INT(11) DEFAULT NULL,
  `ano_id` INT(11) DEFAULT NULL,
  `ano_nome` VARCHAR(255) DEFAULT NULL,
  `ano_texto` VARCHAR(255) DEFAULT NULL,
  `version` INT DEFAULT NULL,
  `date_from` TIMESTAMP DEFAULT NULL,
  `date_to` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`dimdata_codigo`))
ENGINE = InnoDB;

SET SQL_MODE='ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Table `junodwvazio`.`DimHorario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`DimHorario` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`DimHorario` (
  `dimhorario_codigo` INT NOT NULL,
  `horario_id` INT NOT NULL,
  `horario` TIME DEFAULT NULL,
  `turno` VARCHAR(15) DEFAULT NULL,
  `version` INT DEFAULT NULL,
  `date_from` TIMESTAMP DEFAULT NULL,
  `date_to` TIMESTAMP DEFAULT NULL,
  
  PRIMARY KEY (`dimhorario_codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `junodwvazio`.`FatoDeslocamento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `junodwvazio`.`FatoDeslocamento` ;

CREATE TABLE IF NOT EXISTS `junodwvazio`.`FatoDeslocamento` (
  `dimveiculo_codigo` INT NOT NULL,
  `dimenderecoorigem_codigo` INT NOT NULL,
  `dimenderecodestino_codigo` INT NOT NULL,
  `dimaluno_codigo` INT NOT NULL,
  `dimdata_codigo` INT NOT NULL,
  `dimhorario_codigo` INT NOT NULL,
  `vagasdisponibilizadas` INT DEFAULT NULL,
  `vagasocupadas` INT DEFAULT NULL,
  `distanciadeslocamento` DECIMAL(10,3) DEFAULT NULL,
  PRIMARY KEY (`dimveiculo_codigo`, `dimenderecoorigem_codigo`, `dimenderecodestino_codigo`, `dimaluno_codigo`, `dimdata_codigo`, `dimhorario_codigo`),
  INDEX `fk_Fato Corrida_Dim. veículo1_idx` (`dimveiculo_codigo` ASC) VISIBLE,
  INDEX `fk_Fato Corrida_Dim. deslocamento1_idx` (`dimenderecoorigem_codigo` ASC) VISIBLE,
  INDEX `fk_Fato Corrida_Dim. Aluno1_idx` (`dimaluno_codigo` ASC) VISIBLE,
  INDEX `fk_Fato Corrida_Dim. Data1_idx` (`dimdata_codigo` ASC) VISIBLE,
  INDEX `fk_Fato Corrida_Dim.Hora1_idx` (`dimhorario_codigo` ASC) VISIBLE,
  INDEX `fk_Fato Corrida_DimEndereco1_idx` (`dimenderecodestino_codigo` ASC) VISIBLE,
  CONSTRAINT `fk_dimdata`
    FOREIGN KEY (`dimdata_codigo`)
    REFERENCES `junodwpopulado`.`dimdata` (`dimdata_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dimveiculo`
    FOREIGN KEY (`dimveiculo_codigo`)
    REFERENCES `junodwpopulado`.`dimveiculo` (`dimveiculo_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dimenderecoorigem`
    FOREIGN KEY (`dimenderecoorigem_codigo`)
    REFERENCES `junodwpopulado`.`dimendereco` (`dimendereco_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_dimenderecodestino`
    FOREIGN KEY (`dimenderecodestino_codigo`)
    REFERENCES `junodwpopulado`.`dimendereco` (`dimendereco_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_aluno`
    FOREIGN KEY (`dimaluno_codigo`)
    REFERENCES `junodwpopulado`.`dimaluno` (`dimaluno_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_horario`
    FOREIGN KEY (`dimhorario_codigo`)
    REFERENCES `junodwpopulado`.`dimhorario` (`dimhorario_codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;