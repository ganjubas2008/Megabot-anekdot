import sqlite3
from jokeclass import Joke


def get(id, basename="mytable"):
    # Connect to the database
    conn = sqlite3.connect('data/jokes.db')
    
    conn.execute(f'''CREATE TABLE IF NOT EXISTS {basename}
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              likes INTEGER KEY,
              dislikes INTEGER KEY);''')

    # Retrieve data from the table
    cursor = conn.execute(f"SELECT text FROM {basename} WHERE id=?", (id,))
    text_res = cursor.fetchone()

    # Return joke object
    if text_res:
        cursor = conn.execute(f"SELECT likes FROM {basename} WHERE id=?", (id,))
        likes_res = cursor.fetchone()
        cursor = conn.execute(f"SELECT dislikes FROM {basename} WHERE id=?", (id,))
        dislikes_res = cursor.fetchone()    
        conn.close()
        return Joke(id=id, text=text_res[0], likes=int(likes_res[0]), dislikes=int(dislikes_res[0]))
    else:
        conn.close()
        return Joke()


def add(joke, basename="mytable"):
    # If joke is empty
    if joke.id == 0:
        return
    # Connect to the database
    conn = sqlite3.connect('data/jokes.db')

    conn.execute(f'''CREATE TABLE IF NOT EXISTS {basename}
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              likes INTEGER KEY,
              dislikes INTEGER KEY);''')
    
    # Delete if joke is in the database
    old_joke = get(joke.id)
    if old_joke.id != 0: #if id is present in database
        if old_joke == joke:
            return
        else:
            c = conn.cursor()
            c.execute(f"DELETE FROM {basename} WHERE id=?", (joke.id,))
            conn.commit()

    # Insert data into the table
    conn.execute(f"INSERT INTO {basename} (id, text, likes, dislikes) VALUES (?, ?, ?, ?)", (joke.id, joke.text, joke.likes, joke.dislikes))
    conn.commit()

    # Close the connection
    conn.close()

def clear_database(basename="mytable"):
    conn = sqlite3.connect('data/jokes.db')
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS {basename}")
    conn.execute(f'''CREATE TABLE IF NOT EXISTS {basename}
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              likes INTEGER KEY,
              dislikes INTEGER KEY);''')
    conn.commit()
    conn.close()
    
def get_best(basename="mytable"):
    conn = sqlite3.connect('data/jokes.db')

    c = conn.cursor()
    c.execute(f"SELECT * FROM {basename} ORDER BY likes DESC LIMIT 1")
    row = c.fetchone()

    conn.close()
    return Joke(id=row[0], text=row[1], likes=row[2], dislikes=row[3])

def get_worst(basename="mytable"):
    conn = sqlite3.connect('data/jokes.db')

    c = conn.cursor()
    c.execute(f"SELECT * FROM {basename} ORDER BY dislikes DESC LIMIT 1")
    row = c.fetchone()

    conn.close()
    return Joke(id=row[0], text=row[1], likes=row[2], dislikes=row[3])
    
def update(id, delta): #delta = (delta_likes, delta_dislikes)
    joke = get(id)
    joke.likes += delta[0]
    joke.dislikes += delta[1]
    add(joke)
    
if __name__ == '__main__':
    add(Joke(200, "90 10", 90, 10))
    add(Joke(201, "80 10", 80, 102))
    add(Joke(202, "100 10", 100, 10))
    add(Joke(100, "45 8", 45, 8))
    
    print(get_best())
    print(get_worst())
    clear_database()
