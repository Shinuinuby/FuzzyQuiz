
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# STEP 1: Define input and output ranges

accuracy = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "accuracy"
)

response_time = ctrl.Antecedent(
    np.arange(0, 61, 1),
    "response_time"
)

difficulty = ctrl.Consequent(
    np.arange(0, 101, 1),
    "difficulty",
    defuzzify_method="centroid"
)


# STEP 2: Define accuracy membership functions

accuracy["low"] = fuzz.trapmf(
    accuracy.universe, [0, 0, 20, 50]
)

accuracy["medium"] = fuzz.trimf(
    accuracy.universe, [30, 60, 90]
)

accuracy["high"] = fuzz.trapmf(
    accuracy.universe, [60, 90, 100, 100]
)


# STEP 3: Define response-time membership functions

response_time["fast"] = fuzz.trapmf(
    response_time.universe, [0, 0, 10, 25]
)

response_time["moderate"] = fuzz.trimf(
    response_time.universe, [15, 30, 45]
)

response_time["slow"] = fuzz.trapmf(
    response_time.universe, [35, 50, 60, 60]
)


# STEP 4: Define output membership functions

difficulty["easy"] = fuzz.trapmf(
    difficulty.universe, [0, 0, 20, 40]
)

difficulty["medium"] = fuzz.trimf(
    difficulty.universe, [30, 50, 70]
)

difficulty["hard"] = fuzz.trapmf(
    difficulty.universe, [60, 80, 100, 100]
)


# STEP 5: Create Mamdani fuzzy rules

rules = [
    ctrl.Rule(
        accuracy["low"] & response_time["fast"],
        difficulty["easy"]
    ),
    ctrl.Rule(
        accuracy["low"] & response_time["moderate"],
        difficulty["easy"]
    ),
    ctrl.Rule(
        accuracy["low"] & response_time["slow"],
        difficulty["easy"]
    ),
    ctrl.Rule(
        accuracy["medium"] & response_time["fast"],
        difficulty["medium"]
    ),
    ctrl.Rule(
        accuracy["medium"] & response_time["moderate"],
        difficulty["medium"]
    ),
    ctrl.Rule(
        accuracy["medium"] & response_time["slow"],
        difficulty["easy"]
    ),
    ctrl.Rule(
        accuracy["high"] & response_time["fast"],
        difficulty["hard"]
    ),
    ctrl.Rule(
        accuracy["high"] & response_time["moderate"],
        difficulty["hard"]
    ),
    ctrl.Rule(
        accuracy["high"] & response_time["slow"],
        difficulty["medium"]
    )
]


# STEP 6: Build the fuzzy control system

fuzzy_system = ctrl.ControlSystem(rules)


# STEP 7: Function used by FuzzyQuiz

def recommend_difficulty(accuracy_value, avg_time):

    if not 0 <= accuracy_value <= 100:
        raise ValueError(
            "Accuracy must be between 0 and 100."
        )

    if avg_time < 0:
        raise ValueError(
            "Response time cannot be negative."
        )

    # Values above 60 seconds are treated as 60
    avg_time = min(avg_time, 60)

    simulation = ctrl.ControlSystemSimulation(
        fuzzy_system
    )

    simulation.input["accuracy"] = accuracy_value
    simulation.input["response_time"] = avg_time

    simulation.compute()

    fuzzy_score = float(
        simulation.output["difficulty"]
    )

    # Convert numerical output to difficulty
    if fuzzy_score < 40:
        recommended = "Easy"

    elif fuzzy_score < 60:
        recommended = "Medium"

    else:
        recommended = "Hard"

    return {
        "difficulty": recommended,
        "fuzzy_score": round(fuzzy_score, 2),
        "accuracy": round(accuracy_value, 2),
        "average_time": round(avg_time, 2)
    }
