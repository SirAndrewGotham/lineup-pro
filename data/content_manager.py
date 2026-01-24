"""
Content Manager - Load and manage training modules and assets
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class IngredientStep:
    """Single step in an assembly procedure"""
    ingredient_id: str
    ingredient_name: str
    image_path: str
    order: int
    placement: str  # 'heel', 'club', 'crown', etc.
    time_target: int  # seconds
    points: int
    
@dataclass
class TrainingModule:
    """Complete training module for a sandwich/assembly"""
    id: str
    title: str
    description: str
    station: str  # 'grill', 'assembly', 'fry', etc.
    difficulty: int  # 1-5
    estimated_time: int  # seconds
    ingredients: List[IngredientStep]
    video_demo: Optional[str] = None
    tips: List[str] = None
    common_errors: List[str] = None
    
    def __post_init__(self):
        if self.tips is None:
            self.tips = []
        if self.common_errors is None:
            self.common_errors = []

class ContentManager:
    """Manages training content loading and organization"""
    
    def __init__(self, content_dir='assets/content'):
        self.content_dir = Path(content_dir)
        self.modules: Dict[str, TrainingModule] = {}
        self.load_all_modules()
    
    def load_all_modules(self):
        """Load all training modules from JSON files"""
        modules_dir = self.content_dir / 'modules'
        if not modules_dir.exists():
            modules_dir.mkdir(parents=True, exist_ok=True)
            self.create_sample_modules()
            return
        
        for json_file in modules_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    module = TrainingModule(**data)
                    self.modules[module.id] = module
            except Exception as e:
                print(f"Error loading module {json_file}: {e}")
    
    def create_sample_modules(self):
        """Create sample training modules if none exist"""
        sample_modules = [
            TrainingModule(
                id='big_hit_basic',
                title='Big Hit - Basic Assembly',
                description='Standard Big Hit burger assembly',
                station='assembly',
                difficulty=2,
                estimated_time=45,
                ingredients=[
                    IngredientStep('bun_bottom', 'Bottom Bun', 'bun_bottom.png', 1, 'heel', 5, 10),
                    IngredientStep('patty', 'Beef Patty', 'patty.png', 2, 'center', 8, 15),
                    IngredientStep('cheese', 'Cheese Slice', 'cheese.png', 3, 'center', 4, 10),
                    IngredientStep('lettuce', 'Lettuce', 'lettuce.png', 4, 'center', 4, 10),
                    IngredientStep('bun_top', 'Top Bun', 'bun_top.png', 5, 'crown', 5, 10),
                ],
                tips=['Start with bottom bun flat', 'Center patty on bun', 'Melt cheese on patty'],
                common_errors=['Ingredients misaligned', 'Wrong order', 'Too slow']
            )
        ]
        
        modules_dir = self.content_dir / 'modules'
        for module in sample_modules:
            module_path = modules_dir / f'{module.id}.json'
            with open(module_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(module), f, indent=2, ensure_ascii=False)
            self.modules[module.id] = module
    
    def get_module(self, module_id: str) -> Optional[TrainingModule]:
        """Get a specific training module"""
        return self.modules.get(module_id)
    
    def list_modules(self) -> List[TrainingModule]:
        """List all available training modules"""
        return list(self.modules.values())
    
    def get_modules_by_difficulty(self, difficulty: int) -> List[TrainingModule]:
        """Get modules by difficulty level"""
        return [m for m in self.modules.values() if m.difficulty == difficulty]

def create_flashcards_table(self):
    """Create flashcards table"""
    query = '''
            CREATE TABLE IF NOT EXISTS flashcards (
                                                      id TEXT PRIMARY KEY,
                                                      dish_name TEXT NOT NULL,
                                                      dish_name_translation_key TEXT NOT NULL,
                                                      dish_image TEXT,
                                                      ingredients TEXT NOT NULL,
                                                      ingredients_translation_keys TEXT NOT NULL,
                                                      difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')) DEFAULT 'medium',
                category TEXT DEFAULT 'sandwiches',
                assembly_tips TEXT,
                created_at TEXT NOT NULL,
                times_reviewed INTEGER DEFAULT 0,
                mastery_level REAL DEFAULT 0.0
                ) \
            '''
    self.execute_query(query)

def save_flashcard(self, flashcard):
    """Save or update a flashcard"""
    query = '''
        INSERT OR REPLACE INTO flashcards 
        (id, dish_name, dish_name_translation_key, dish_image, ingredients, 
         ingredients_translation_keys, difficulty, category, assembly_tips, 
         created_at, times_reviewed, mastery_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    params = (
        flashcard.id,
        flashcard.dish_name,
        flashcard.dish_name_translation_key,
        flashcard.dish_image,
        ','.join(flashcard.ingredients),
        ','.join(flashcard.ingredients_translation_keys),
        flashcard.difficulty,
        flashcard.category,
        ','.join(flashcard.assembly_tips),
        flashcard.created_at.isoformat(),
        flashcard.times_reviewed,
        flashcard.mastery_level
    )
    self.execute_query(query, params)

def get_flashcards(self, category=None, difficulty=None, limit=None):
    """Get flashcards with optional filters"""
    query = 'SELECT * FROM flashcards WHERE 1=1'
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)

    if difficulty:
        query += ' AND difficulty = ?'
        params.append(difficulty)

    query += ' ORDER BY mastery_level ASC, times_reviewed ASC'

    if limit:
        query += ' LIMIT ?'
        params.append(limit)

    results = self.execute_query(query, params, fetch=True)
    return [Flashcard.from_dict(row) for row in results]

def get_flashcard_by_id(self, flashcard_id):
    """Get a specific flashcard by ID"""
    query = 'SELECT * FROM flashcards WHERE id = ?'
    result = self.execute_query(query, (flashcard_id,), fetch=True)
    return Flashcard.from_dict(result[0]) if result else None

def update_flashcard_progress(self, flashcard_id, mastered=True):
    """Update flashcard progress after review"""
    flashcard = self.get_flashcard_by_id(flashcard_id)
    if flashcard:
        flashcard.times_reviewed += 1
        if mastered:
            # Increase mastery (simplified algorithm)
            flashcard.mastery_level = min(1.0, flashcard.mastery_level + 0.25)
        else:
            # Decrease mastery if wrong
            flashcard.mastery_level = max(0.0, flashcard.mastery_level - 0.1)

        self.save_flashcard(flashcard)
