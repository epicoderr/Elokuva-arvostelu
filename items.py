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
    sql = """
        SELECT items.id, 
               items.title,
               users.username 
        FROM items 
        JOIN users ON items.user_id = users.id
        ORDER BY items.id DESC
    """
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
    db.execute(sql, [title, description, review, item_id])

def remove_item(item_id):
    sql = "DELETE FROM comments WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM images WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])
    
def find_items(query):
    sql = """
        SELECT id, title
        FROM items
        WHERE title LIKE ? OR description LIKE ?
        ORDER BY id DESC
    """
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_comment(item_id, user_id, content):
    sql = """
      INSERT INTO comments (item_id, user_id, content)
      VALUES (?, ?, ?)
    """
    db.execute(sql, (item_id, user_id, content))
    db.commit()

def get_comments(item_id):
    sql = """
      SELECT
        c.id,
        c.item_id,
        c.user_id,       
        c.content,
        c.created_at,
        u.username
      FROM comments c
      JOIN users u ON c.user_id = u.id
      WHERE c.item_id = ?
      ORDER BY c.created_at DESC
    """
    return db.query(sql, (item_id,))

def get_comment(comment_id):
    sql = """
      SELECT id, item_id, user_id, content, created_at
      FROM comments
      WHERE id = ?
    """
    results = db.query(sql, (comment_id,))
    return results[0] if results else None

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id = ?"
    db.execute(sql, (comment_id,))
    db.commit()

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id = ?"
    return db.query(sql, [item_id])

def add_image(item_id, image):
    sql = "INSERT INTO images (item_id, image) VALUES (?, ?)"
    db.execute(sql, [item_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(item_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND item_id = ?"
    db.execute(sql, [image_id, item_id])