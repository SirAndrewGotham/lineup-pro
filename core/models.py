from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Literal
from datetime import datetime
import json

class TrainingMode(Enum):
    GUIDED = "guided"
    PRACTICE = "practice"
    EXAM = "exam"

class IngredientType(Enum):
    BREAD = "bread"
    PROTEIN = "protein"
    VEGETABLE = "vegetable"
    SAUCE = "sauce"
    CHEESE = "cheese"
    TOPPING = "topping"

@dataclass
class Ingredient:
    id: str
    name: str
    type: IngredientType
    image_path: str
    calories: int = 0
    allergens: List[str] = field(default_factory=list)
    placement_zones: List[str] = field(default_factory=lambda: ["center"])

@dataclass
class AssemblyStep:
    order: int
    ingredient: Ingredient
    placement: str  # 'heel', 'center', 'crown', 'left', 'right'
    quantity: int = 1
    time_target: int = 5  # seconds
    points: int = 10
    critical: bool = True  # Must be correct for passing

@dataclass
class SandwichTemplate:
    id: str
    name: str
    station: str
    difficulty: int  # 1-5
    total_time_target: int  # seconds
    steps: List[AssemblyStep]
    description: str = ""
    image_path: str = ""
    common_errors: List[str] = field(default_factory=list)

@dataclass
class TrainingSession:
    id: str
    user_id: str
    template_id: str
    mode: TrainingMode
    start_time: datetime
    end_time: Optional[datetime] = None
    score: float = 0.0
    accuracy: float = 0.0
    speed: float = 0.0
    errors: List[Dict] = field(default_factory=list)
    completed_steps: List[int] = field(default_factory=list)

@dataclass
class UserProgress:
    user_id: str
    templates_mastered: Dict[str, float] = field(default_factory=dict)  # template_id: best_score
    total_sessions: int = 0
    average_accuracy: float = 0.0
    average_speed: float = 0.0
    skill_matrix: Dict[str, float] = field(default_factory=dict)  # skill: level

@dataclass
class Flashcard:
    """Represents a single flashcard for dish memorization"""
    id: str
    dish_name: str
    dish_name_translation_key: str  # For i18n
    dish_image: str  # Path to image
    ingredients: List[str]  # List of ingredient names
    ingredients_translation_keys: List[str]  # For i18n
    difficulty: Literal['easy', 'medium', 'hard'] = 'medium'
    category: str = 'sandwiches'  # e.g., 'sandwiches', 'breakfast', 'sides'
    assembly_tips: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    times_reviewed: int = 0
    mastery_level: float = 0.0  # 0.0 to 1.0

    def to_dict(self):
        """Convert to dictionary for SQLite storage"""
        return {
            'id': self.id,
            'dish_name': self.dish_name,
            'dish_name_translation_key': self.dish_name_translation_key,
            'dish_image': self.dish_image,
            'ingredients': ','.join(self.ingredients),
            'ingredients_translation_keys': ','.join(self.ingredients_translation_keys),
            'difficulty': self.difficulty,
            'category': self.category,
            'assembly_tips': ','.join(self.assembly_tips),
            'created_at': self.created_at.isoformat(),
            'times_reviewed': self.times_reviewed,
            'mastery_level': self.mastery_level
        }

    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            id=data['id'],
            dish_name=data['dish_name'],
            dish_name_translation_key=data['dish_name_translation_key'],
            dish_image=data['dish_image'],
            ingredients=data['ingredients'].split(','),
            ingredients_translation_keys=data['ingredients_translation_keys'].split(','),
            difficulty=data['difficulty'],
            category=data['category'],
            assembly_tips=data['assembly_tips'].split(','),
            created_at=datetime.fromisoformat(data['created_at']),
            times_reviewed=data['times_reviewed'],
            mastery_level=data['mastery_level']
        )
