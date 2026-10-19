from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SessionStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Question(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    text: str
    topic: str
    difficulty: Difficulty
    is_follow_up: bool = False


class Answer(BaseModel):
    question_id: UUID
    text: str = Field(min_length=1)
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Evaluation(BaseModel):
    score: int = Field(ge=1, le=10)
    strengths: list[str]
    weaknesses: list[str]
    needs_follow_up: bool
    feedback: str


class Turn(BaseModel):
    question: Question
    answer: Answer | None = None
    evaluation: Evaluation | None = None


class InterviewSession(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: str  # e.g. "AI Engineer"
    status: SessionStatus = SessionStatus.IN_PROGRESS
    max_questions: int = Field(default=5, ge=1, le=20)
    turns: list[Turn] = Field(default_factory=list)

    @property
    def average_score(self) -> float | None:
        scores = [t.evaluation.score for t in self.turns if t.evaluation]
        return sum(scores) / len(scores) if scores else None