"""
Assembly Engine - Core drag-and-drop physics and simulation
"""

from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
import random

class AssemblyEngine(Widget):
    """
    Engine that handles physics, collision detection, and assembly logic
    for the drag-and-drop training simulator.
    """
    
    gravity = NumericProperty(0.5)
    friction = NumericProperty(0.95)
    snap_distance = NumericProperty(20)  # Pixels
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ingredients = []
        self.target_positions = {}
        self.current_score = 0
        self.max_score = 100
        
    def add_ingredient(self, ingredient_widget, target_position):
        """
        Add an ingredient to the assembly area
        """
        self.ingredients.append(ingredient_widget)
        self.target_positions[ingredient_widget] = target_position
        self.add_widget(ingredient_widget)
    
    def check_collision(self, ingredient, target):
        """
        Check if ingredient is close enough to target position
        """
        ingredient_pos = Vector(ingredient.center)
        target_pos = Vector(target)
        distance = ingredient_pos.distance(target_pos)
        
        return distance <= self.snap_distance
    
    def snap_to_position(self, ingredient):
        """
        Snap ingredient to its target position
        """
        if ingredient in self.target_positions:
            ingredient.center = self.target_positions[ingredient]
            return True
        return False
    
    def calculate_score(self, ingredient, time_taken):
        """
        Calculate score for placing an ingredient
        """
        if ingredient in self.target_positions:
            current_pos = Vector(ingredient.center)
            target_pos = Vector(self.target_positions[ingredient])
            distance = current_pos.distance(target_pos)
            
            # Perfect placement bonus
            if distance <= 5:
                accuracy_bonus = 20
            elif distance <= 10:
                accuracy_bonus = 15
            elif distance <= 15:
                accuracy_bonus = 10
            else:
                accuracy_bonus = 5
            
            # Time bonus (faster = better)
            time_bonus = max(0, 30 - time_taken) * 2
            
            return accuracy_bonus + time_bonus
        return 0
    
    def reset(self):
        """Reset the assembly area"""
        for ingredient in self.ingredients:
            self.remove_widget(ingredient)
        self.ingredients = []
        self.target_positions = {}
        self.current_score = 0
