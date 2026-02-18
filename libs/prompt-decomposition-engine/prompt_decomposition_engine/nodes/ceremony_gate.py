"""
Ceremony Gate

Graph-level value gate that checks whether a decomposed prompt
can proceed to execution or needs ceremonial pause.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from prompt_decomposition.action_stack import DecompositionResult
from prompt_decomposition_engine.nodes.perspective_nodes import ThreeUniversePerspective


class GateDecision(str, Enum):
    PROCEED = "proceed"
    CAUTION = "caution"
    HOLD = "hold"


@dataclass
class CeremonyGateResult:
    decision: GateDecision
    reasons: List[str]
    relational_score: float
    ceremony_needed: bool
    human_review_requested: bool


class CeremonyGate:
    """Evaluates whether a decomposition can proceed to execution."""

    def __init__(
        self,
        balance_threshold: float = 0.4,
        coherence_threshold: float = 0.3,
        enforce: bool = False,
    ):
        self.balance_threshold = balance_threshold
        self.coherence_threshold = coherence_threshold
        self.enforce = enforce

    def evaluate(
        self,
        decomposition: DecompositionResult,
        perspective: Optional[ThreeUniversePerspective] = None,
    ) -> CeremonyGateResult:
        reasons: List[str] = []
        relational_score = decomposition.balance
        ceremony_needed = False
        human_review_requested = False

        if decomposition.balance < self.balance_threshold:
            reasons.append(
                f"Balance ({decomposition.balance * 100:.0f}%) below threshold "
                f"({self.balance_threshold * 100:.0f}%)"
            )

        if decomposition.neglected_directions:
            dirs = ", ".join(d.value for d in decomposition.neglected_directions)
            reasons.append(f"Neglected directions: {dirs}")

        lower = decomposition.prompt.lower()
        ceremony_kws = ["indigenous", "ceremony", "medicine wheel", "elder", "sacred", "protocol"]
        has_ceremony_domain = any(kw in lower for kw in ceremony_kws)

        if has_ceremony_domain and not decomposition.directions.get("west"):
            reasons.append("Indigenous/ceremonial domain work without validation/reflection dimension")
            ceremony_needed = True
            human_review_requested = True

        if perspective:
            relational_score = (decomposition.balance + perspective.coherence) / 2.0

            if perspective.coherence < self.coherence_threshold:
                reasons.append(
                    f"Three-universe coherence ({perspective.coherence * 100:.0f}%) below threshold"
                )

            critical = [f for i in perspective.insights for f in i.flags if "🛑" in f]
            if critical:
                reasons.extend(critical)
                ceremony_needed = True
                human_review_requested = True

            warnings = [f for i in perspective.insights for f in i.flags if "⚠️" in f]
            if warnings:
                reasons.extend(warnings)
                ceremony_needed = True

        if human_review_requested or (ceremony_needed and self.enforce):
            decision = GateDecision.HOLD
        elif reasons:
            decision = GateDecision.CAUTION
        else:
            decision = GateDecision.PROCEED

        return CeremonyGateResult(
            decision=decision,
            reasons=reasons,
            relational_score=max(0.0, min(1.0, relational_score)),
            ceremony_needed=ceremony_needed,
            human_review_requested=human_review_requested,
        )

    def can_proceed(
        self,
        decomposition: DecompositionResult,
        perspective: Optional[ThreeUniversePerspective] = None,
    ) -> bool:
        return self.evaluate(decomposition, perspective).decision != GateDecision.HOLD
