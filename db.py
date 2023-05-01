
import sqlite3
from jokeclass import Joke


def get(id, basename="mytable"):
    # Connect to the database
    conn = sqlite3.connect('data/jokes.db')

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
              likes INTEGER,
              dislikes INTEGER);''')
    
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
    conn.execute(f'''CREATE TABLE {basename}
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              likes TEXT NOT NULL,
              dislikes TEXT NOT NULL);''')
    conn.commit()
    conn.close()
    
def update(id, delta): #delta = (delta_likes, delta_dislikes)
    joke = get(id)
    joke.likes += delta[0]
    joke.dislikes += delta[1]
    add(joke)
    
if __name__ == '__main__':
    add(Joke(123, "test joke", 90, 10))
    update(123, (0, 1))
    
    print(get(123))
    
    clear_database()
