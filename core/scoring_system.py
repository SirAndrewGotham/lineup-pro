from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json

from core.models import *

class ScoringSystem:
    """Calculates scores and tracks performance"""

    def __init__(self):
        self.base_points_per_step = 10
        self.time_bonus_factor = 2.0
        self.accuracy_weight = 0.7
        self.speed_weight = 0.3

    def calculate_session_score(self, session: TrainingSession) -> Dict:
        """Calculate comprehensive score for a training session"""

        # Get template for reference
        # This would come from database in real implementation
        template = self._get_template_by_id(session.template_id)

        if not template:
            return {
                'score': 0,
                'accuracy': 0,
                'speed': 0,
                'grade': 'F',
                'feedback': 'Template not found'
            }

        # Calculate accuracy
        accuracy = self._calculate_accuracy(session, template)

        # Calculate speed
        speed = self._calculate_speed(session, template)

        # Calculate composite score (0-100)
        composite_score = (
                accuracy * 100 * self.accuracy_weight +
                speed * 100 * self.speed_weight
        )

        # Apply time bonus for exam mode
        if session.mode == TrainingMode.EXAM and speed > 0.8:
            time_bonus = min(10, (speed - 0.8) * 50)  # Up to 10 bonus points
            composite_score += time_bonus

        # Ensure score is within bounds
        final_score = min(100, max(0, composite_score))

        # Determine grade
        grade = self._get_grade(final_score)

        # Generate feedback
        feedback = self._generate_feedback(session, accuracy, speed)

        # Update session object
        session.score = final_score
        session.accuracy = accuracy
        session.speed = speed
        session.end_time = datetime.now()

        return {
            'score': final_score,
            'accuracy': accuracy,
            'speed': speed,
            'grade': grade,
            'feedback': feedback,
            'passed': final_score >= 70
        }

    def _calculate_accuracy(self, session: TrainingSession, template: SandwichTemplate) -> float:
        """Calculate accuracy score (0-1)"""
        if not session.completed_steps:
            return 0.0

        total_steps = len(template.steps)
        completed_correctly = len(session.completed_steps)

        # Check for critical errors
        critical_errors = 0
        for error in session.errors:
            if error.get('critical', False):
                critical_errors += 1

        # Penalize critical errors heavily
        critical_penalty = critical_errors * 0.3

        # Base accuracy
        base_accuracy = completed_correctly / total_steps

        # Apply penalties
        final_accuracy = max(0, base_accuracy - critical_penalty)

        return final_accuracy

    def _calculate_speed(self, session: TrainingSession, template: SandwichTemplate) -> float:
        """Calculate speed score (0-1)"""
        if not session.start_time or not session.end_time:
            return 0.0

        # Calculate actual time taken
        actual_time = (session.end_time - session.start_time).total_seconds()

        # Target time from template
        target_time = template.total_time_target

        if actual_time <= target_time:
            # Finished on time or early
            return 1.0
        else:
            # Penalize for overtime
            overtime = actual_time - target_time
            # Exponential decay for overtime penalty
            speed_score = max(0, 1.0 - (overtime / target_time))
            return speed_score

    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def _generate_feedback(self, session: TrainingSession, accuracy: float, speed: float) -> str:
        """Generate personalized feedback based on performance"""

        feedback_parts = []

        # Accuracy feedback
        if accuracy >= 0.9:
            feedback_parts.append("Excellent accuracy! Perfect assembly sequence.")
        elif accuracy >= 0.7:
            feedback_parts.append("Good accuracy. Minor improvements needed in placement.")
        elif accuracy >= 0.5:
            feedback_parts.append("Focus on correct ingredient placement and order.")
        else:
            feedback_parts.append("Review the assembly sequence and try again.")

        # Speed feedback
        if speed >= 0.9:
            feedback_parts.append("Great speed! Well within target time.")
        elif speed >= 0.7:
            feedback_parts.append("Good pace. Could improve efficiency.")
        elif speed >= 0.5:
            feedback_parts.append("Work on reducing assembly time.")
        else:
            feedback_parts.append("Too slow. Practice to improve speed.")

        # Error-specific feedback
        if session.errors:
            common_errors = [e.get('type', 'unknown') for e in session.errors[:3]]
            feedback_parts.append(f"Watch out for: {', '.join(common_errors)}")

        return " ".join(feedback_parts)

    def _get_template_by_id(self, template_id: str):
        """Helper to get template - would connect to database"""
        # Placeholder - in real app, this would query the database
        return None

    def analyze_performance_trends(self, user_id: str, sessions: List[TrainingSession]) -> Dict:
        """Analyze performance trends over time"""
        if not sessions:
            return {}

        # Calculate averages
        scores = [s.score for s in sessions]
        accuracies = [s.accuracy for s in sessions]
        speeds = [s.speed for s in sessions]

        avg_score = sum(scores) / len(scores)
        avg_accuracy = sum(accuracies) / len(accuracies)
        avg_speed = sum(speeds) / len(speeds)

        # Identify trends
        recent_sessions = sessions[-5:] if len(sessions) >= 5 else sessions
        recent_avg = sum([s.score for s in recent_sessions]) / len(recent_sessions)

        trend = "improving" if recent_avg > avg_score else "declining" if recent_avg < avg_score else "stable"

        # Identify weakest areas
        error_types = {}
        for session in sessions:
            for error in session.errors:
                error_type = error.get('type', 'unknown')
                error_types[error_type] = error_types.get(error_type, 0) + 1

        common_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            'average_score': avg_score,
            'average_accuracy': avg_accuracy,
            'average_speed': avg_speed,
            'total_sessions': len(sessions),
            'performance_trend': trend,
            'common_errors': common_errors,
            'recommendations': self._generate_recommendations(common_errors)
        }

    def _generate_recommendations(self, common_errors: List[Tuple[str, int]]) -> List[str]:
        """Generate training recommendations based on common errors"""
        recommendations = []

        error_advice = {
            'wrong_order': "Practice the assembly sequence in Guided Mode",
            'wrong_placement': "Focus on ingredient placement zones",
            'missing_ingredient': "Check each step carefully before proceeding",
            'overtime': "Work on speed without sacrificing accuracy",
            'sauce_amount': "Pay attention to sauce portion control"
        }

        for error_type, count in common_errors:
            if error_type in error_advice:
                recommendations.append(error_advice[error_type])

        return recommendations[:3]  # Return top 3 recommendations
