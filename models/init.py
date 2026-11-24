# Import every model so Base.metadata knows about all tables
# (needed for create_all and for string-based relationships to resolve).
from .member import Member
from .fitness_goal import FitnessGoal
from .health_metric import HealthMetric
from .trainer import Trainer
from .admin import Admin
