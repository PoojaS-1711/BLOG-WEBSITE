import sqlite3
import datetime

# --------- Blog Table ---------
def create_blog_table():
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            author TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_blog_post(title, content, category, author):
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute('INSERT INTO blog_posts (title, content, category, author, timestamp) VALUES (?, ?, ?, ?, ?)', 
              (title, content, category, author, timestamp))
    conn.commit()
    conn.close()

def get_all_posts():
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    c.execute('SELECT title, content, category, author, timestamp FROM blog_posts ORDER BY id DESC')
    data = c.fetchall()
    conn.close()
    return data

def get_posts_by_category(selected_category):
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT title, content, category, author, timestamp 
        FROM blog_posts 
        WHERE category=? 
        ORDER BY id DESC
    ''', (selected_category,))
    data = c.fetchall()
    conn.close()
    return data

# ---------- Comments Table ----------
# ---------- Comments Table ----------
def create_comments_table():
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_title TEXT,
            commenter TEXT,
            comment TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_comment(post_title, commenter, comment):
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute('''
        INSERT INTO comments (post_title, commenter, comment, timestamp) 
        VALUES (?, ?, ?, ?)
    ''', (post_title, commenter, comment, timestamp))
    conn.commit()
    conn.close()

def get_comments_for_post(post_title):
    conn = sqlite3.connect('blog_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT commenter, comment, timestamp 
        FROM comments 
        WHERE post_title = ? 
        ORDER BY comment_id ASC
    ''', (post_title,))
    data = c.fetchall()
    conn.close()
    return data
