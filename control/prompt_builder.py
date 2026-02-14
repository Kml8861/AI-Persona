from control.behavior import BehaviorDecision


# STM:
decision = {
    "mode": "ANALYSIS",
    "style": "FORMAL",
    "verbosity": "high"
}


def build_behavior_prompt(decision: BehaviorDecision, wm_focus: str = None, ltm_snippets: list = None):
    parts = []

    if decision.mode:
        parts.append(f"You are operating in {decision.mode.value} mode.")
    if decision.style:
        parts.append(f"Adopt a {decision.style.value.replace('_',' ')} communication style.")
    if decision.verbosity:
        parts.append(f"Adjust responses to {decision.verbosity} detail.")
    if decision.temperature_shift:
        parts.append(f"Shift temperature by {decision.temperature_shift}.")

    if wm_focus:
        parts.append(f"Focus on: {wm_focus}.")
    if ltm_snippets:
        parts.append(f"Relevant memories: {', '.join(ltm_snippets)}")

    return {"role": "system", "content": " ".join(parts)}