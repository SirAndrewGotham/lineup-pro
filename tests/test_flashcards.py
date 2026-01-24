#!/usr/bin/env python3
"""
Test flashcards feature
"""

# Test database methods
print("Testing flashcards feature...")

from data.database import DatabaseManager
from data.seed_flashcards import seed_flashcards

# Initialize database
db = DatabaseManager()
db.initialize()

# Seed flashcards
seed_flashcards()

# Test retrieval
flashcards = db.get_flashcards()
print(f"Retrieved {len(flashcards)} flashcards")

for fc in flashcards:
    print(f"  - {fc.dish_name} ({fc.category}, {fc.difficulty})")

print("\n✅ Flashcards feature tested successfully!")
