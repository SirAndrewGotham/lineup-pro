import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

from core.models import *

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "lineup_pro.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def initialize(self):
        """Initialize database with schema"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.create_tables()
        self.create_indexes()

        # Seed with universal templates if empty
        if self.is_database_empty():
            self.seed_universal_templates()

        logger.info("Database initialized successfully")

    def create_tables(self):
        """Create all database tables"""

        # Users table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                                                 id TEXT PRIMARY KEY,
                                                                 name TEXT NOT NULL,
                                                                 role TEXT DEFAULT 'trainee',
                                                                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                            ''')

        # Ingredients table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS ingredients (
                                                                       id TEXT PRIMARY KEY,
                                                                       name TEXT NOT NULL,
                                                                       type TEXT NOT NULL,
                                                                       image_path TEXT,
                                                                       calories INTEGER DEFAULT 0,
                                                                       allergens TEXT DEFAULT '[]',
                                                                       placement_zones TEXT DEFAULT '["center"]'
                            )
                            ''')

        # Sandwich templates table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS templates (
                                                                     id TEXT PRIMARY KEY,
                                                                     name TEXT NOT NULL,
                                                                     station TEXT NOT NULL,
                                                                     difficulty INTEGER DEFAULT 1,
                                                                     total_time_target INTEGER DEFAULT 60,
                                                                     steps TEXT NOT NULL,  -- JSON array of AssemblyStep
                                                                     description TEXT,
                                                                     image_path TEXT,
                                                                     common_errors TEXT DEFAULT '[]',
                                                                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                            ''')

        # Training sessions table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS training_sessions (
                                                                             id TEXT PRIMARY KEY,
                                                                             user_id TEXT NOT NULL,
                                                                             template_id TEXT NOT NULL,
                                                                             mode TEXT NOT NULL,
                                                                             start_time TIMESTAMP NOT NULL,
                                                                             end_time TIMESTAMP,
                                                                             score REAL DEFAULT 0.0,
                                                                             accuracy REAL DEFAULT 0.0,
                                                                             speed REAL DEFAULT 0.0,
                                                                             errors TEXT DEFAULT '[]',
                                                                             completed_steps TEXT DEFAULT '[]',
                                                                             FOREIGN KEY (user_id) REFERENCES users (id),
                                FOREIGN KEY (template_id) REFERENCES templates (id)
                                )
                            ''')

        # User progress table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user_progress (
                                                                         user_id TEXT PRIMARY KEY,
                                                                         templates_mastered TEXT DEFAULT '{}',
                                                                         total_sessions INTEGER DEFAULT 0,
                                                                         average_accuracy REAL DEFAULT 0.0,
                                                                         average_speed REAL DEFAULT 0.0,
                                                                         skill_matrix TEXT DEFAULT '{}',
                                                                         last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                                         FOREIGN KEY (user_id) REFERENCES users (id)
                                )
                            ''')

        self.conn.commit()

    def create_indexes(self):
        """Create performance indexes"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_sessions_user ON training_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_template ON training_sessions(template_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_time ON training_sessions(start_time)",
            "CREATE INDEX IF NOT EXISTS idx_templates_station ON templates(station)",
            "CREATE INDEX IF NOT EXISTS idx_templates_difficulty ON templates(difficulty)"
        ]

        for index_sql in indexes:
            self.cursor.execute(index_sql)

        self.conn.commit()

    def is_database_empty(self) -> bool:
        """Check if database needs seeding"""
        self.cursor.execute("SELECT COUNT(*) as count FROM templates")
        result = self.cursor.fetchone()
        return result['count'] == 0

    def seed_universal_templates(self):
        """Seed database with 5 universal sandwich templates"""
        from data.seed_data import UNIVERSAL_TEMPLATES

        for template in UNIVERSAL_TEMPLATES:
            self.save_template(template)

        logger.info(f"Seeded {len(UNIVERSAL_TEMPLATES)} universal templates")

    def save_template(self, template: SandwichTemplate):
        """Save or update a sandwich template"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO templates 
            (id, name, station, difficulty, total_time_target, steps, description, image_path, common_errors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            template.id,
            template.name,
            template.station,
            template.difficulty,
            template.total_time_target,
            json.dumps([step.__dict__ for step in template.steps]),
            template.description,
            template.image_path,
            json.dumps(template.common_errors)
        ))
        self.conn.commit()

    def get_template(self, template_id: str) -> Optional[SandwichTemplate]:
        """Retrieve a template by ID"""
        self.cursor.execute(
            "SELECT * FROM templates WHERE id = ?",
            (template_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._row_to_template(row)

    def get_all_templates(self, station: str = None, difficulty: int = None) -> List[SandwichTemplate]:
        """Retrieve all templates with optional filters"""
        query = "SELECT * FROM templates"
        params = []

        if station or difficulty:
            query += " WHERE"
            conditions = []

            if station:
                conditions.append("station = ?")
                params.append(station)

            if difficulty:
                conditions.append("difficulty = ?")
                params.append(difficulty)

            query += " " + " AND ".join(conditions)

        query += " ORDER BY difficulty, name"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        return [self._row_to_template(row) for row in rows]

    def _row_to_template(self, row) -> SandwichTemplate:
        """Convert database row to SandwichTemplate object"""
        steps_data = json.loads(row['steps'])
        steps = []

        for step_data in steps_data:
            # Here you would need to fetch the ingredient object
            # For simplicity, we'll create a placeholder
            ingredient = Ingredient(
                id=step_data['ingredient']['id'],
                name=step_data['ingredient']['name'],
                type=IngredientType(step_data['ingredient']['type']),
                image_path=step_data['ingredient']['image_path']
            )

            step = AssemblyStep(
                order=step_data['order'],
                ingredient=ingredient,
                placement=step_data['placement'],
                quantity=step_data.get('quantity', 1),
                time_target=step_data.get('time_target', 5),
                points=step_data.get('points', 10),
                critical=step_data.get('critical', True)
            )
            steps.append(step)

        return SandwichTemplate(
            id=row['id'],
            name=row['name'],
            station=row['station'],
            difficulty=row['difficulty'],
            total_time_target=row['total_time_target'],
            steps=steps,
            description=row['description'],
            image_path=row['image_path'],
            common_errors=json.loads(row['common_errors'])
        )

    def save_session(self, session: TrainingSession):
        """Save training session to database"""
        self.cursor.execute('''
                            INSERT INTO training_sessions
                            (id, user_id, template_id, mode, start_time, end_time, score, accuracy, speed, errors, completed_steps)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                session.id,
                                session.user_id,
                                session.template_id,
                                session.mode.value,
                                session.start_time.isoformat(),
                                session.end_time.isoformat() if session.end_time else None,
                                session.score,
                                session.accuracy,
                                session.speed,
                                json.dumps(session.errors),
                                json.dumps(session.completed_steps)
                            ))

        # Update user progress
        self.update_user_progress(session)

        self.conn.commit()

    def update_user_progress(self, session: TrainingSession):
        """Update user progress based on session results"""
        # Get current progress
        self.cursor.execute(
            "SELECT * FROM user_progress WHERE user_id = ?",
            (session.user_id,)
        )
        row = self.cursor.fetchone()

        if row:
            templates_mastered = json.loads(row['templates_mastered'])
            total_sessions = row['total_sessions'] + 1

            # Update best score for this template
            current_best = templates_mastered.get(session.template_id, 0)
            if session.score > current_best:
                templates_mastered[session.template_id] = session.score

            # Calculate new averages
            old_accuracy = row['average_accuracy']
            old_speed = row['average_speed']
            new_accuracy = (old_accuracy * (total_sessions - 1) + session.accuracy) / total_sessions
            new_speed = (old_speed * (total_sessions - 1) + session.speed) / total_sessions

            self.cursor.execute('''
                                UPDATE user_progress
                                SET templates_mastered = ?, total_sessions = ?, average_accuracy = ?, average_speed = ?, last_updated = CURRENT_TIMESTAMP
                                WHERE user_id = ?
                                ''', (
                                    json.dumps(templates_mastered),
                                    total_sessions,
                                    new_accuracy,
                                    new_speed,
                                    session.user_id
                                ))
        else:
            # First session for this user
            templates_mastered = {session.template_id: session.score}
            self.cursor.execute('''
                                INSERT INTO user_progress
                                (user_id, templates_mastered, total_sessions, average_accuracy, average_speed)
                                VALUES (?, ?, 1, ?, ?)
                                ''', (
                                    session.user_id,
                                    json.dumps(templates_mastered),
                                    session.accuracy,
                                    session.speed
                                ))

    def get_user_progress(self, user_id: str) -> Optional[UserProgress]:
        """Get user progress statistics"""
        self.cursor.execute(
            "SELECT * FROM user_progress WHERE user_id = ?",
            (user_id,)
        )
        row = self.cursor.fetchone()

        if not row:
            return None

        return UserProgress(
            user_id=row['user_id'],
            templates_mastered=json.loads(row['templates_mastered']),
            total_sessions=row['total_sessions'],
            average_accuracy=row['average_accuracy'],
            average_speed=row['average_speed'],
            skill_matrix=json.loads(row['skill_matrix'])
        )

    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get recent training sessions for a user"""
        self.cursor.execute('''
                            SELECT s.*, t.name as template_name
                            FROM training_sessions s
                                     JOIN templates t ON s.template_id = t.id
                            WHERE s.user_id = ?
                            ORDER BY s.start_time DESC
                                LIMIT ?
                            ''', (user_id, limit))

        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
