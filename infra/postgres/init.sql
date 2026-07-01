# PostgreSQL initialization script

CREATE DATABASE investment_db;
CREATE DATABASE keycloak_db;
CREATE DATABASE metabase_db;

-- Enable pgcrypto extension for encryption
\c investment_db
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create a schema for audit logs (immutable)
CREATE SCHEMA audit;

-- Create encrypted fields function
CREATE OR REPLACE FUNCTION encrypt_pii(plaintext TEXT, key TEXT DEFAULT current_setting('app.encryption_key')) 
RETURNS BYTEA AS $$
BEGIN
  RETURN pgp_sym_encrypt(plaintext, key);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION decrypt_pii(ciphertext BYTEA, key TEXT DEFAULT current_setting('app.encryption_key')) 
RETURNS TEXT AS $$
BEGIN
  RETURN pgp_sym_decrypt(ciphertext, key);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE investment_db TO investment_user;
GRANT ALL PRIVILEGES ON DATABASE keycloak_db TO investment_user;
GRANT ALL PRIVILEGES ON DATABASE metabase_db TO investment_user;
