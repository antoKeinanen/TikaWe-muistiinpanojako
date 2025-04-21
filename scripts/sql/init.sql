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

CREATE TABLE
    user_statistics (
        user_id INTEGER PRIMARY KEY,
        note_count INTEGER DEFAULT 0,
        comment_count INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE INDEX idx_users_username ON users (username);

CREATE INDEX idx_users_token ON users (token);

CREATE INDEX idx_notes_user_id ON notes (user_id);

CREATE INDEX idx_notes_created_at ON notes (created_at);

CREATE INDEX idx_tags_note_id ON tags (note_id);

CREATE INDEX idx_tags_label ON tags (label);

CREATE INDEX idx_comments_note_id ON comments (note_id);

CREATE TRIGGER create_user_statistics AFTER INSERT ON users BEGIN
INSERT INTO
    user_statistics (user_id)
VALUES
    (NEW.id);

END;

CREATE TRIGGER delete_user_statistics AFTER DELETE ON users BEGIN
DELETE FROM user_statistics
WHERE
    user_id = OLD.id;

END;

CREATE TRIGGER increment_note_count AFTER INSERT ON notes BEGIN
UPDATE user_statistics
SET
    note_count = note_count + 1
WHERE
    user_id = NEW.user_id;

END;

CREATE TRIGGER decrement_note_count AFTER DELETE ON notes BEGIN
UPDATE user_statistics
SET
    note_count = note_count - 1
WHERE
    user_id = OLD.user_id;

END;

CREATE TRIGGER increment_comment_count AFTER INSERT ON comments BEGIN
UPDATE user_statistics
SET
    comment_count = comment_count + 1
WHERE
    user_id = NEW.user_id;

END;

CREATE TRIGGER decrement_comment_count AFTER DELETE ON comments BEGIN
UPDATE user_statistics
SET
    comment_count = comment_count - 1
WHERE
    user_id = OLD.user_id;

END;