CREATE TABLE
    IF NOT EXISTS categories (
        slug VARCHAR NOT NULL PRIMARY KEY,
        name VARCHAR NOT NULL,
        description VARCHAR NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS addresses (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        address_label VARCHAR NOT NULL,
        city VARCHAR NOT NULL,
        state VARCHAR NOT NULL,
        zip_code VARCHAR NOT NULL,
        country VARCHAR NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS customers (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        email VARCHAR NOT NULL UNIQUE,
        password VARCHAR NOT NULL,
        phone VARCHAR NOT NULL,
        default_address_id BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (default_address_id) REFERENCES addresses (id)
    );

CREATE TABLE
    IF NOT EXISTS products (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR NOT NULL,
        description VARCHAR NOT NULL,
        price BIGINT NOT NULL,
        stock INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS payments (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        amount BIGINT NOT NULL,
        method VARCHAR NOT NULL,
        status VARCHAR NOT NULL CHECK (status IN ('PENDING', 'PAID', 'FAILED')),
        paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS mediafiles (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        url VARCHAR NOT NULL,
        type VARCHAR NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS shipping (
        id UUID DEFAULT gen_random_uuid () PRIMARY KEY,
        address_id BIGINT NOT NULL,
        status VARCHAR NOT NULL CHECK (
            status IN ('PENDING', 'SHIPPED', 'DELIVERED', 'RETURNED')
        ),
        estimated_delivery INT NOT NULL,
        delivered_at TIMESTAMP,
        shipped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (address_id) REFERENCES addresses (id)
    );

CREATE TABLE
    IF NOT EXISTS orders (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        customer_id UUID NOT NULL,
        shipping_id UUID NOT NULL,
        payment_id UUID NOT NULL,
        ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (shipping_id) REFERENCES shipping (id),
        FOREIGN KEY (payment_id) REFERENCES payments (id)
    );

CREATE TABLE
    IF NOT EXISTS product_categories (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        product_id BIGINT NOT NULL,
        category_id VARCHAR NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (category_id) REFERENCES categories (slug)
    );

CREATE TABLE
    IF NOT EXISTS order_items (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        order_id BIGINT NOT NULL,
        product_id BIGINT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    );

CREATE TABLE
    IF NOT EXISTS products_mediafiles (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        product_id BIGINT NOT NULL,
        media_file_id BIGINT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id),
        FOREIGN KEY (media_file_id) REFERENCES mediafiles (id)
    );