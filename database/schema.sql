CREATE TABLE IF NOT EXISTS text_data (
    source VARCHAR(20),
    id VARCHAR(120),
    content TEXT,
    intention TEXT,
    created_at TIMESTAMP,
    timestamp TIMESTAMP CURRENT_TIMESTAMP,
    PRIMARY KEY (source, id)
);

CREATE TABLE IF NOT EXISTS tag (
    id SERIAL PRIMARY KEY,
    title VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS query (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS label (
    tag BIGINT,
    source VARCHAR(20),
    id VARCHAR(120),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source, id) REFERENCES text_data(source, id),
    FOREIGN KEY (tag) REFERENCES tag(id),
    PRIMARY KEY (tag, source, id)
);

CREATE TABLE IF NOT EXISTS already_labeled (
    query BIGINT,
    source VARCHAR(20),
    id VARCHAR(120),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source, id) REFERENCES text_data(source, id),
    FOREIGN KEY (query) REFERENCES query(id),
    PRIMARY KEY (query, source, id)
);

CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS token (
    key VARCHAR(40) PRIMARY KEY,
    auth_user BIGINT NOT NULL UNIQUE,
    FOREIGN KEY (auth_user) REFERENCES auth_user(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
