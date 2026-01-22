from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
import json
from datetime import datetime

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
