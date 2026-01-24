def __init__(self, db_path='data/training.db'):
    self.db_path = db_path
    self.connection = None
    self.connect()

    # Create all tables
    self.create_tables()
    self.create_flashcards_table()
