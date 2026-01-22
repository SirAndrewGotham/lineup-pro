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
