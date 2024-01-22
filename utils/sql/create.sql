-- ------------------
-- Create database --
-- ------------------
CREATE DATABASE IF NOT EXISTS ensaware;
USE ensaware;
-- ----------------------
-- Create career table --
-- ----------------------
CREATE TABLE IF NOT EXISTS career (
    id VARCHAR(60) DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_career_id PRIMARY KEY (id),
    CONSTRAINT unq_career_name UNIQUE (name)
);
-- -----------------------
-- Create profile table --
-- -----------------------
CREATE TABLE IF NOT EXISTS profile (
    id VARCHAR(60) DEFAULT (UUID()),
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_profile_id PRIMARY KEY (id),
    CONSTRAINT unq_profile_name UNIQUE (name)
);
-- --------------------
-- Create user table --
-- --------------------
CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(60) DEFAULT (UUID()),
    provider_id VARCHAR(60) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    picture VARCHAR(255) NULL,
    profile_id VARCHAR(60) NOT NULL,
    career_id VARCHAR(60) NULL,
    refresh_token VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (id),
    CONSTRAINT unq_user_email UNIQUE (email),
    CONSTRAINT fk_user_profile_id FOREIGN KEY (profile_id) REFERENCES profile (id),
    CONSTRAINT fk_user_career_id FOREIGN KEY (career_id) REFERENCES career (id),
    CONSTRAINT unq_user_refresh_token UNIQUE (refresh_token)
);
-- Create indexes
CREATE INDEX idx_user_provider ON user (provider);
-- ----------------------------
-- Create content_type table --
-- ----------------------------
CREATE TABLE IF NOT EXISTS content_type (
    id VARCHAR(60) DEFAULT (UUID()),
    model VARCHAR(100) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_content_type_id PRIMARY KEY (id),
    CONSTRAINT unq_content_type_model UNIQUE (model)
);
-- --------------------
-- Create permission --
-- --------------------
CREATE TABLE IF NOT EXISTS permission (
    id VARCHAR(60) DEFAULT (UUID()),
    content_type_id VARCHAR(60) NOT NULL,
    code_name VARCHAR(255) NOT NULL,
    description VARCHAR(100) NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_permission_id PRIMARY KEY (id),
    CONSTRAINT fk_permission_content_type_id FOREIGN KEY (content_type_id) REFERENCES content_type (id),
    CONSTRAINT unq_permission_code_name UNIQUE (code_name)
);
-- ----------------------------
-- Create permission_profile --
-- ----------------------------
CREATE TABLE IF NOT EXISTS permission_profile (
    id VARCHAR(60) DEFAULT (UUID()),
    permission_id VARCHAR(60) NOT NULL,
    profile_id VARCHAR(60) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_permission_profile_id PRIMARY KEY (id),
    CONSTRAINT fk_permission_profile_profile_id FOREIGN KEY (profile_id) REFERENCES profile (id),
    CONSTRAINT fk_permission_profile_permission_id FOREIGN KEY (permission_id) REFERENCES permission (id),
    CONSTRAINT unq_permission_profile UNIQUE (permission_id, profile_id)
);
-- -------------------
-- Create type_room --
-- -------------------
CREATE TABLE IF NOT EXISTS type_room (
    id VARCHAR(60) DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_type_room_id PRIMARY KEY (id),
    CONSTRAINT unq_type_room_name UNIQUE (name)
);
-- --------------
-- Create room --
-- --------------
CREATE TABLE IF NOT EXISTS room (
    id VARCHAR(60) DEFAULT (UUID()),
    type_room_id VARCHAR(60) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    distance_meters INT NOT NULL DEFAULT 5,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_room_id PRIMARY KEY (id),
    CONSTRAINT fk_room_type_room_id FOREIGN KEY (type_room_id) REFERENCES type_room (id),
    CONSTRAINT unq_room_name UNIQUE (name)
);
-- -----------------------
-- Create elements_room --
-- -----------------------
CREATE TABLE IF NOT EXISTS elements_room (
    id VARCHAR(60) DEFAULT (UUID()),
    room_id VARCHAR(60) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    data TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_elements_room PRIMARY KEY (id),
    CONSTRAINT fk_elements_room_room_id FOREIGN KEY (room_id) REFERENCES room (id)
);
-- -- --------------------------------
-- -- Create historic_qr_code table --
-- -- --------------------------------
CREATE TABLE IF NOT EXISTS historic_qr_code (
    id VARCHAR(60) DEFAULT (UUID()),
    user_id VARCHAR(60) NOT NULL,
    element_room_id VARCHAR(60) NULL,
    data TEXT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_historic_qr_code_id PRIMARY KEY (id),
    CONSTRAINT fk_historic_qr_code_user_id FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT fk_historic_qr_code_element_room_id FOREIGN KEY (element_room_id) REFERENCES elements_room (id)
);
-- -----------------------
-- Create library table --
-- -----------------------
CREATE TABLE IF NOT EXISTS library (
    id VARCHAR(60) NOT NULL DEFAULT (UUID()),
    title VARCHAR(100) NOT NULL,
    bar_code VARCHAR(20) NULL,
    isbn VARCHAR(20) NULL,
    item_number VARCHAR(20) NULL,
    library_number VARCHAR(20) NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_library_id PRIMARY KEY (id)
);
-- Create indexes
CREATE INDEX idx_library_isbn ON library (isbn);
CREATE INDEX idx_library_bar_code ON library (bar_code);
CREATE INDEX idx_library_item_number ON library (item_number);
CREATE INDEX idx_library_library_number ON library (library_number);
-- ----------------------------
-- Create library_user table --
-- ----------------------------
CREATE TABLE IF NOT EXISTS library_user (
    id VARCHAR(60) NOT NULL DEFAULT (UUID()),
    library_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_library_user_id PRIMARY KEY (id),
    CONSTRAINT fk_library_user_library_id FOREIGN KEY (library_id) REFERENCES library (id),
    CONSTRAINT fk_library_user_user_id FOREIGN KEY (user_id) REFERENCES user (id)
);
-- ----------------------
-- Create domain table --
-- ----------------------
CREATE TABLE IF NOT EXISTS domain (
    id VARCHAR(60) NOT NULL DEFAULT (UUID()),
    value VARCHAR(100) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP NULL,
    CONSTRAINT pk_domain_id PRIMARY KEY (id),
    CONSTRAINT unq_domain_value UNIQUE (value)
);