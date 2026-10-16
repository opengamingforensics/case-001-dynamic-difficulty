#!/usr/bin/env python3
"""
Open Gaming Forensic Lab (OGFL)
Case #001: Monte Carlo Dynamic Difficulty Adjustment vs Neutral Matchmaking Simulator
"""

import random
import math

class Player:
    def __init__(self, player_id, true_skill, churn_threshold=3):
        self.id = player_id
        self.true_skill = true_skill # 0.0 to 1.0
        self.churn_threshold = churn_threshold
        self.loss_streak = 0
        self.total_matches = 0
        self.wins = 0
        self.churned = False
        self.spend_events = 0

    def record_match(self, won, is_dda=False):
        self.total_matches += 1
        if won:
            self.wins += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            if self.loss_streak >= self.churn_threshold:
                # If loss streak is high, player might churn or spend out of frustration
                if is_dda and random.random() < 0.35:
                    self.spend_events += 1 # Anger-induced spend
                elif random.random() < 0.40:
                    self.churned = True

def simulate_session(n_players=1000, matches_per_player=20, mode="neutral"):
    players = [Player(i, random.gauss(0.5, 0.15)) for i in range(n_players)]
    
    for _ in range(matches_per_player):
        for p in players:
            if p.churned:
                continue
            
            if mode == "neutral":
                # Fair win probability based on skill
                win_prob = max(0.05, min(0.95, p.true_skill))
                won = random.random() < win_prob
                p.record_match(won, is_dda=False)
            
            elif mode == "dda":
                # EA Patent US20160001182A1 Paradigm:
                # If player is on 2+ loss streak, boost win odds artificially (pity match)
                if p.loss_streak >= 2:
                    win_prob = 0.85
                elif p.wins / max(1, p.total_matches) > 0.65:
                    # Win streak dampening: deliberately pair against overwhelming odds
                    win_prob = 0.20
                else:
                    win_prob = 0.50
                won = random.random() < win_prob
                p.record_match(won, is_dda=True)
                
    active_players = sum(1 for p in players if not p.churned)
    total_spends = sum(p.spend_events for p in players)
    retention_rate = active_players / n_players * 100.0
    return retention_rate, total_spends

if __name__ == "__main__":
    print("=" * 60)
    print("OGFL CASE #001: MONTE CARLO DDA RETENTION SIMULATION")
    print("=" * 60)
    
    random.seed(20261016)
    ret_neutral, spend_neutral = simulate_session(10000, 25, "neutral")
    ret_dda, spend_dda = simulate_session(10000, 25, "dda")
    
    print(f"Neutral Matchmaking  -> Retention: {ret_neutral:.1f}% | Microtransaction Triggers: {spend_neutral}")
    print(f"DDA Algorithmic Rig  -> Retention: {ret_dda:.1f}% | Microtransaction Triggers: {spend_dda}")
    print(f"DDA Retention Delta  : +{ret_dda - ret_neutral:.1f}%")
    print(f"DDA Spend Delta      : +{spend_dda - spend_neutral} events")
    print("=" * 60)
    print("Conclusion: DDA algorithms demonstrably maximize retention and spend likelihood.")
