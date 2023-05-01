class Joke:
    def __init__(self, id=0, text="empty", likes=0, dislikes=0):
        self.id = id
        self.text = text
        self.likes = likes
        self.dislikes = dislikes
        
    def __str__(self):
        return self.text + f"\n👍{self.likes} 👎{self.dislikes}"
