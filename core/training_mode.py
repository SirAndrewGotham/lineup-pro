"""
Training session management for different training modes
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional

from core.models import TrainingSession, TrainingMode
from core.scoring_system import ScoringSystem

class TrainingSessionManager:
    """Manages a training session across different modes"""

    def __init__(self, app, user_id: str, template_id: str, mode: str):
        self.app = app
        self.user_id = user_id
        self.template_id = template_id
        self.mode = TrainingMode(mode)
        self.session_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.end_time = None
        self.is_completed = False
        self.current_step = 0
        self.errors = []
        self.completed_steps = []

        # Initialize session object
        self.session = TrainingSession(
            id=self.session_id,
            user_id=user_id,
            template_id=template_id,
            mode=self.mode,
            start_time=self.start_time
        )

        # Get template from database
        self.template = self.app.db.get_template(template_id)

        if not self.template:
            raise ValueError(f"Template not found: {template_id}")

    def next_step(self):
        """Move to next step in training"""
        if self.current_step < len(self.template.steps) - 1:
            self.current_step += 1
            return True
        return False

    def previous_step(self):
        """Move to previous step (not allowed in exam mode)"""
        if self.mode != TrainingMode.EXAM and self.current_step > 0:
            self.current_step -= 1
            return True
        return False

    def record_error(self, error_type: str, description: str, step: int = None):
        """Record an error during training"""
        error = {
            'type': error_type,
            'description': description,
            'step': step if step is not None else self.current_step,
            'timestamp': datetime.now().isoformat()
        }
        self.errors.append(error)
        self.session.errors = self.errors

    def complete_step(self, step_index: int):
        """Mark a step as completed"""
        if step_index not in self.completed_steps:
            self.completed_steps.append(step_index)
            self.session.completed_steps = self.completed_steps

    def end_session(self, completed: bool = True):
        """End the training session and calculate score"""
        self.end_time = datetime.now()
        self.is_completed = completed

        # Update session with end time
        self.session.end_time = self.end_time

        # Calculate score if completed
        if completed:
            scoring_system = ScoringSystem()
            score_result = scoring_system.calculate_session_score(self.session)

            # Update session with scores
            self.session.score = score_result['score']
            self.session.accuracy = score_result['accuracy']
            self.session.speed = score_result['speed']

            # Save to database
            self.app.db.save_session(self.session)

        return self.session
