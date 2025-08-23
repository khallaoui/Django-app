-- Script SQL pour créer la base de données Django
-- À exécuter dans phpMyAdmin ou MySQL Command Line

-- Créer la base de données
CREATE DATABASE IF NOT EXISTS gestion_alertes_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Sélectionner la base de données
USE gestion_alertes_db;

-- Créer un utilisateur Django (optionnel)
-- CREATE USER IF NOT EXISTS 'django_user'@'localhost' IDENTIFIED BY 'django_password';
-- GRANT ALL PRIVILEGES ON gestion_alertes_db.* TO 'django_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Vérifier que la base de données est créée
SHOW DATABASES LIKE 'gestion_alertes_db';

-- Afficher un message de confirmation
SELECT 'Base de données gestion_alertes_db créée avec succès!' AS Message;