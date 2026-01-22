"""
Ingredient Widget - Draggable ingredient for assembly simulation
"""

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.vector import Vector
from kivy.animation import Animation

class IngredientWidget(Image):
    """
    Draggable ingredient widget with physics properties
    """
    
    ingredient_id = StringProperty('')
    ingredient_name = StringProperty('')
    is_dragging = BooleanProperty(False)
    is_snapped = BooleanProperty(False)
    order = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = None
        self.velocity = Vector(0, 0)
        
    def on_touch_down(self, touch):
        """Handle touch down for dragging"""
        if self.collide_point(*touch.pos) and not self.is_snapped:
            self.is_dragging = True
            self.start_pos = self.pos
            touch.grab(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Handle touch movement for dragging"""
        if self.is_dragging and touch.grab_current is self:
            self.center = touch.pos
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Handle touch up - release ingredient"""
        if self.is_dragging and touch.grab_current is self:
            self.is_dragging = False
            touch.ungrab(self)
            
            # Apply some physics (bounce/slide)
            self.apply_physics()
            return True
        return super().on_touch_up(touch)
    
    def apply_physics(self):
        """Apply simple physics when released"""
        # Simple friction
        anim = Animation(
            x=self.x + self.velocity.x * 10,
            y=self.y + self.velocity.y * 10,
            duration=0.3,
            t='out_quad'
        )
        anim.start(self)
    
    def snap_to(self, target_pos):
        """Animate snapping to target position"""
        self.is_snapped = True
        self.is_dragging = False
        
        anim = Animation(
            center_x=target_pos[0],
            center_y=target_pos[1],
            duration=0.2,
            t='out_back'
        )
        anim.start(self)
        
        # Visual feedback
        self.color = [0.6, 1, 0.6, 1]  # Light green
        
    def reset(self):
        """Reset ingredient to original state"""
        self.is_dragging = False
        self.is_snapped = False
        self.color = [1, 1, 1, 1]  # White
        if self.start_pos:
            self.pos = self.start_pos
