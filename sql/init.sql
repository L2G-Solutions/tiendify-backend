CREATE TABLE
    IF NOT EXISTS users (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        email VARCHAR NOT NULL UNIQUE,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        phone VARCHAR,
        email_verified BOOLEAN NOT NULL,
        role VARCHAR NOT NULL CHECK (role IN ('ADMIN', 'USER'))
    );

CREATE TABLE
    IF NOT EXISTS resource_group (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        azure_blob_storage_id VARCHAR,
        database_id VARCHAR,
        web_app_id VARCHAR,
        api_url VARCHAR
    );

CREATE TABLE
    IF NOT EXISTS shop (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        name VARCHAR NOT NULL,
        headline VARCHAR,
        about VARCHAR,
        currency VARCHAR NOT NULL,
        logoImg VARCHAR,
        bannerImg VARCHAR,
        country VARCHAR NOT NULL,
        status VARCHAR NOT NULL CHECK (
            status IN ('ACTIVE', 'UNPUPLISHED', 'DELETED', 'SUSPENDED')
        ),
        verified BOOLEAN NOT NULL,
        owner_id UUID NOT NULL,
        resource_group_id UUID,
        FOREIGN KEY (owner_id) REFERENCES users (id),
        FOREIGN KEY (resource_group_id) REFERENCES resource_group (id)
    );

CREATE TABLE
    IF NOT EXISTS shop_externallinks (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        shop_id UUID NOT NULL,
        name BIGINT NOT NULL,
        external_link_id BIGINT NOT NULL,
        FOREIGN KEY (shop_id) REFERENCES shop (id)
    );