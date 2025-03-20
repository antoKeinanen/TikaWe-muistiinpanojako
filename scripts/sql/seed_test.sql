-- Username: user1 Password: Password123
INSERT INTO
    users (username, password_hash, token)
VALUES
    (
        "user1",
        "scrypt:131072:8:1$yZc0TqTmS96JBmD4AwqMSICC3GzFiVRY$8ef4689150524b736d02e3e67bc440d322a85ce92f3fdfa451b2a76cfd3960f6d3d12e6a46c9886c85992d68e0fa67577ce30e7d7e2e2fd8e879ca21c5a1494a",
        "USER_1_TOKEN"
    );

-- Username: user2 Password: Password123
INSERT INTO
    users (username, password_hash, token)
VALUES
    (
        "user2",
        "scrypt:131072:8:1$yZc0TqTmS96JBmD4AwqMSICC3GzFiVRY$8ef4689150524b736d02e3e67bc440d322a85ce92f3fdfa451b2a76cfd3960f6d3d12e6a46c9886c85992d68e0fa67577ce30e7d7e2e2fd8e879ca21c5a1494a",
        "USER_2_TOKEN"
    );

INSERT INTO
    notes (title, content, user_id)
VALUES
    ("Note 1", "Tämä on esimerkki muistiinpano", 1);