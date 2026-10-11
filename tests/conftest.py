import pytest

from ultron.brain.brain import Brain
from ultron.trainer.trainer import Trainer


@pytest.fixture(scope="session")
def trained():
    """One fully trained brain shared by the tests that need it."""
    brain = Brain()
    trainer = Trainer(brain)
    trainer.run_all()
    return brain, trainer.results
