PRAGMA foreign_keys = ON;

CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        token TEXT NOT NULL
    );

CREATE TABLE
    notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE
    comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        note_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (note_id) REFERENCES notes (id) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE
    tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT NOT NULL,
        note_id INTEGER NOT NULL,
        FOREIGN KEY (note_id) REFERENCES notes (id) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE INDEX idx_users_username ON users (username);

CREATE INDEX idx_users_token ON users (token);

CREATE INDEX idx_notes_user_id ON notes (user_id);

CREATE INDEX idx_notes_created_at ON notes (created_at);

CREATE INDEX idx_tags_note_id ON tags (note_id);

CREATE INDEX idx_tags_label ON tags (label);

CREATE INDEX idx_comments_note_id ON comments (note_id);