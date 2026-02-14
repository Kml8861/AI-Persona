from dataclasses import dataclass
from typing import Dict

@dataclass
class AffectState:
    vector: Dict[str, float]  # np. {'joy': 0.3, 'sadness': 0.1, 'anger': 0.0}

    def update_from_memory(self, wm_snapshot, stm_snapshot, ltm_events):
        # przykład prostej logiki: emocje rosną przy refleksji, maleją przy nudzie
        joy = 0.1 + (0.2 if stm_snapshot.get("is_reflective") else 0.0)
        sadness = 0.1 + (0.3 if stm_snapshot.get("is_analytical") else 0.0)
        # uwzględniamy LTM
        for e in ltm_events:
            if e.type == LTMEventType.EMOTION:
                joy += 0.05 * e.importance
        self.vector = {"joy": joy, "sadness": sadness, "anger": 0.0}