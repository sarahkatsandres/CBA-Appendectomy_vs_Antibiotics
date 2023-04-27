## COPIED FROM HW 12 SOLUTION

from enum import Enum

import numpy as np

# simulation settings
POP_SIZE = 5000         # cohort population size
SIM_LENGTH = 25    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

ANNUAL_PROB_ALL_CAUSE_MORT = 41.4 / 1000
ANNUAL_PROB_STROKE_MORT = 36.2 / 100000
ANNUAL_PROB_FIRST_STROKE = 25 / 1000
PROB_SURVIVE_FIRST_STROKE = 0.75
PROB_SURVIVE_RECURRENT_STROKE = 0.7
FIVE_YEAR_PROB_RECURRENT_STROKE = 0.35
STROKE_DURATION = 1/52  # 1 week

ANTICOAG_STROKE_REDUCTION = 0.75  # % reduction
ANTICOAG_BLEEDING_DEATH_INCREASE = 0.05  # % increase


class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    STROKE_DEAD = 3
    NATURAL_DEATH = 4


ANNUAL_STATE_UTILITY = [
    1,          # WEL
    0.2,        # STROKE
    0.9,        # POST-STROKE
    0,          # STROKE DEATH
    0]          # NATURAL DEATH

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,      # WELL
    0,      # STROKE
    200,    # POST-STROKE
    0,      # STROKE DEATH
    0       # NATURAL DEATH
]

ANTICOAG_COST = 3000
STROKE_COST = 5000