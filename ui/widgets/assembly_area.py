from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import (
    NumericProperty, ListProperty, ObjectProperty,
    StringProperty, BooleanProperty
)

class DraggableIngredient(DragBehavior, Image):
    """Draggable ingredient widget"""
    ingredient_id = StringProperty('')
    ingredient_name = StringProperty('')
    original_pos = ListProperty([0, 0])
    is_correct_placement = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag_timeout = 100
        self.drag_distance = 10
        self.bind(pos=self.on_pos)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # Return to original position if not dropped in target zone
            if not self.is_correct_placement:
                self.return_to_original()
        return super().on_touch_up(touch)

    def return_to_original(self):
        """Animate return to original position"""
        anim = Animation(pos=self.original_pos, duration=0.3, t='out_back')
        anim.start(self)

class AssemblyArea(Widget):
    """Main assembly simulation area"""
    current_step = NumericProperty(0)
    total_steps = NumericProperty(0)
    placement_zones = ListProperty([])
    active_ingredients = ListProperty([])
    template = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.placement_targets = {}
        self.draggables = []
        self.completed_steps = []
        self.bind(size=self.update_canvas)

    def setup_template(self, template):
        """Initialize assembly area with a template"""
        self.template = template
        self.total_steps = len(template.steps)
        self.current_step = 0
        self.clear_widgets()
        self.draggables = []
        self.completed_steps = []

        # Create placement zones
        self.create_placement_zones()

        # Show first step ingredients
        self.show_current_step()

    def create_placement_zones(self):
        """Create visual placement zones on the assembly area"""
        self.placement_targets = {}

        # Define zone positions (relative to assembly area)
        zones = {
            'heel': (self.center_x - 100, self.center_y - 50),
            'center': (self.center_x, self.center_y),
            'crown': (self.center_x + 100, self.center_y - 50),
            'left': (self.center_x - 150, self.center_y),
            'right': (self.center_x + 150, self.center_y)
        }

        for zone_name, pos in zones.items():
            self.placement_targets[zone_name] = {
                'pos': pos,
                'radius': 40,
                'occupied': False
            }

    def show_current_step(self):
        """Display ingredients for current step"""
        if not self.template or self.current_step >= len(self.template.steps):
            return

        current_step_data = self.template.steps[self.current_step]

        # Create draggable ingredient
        ingredient_widget = DraggableIngredient(
            source=current_step_data.ingredient.image_path,
            size=(80, 80),
            pos=(50, self.height - 150),  # Top-left starting position
            ingredient_id=current_step_data.ingredient.id,
            ingredient_name=current_step_data.ingredient.name,
            original_pos=[50, self.height - 150]
        )

        self.add_widget(ingredient_widget)
        self.draggables.append(ingredient_widget)

        # Highlight target zone
        self.highlight_target_zone(current_step_data.placement)

    def highlight_target_zone(self, zone_name):
        """Highlight the target placement zone"""
        if zone_name in self.placement_targets:
            zone = self.placement_targets[zone_name]

            # Create highlight visual
            with self.canvas.after:
                Color(0, 1, 0, 0.3)  # Green with transparency
                self.highlight_circle = Line(
                    circle=(
                        zone['pos'][0], zone['pos'][1],
                        zone['radius']
                    ),
                    width=2
                )

    def check_placement(self, draggable, touch_pos):
        """Check if ingredient is placed in correct zone"""
        if not self.template or self.current_step >= len(self.template.steps):
            return False

        current_step = self.template.steps[self.current_step]
        target_zone = current_step_data.placement

        if target_zone in self.placement_targets:
            zone = self.placement_targets[target_zone]
            zone_pos = zone['pos']
            zone_radius = zone['radius']

            # Calculate distance from zone center
            distance = Vector(touch_pos).distance(zone_pos)

            if distance <= zone_radius:
                # Correct placement!
                draggable.is_correct_placement = True
                self.complete_current_step(draggable, zone_pos)
                return True

        return False

    def complete_current_step(self, draggable, target_pos):
        """Complete the current assembly step"""
        # Snap to target position
        draggable.pos = [
            target_pos[0] - draggable.width/2,
            target_pos[1] - draggable.height/2
        ]

        # Mark zone as occupied
        current_step = self.template.steps[self.current_step]
        self.placement_targets[current_step.placement]['occupied'] = True

        # Record completion
        self.completed_steps.append(self.current_step)

        # Remove highlight
        if hasattr(self, 'highlight_circle'):
            self.canvas.after.remove(self.highlight_circle)

        # Move to next step after delay
        Clock.schedule_once(lambda dt: self.next_step(), 0.5)

    def next_step(self):
        """Advance to next assembly step"""
        self.current_step += 1

        if self.current_step < len(self.template.steps):
            self.show_current_step()
        else:
            self.on_assembly_complete()

    def on_assembly_complete(self):
        """Trigger when assembly is complete"""
        # This will be connected to scoring system
        print(f"Assembly complete! Steps: {len(self.completed_steps)}/{self.total_steps}")

    def update_canvas(self, *args):
        """Update canvas when size changes"""
        self.create_placement_zones()

    def clear_widgets(self):
        """Clear all draggable widgets"""
        for draggable in self.draggables:
            self.remove_widget(draggable)
        self.draggables = []
