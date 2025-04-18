import db

def add_item(title, description, review, user_id, classes):
    sql = "INSERT INTO items (title, description, review, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, review, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    
    return db.query(sql)

def get_item(item_id):
    sql = """
    SELECT items.id,
           items.title, 
           items.description,
           items.review, 
           users.id user_id,
           users.username
    FROM items, users
    WHERE items.user_id = users.id AND items.id = ?
"""
    result = db.query(sql, [item_id])[0]
    return result if result else None

def update_item(item_id, title, description, review):
    sql = """
    UPDATE items SET title= ?,
           description = ?, 
           review = ?
    WHERE id = ?
"""
    db.execute(sql, [ title, description, review, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [ item_id])

def find_items(query):
    sql = """
        SELECT id, title
        FROM items
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY id DESC
    """
    like = "%" + query + "%"
    return db.query(sql, [like, like])
