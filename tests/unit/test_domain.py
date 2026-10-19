import pytest
from pydantic import ValidationError

from interview_coach.domain.models import (
    Answer,
    Difficulty,
    Evaluation,
    InterviewSession,
    Question,
    Turn,
)


def make_evaluation(score: int = 7) -> Evaluation:
    return Evaluation(
        score=score,
        strengths=["clear"],
        weaknesses=["no example"],
        needs_follow_up=False,
        feedback="Good answer.",
    )


def test_evaluation_rejects_out_of_range_score() -> None:
    with pytest.raises(ValidationError):
        make_evaluation(score=15)