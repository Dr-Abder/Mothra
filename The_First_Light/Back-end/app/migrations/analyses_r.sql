CREATE TABLE IF NOT EXISTS analyses(
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    photo TEXT NOT NULL,
    diagnostic TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP NOT NULL
)