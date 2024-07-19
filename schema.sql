DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);


CREATE TABLE file_info (
  id SERIAL PRIMARY KEY,
  moonshot_id VARCHAR(255),
  filename VARCHAR(255) ,
  file_type VARCHAR(63),
  title TEXT,
  file_content text
);
CREATE TABLE IF NOT EXISTS embeddings (id SERIAL PRIMARY KEY, embedding TEXT)


CREATE TABLE qna (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    embedding BYTEA NOT NULL,
    answer TEXT,
    PRIMARY KEY (id)
);