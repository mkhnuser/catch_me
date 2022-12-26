BEGIN TRANSACTION;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS rendezvous(
    id uuid DEFAULT uuid_generate_v4(),
    title TEXT
    CONSTRAINT is_title_length_in_required_interval
    CHECK (4 <= char_length(title) AND char_length(title) <= 64) NOT NULL,
    description TEXT
    CONSTRAINT is_description_length_in_required_interval
    CHECK (char_length(description) <= 1024) NULL,
    latitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY(id)
);

COMMIT;
