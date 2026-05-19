DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(120),
    role VARCHAR(20) DEFAULT 'user',
    token VARCHAR(100)
);

INSERT INTO users (username, password, email, role, token) VALUES
    ('admin', 'admin123',  'admin@lab.local', 'admin', 'token_admin_001'),
    ('alice', 'password',  'alice@lab.local', 'user',  'token_alice_002'),
    ('bob',   '123456',    'bob@lab.local',   'user',  'token_bob_003');