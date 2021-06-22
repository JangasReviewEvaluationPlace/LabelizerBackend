CREATE TABLE IF NOT EXISTS text_data (
    source VARCHAR(20),
    id VARCHAR(120),
    content TEXT,
    intention TEXT,
    created_at TIMESTAMP,
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