-- this sql for creating the database schema for the review management system. It defines tables for users, reviews, categories, and review analysis, along with their relationships and constraints.

-- جدول المالك و الادمن

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK (user_type IN ('owner', 'admin')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--جدول التقييمات الغير معالجه

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    stars INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5),
    status TEXT NOT NULL CHECK (status IN ('queued', 'processed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--جدول التصنيفات

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

--جدول التقاييمات المعالجه

CREATE TABLE IF NOT EXISTS review_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    opinion TEXT NOT NULL CHECK (opinion IN ('positive', 'neutral', 'negative')),
    analyzed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);