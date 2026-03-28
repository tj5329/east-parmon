#!/usr/bin/env python3
"""Hardwood Dynasty: Interactive basketball management and career sim.

Text-based game inspired by MyNBA/MyGM concepts:
- Real teams, players, and coaches (seed data)
- Three modes: GM, Player Career, Coach Career
- Multi-season simulation with drafted generated prospects
- "Encrypted" face/avatar IDs for players and coaches
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


POSITIONS = ["PG", "SG", "SF", "PF", "C"]

FIRST_NAMES = [
    "Jalen",
    "Kai",
    "Mason",
    "Rico",
    "Ethan",
    "Noah",
    "Avery",
    "Luca",
    "Darius",
    "Malik",
    "Zion",
    "Isaiah",
    "Elijah",
    "Carter",
]

LAST_NAMES = [
    "Brooks",
    "Washington",
    "Hunter",
    "Miles",
    "King",
    "Cole",
    "Turner",
    "Johnson",
    "Pierce",
    "Evans",
    "Baker",
    "Reed",
    "Parker",
    "Davis",
]


@dataclass
class Player:
    name: str
    position: str
    rating: int
    age: int
    salary: int
    is_generated: bool = False
    badge: str = ""

    def encrypted_face_id(self) -> str:
        base = f"{self.name}|{self.position}|{self.age}|player"
        return hashlib.sha256(base.encode()).hexdigest()[:14]

    def season_progress(self) -> None:
        if self.age <= 27:
            growth = random.randint(0, 3)
        elif self.age <= 31:
            growth = random.randint(-1, 2)
        else:
            growth = random.randint(-3, 1)

        self.rating = max(62, min(99, self.rating + growth))
        self.age += 1


@dataclass
class Coach:
    name: str
    style: str
    iq: int
    salary: int

    def encrypted_avatar_id(self) -> str:
        base = f"{self.name}|{self.style}|coach"
        return hashlib.sha256(base.encode()).hexdigest()[:14]

    def season_progress(self) -> None:
        self.iq = max(65, min(99, self.iq + random.randint(-1, 2)))


@dataclass
class Team:
    name: str
    coach: Coach
    roster: List[Player]
    chemistry: int = 72
    wins: int = 0
    losses: int = 0

    def team_rating(self) -> int:
        core = sorted([p.rating for p in self.roster], reverse=True)[:8]
        return int(sum(core) / len(core)) if core else 70

    def payroll(self) -> int:
        return sum(p.salary for p in self.roster) + self.coach.salary

    def reset_record(self) -> None:
        self.wins, self.losses = 0, 0


@dataclass
class League:
    teams: List[Team]
    season: int = 2026
    free_agents: List[Player] = field(default_factory=list)

    def standings(self) -> List[Team]:
        return sorted(self.teams, key=lambda t: (t.wins, t.team_rating()), reverse=True)


def make_player(name: str, pos: str, ovr: int, age: int, salary: int, badge: str = "") -> Player:
    return Player(name=name, position=pos, rating=ovr, age=age, salary=salary, badge=badge)


def seed_league() -> League:
    teams = [
        Team(
            "Los Angeles Lakers",
            Coach("JJ Redick", "Pace & Space", 81, 8),
            [
                make_player("LeBron James", "SF", 95, 41, 48, "Legend Floor General"),
                make_player("Luka Doncic", "PG", 97, 27, 51, "Magician"),
                make_player("Anthony Davis", "PF", 94, 33, 50, "Paint Dominator"),
                make_player("Austin Reaves", "SG", 84, 28, 17, "Shot Creator"),
                make_player("Rui Hachimura", "PF", 79, 28, 16, "Midrange Maestro"),
            ],
        ),
        Team(
            "Golden State Warriors",
            Coach("Steve Kerr", "Motion Offense", 90, 9),
            [
                make_player("Stephen Curry", "PG", 96, 38, 56, "Deep Range Deadeye"),
                make_player("Jimmy Butler", "SF", 90, 37, 45, "Two-Way Wing"),
                make_player("Draymond Green", "PF", 82, 36, 24, "Defensive Anchor"),
                make_player("Brandin Podziemski", "SG", 79, 23, 6, "Glue Guy"),
                make_player("Jonathan Kuminga", "SF", 84, 24, 24, "Athletic Freak"),
            ],
        ),
        Team(
            "Boston Celtics",
            Coach("Joe Mazzulla", "5-Out Attack", 87, 7),
            [
                make_player("Jayson Tatum", "SF", 95, 28, 54, "Franchise Scorer"),
                make_player("Jaylen Brown", "SG", 92, 29, 52, "Slasher"),
                make_player("Kristaps Porzingis", "C", 87, 31, 31, "Stretch Big"),
                make_player("Derrick White", "SG", 86, 32, 19, "Two-Way Guard"),
                make_player("Jrue Holiday", "PG", 84, 36, 34, "Perimeter Lock"),
            ],
        ),
        Team(
            "Denver Nuggets",
            Coach("Michael Malone", "Inside-Out", 88, 8),
            [
                make_player("Nikola Jokic", "C", 98, 31, 55, "Sombor Shuffle"),
                make_player("Jamal Murray", "PG", 89, 29, 38, "Clutch Shotmaker"),
                make_player("Aaron Gordon", "PF", 84, 30, 25, "Lob Threat"),
                make_player("Michael Porter Jr.", "SF", 83, 28, 30, "Sniper"),
                make_player("Christian Braun", "SG", 80, 25, 7, "Hustle Engine"),
            ],
        ),
        Team(
            "Milwaukee Bucks",
            Coach("Doc Rivers", "Halfcourt Balance", 84, 10),
            [
                make_player("Giannis Antetokounmpo", "PF", 97, 32, 57, "Greek Freak"),
                make_player("Damian Lillard", "PG", 90, 36, 58, "Logo Shooter"),
                make_player("Khris Middleton", "SF", 83, 35, 34, "Three-Level Scorer"),
                make_player("Brook Lopez", "C", 80, 38, 23, "Rim Protector"),
                make_player("Bobby Portis", "PF", 82, 31, 12, "Energy Big"),
            ],
        ),
        Team(
            "Miami Heat",
            Coach("Erik Spoelstra", "Culture Defense", 93, 11),
            [
                make_player("Tyler Herro", "SG", 86, 27, 32, "Microwave"),
                make_player("Bam Adebayo", "C", 90, 29, 38, "Switchable Big"),
                make_player("Terry Rozier", "PG", 81, 32, 25, "Scoring Guard"),
                make_player("Jaime Jaquez Jr.", "SF", 79, 24, 5, "Smart Cutter"),
                make_player("Andrew Wiggins", "SF", 80, 31, 26, "Two-Way Athlete"),
            ],
        ),
    ]
    return League(teams=teams)


def safe_int(prompt: str, low: int, high: int) -> int:
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            val = int(raw)
            if low <= val <= high:
                return val
        print(f"Enter a number from {low} to {high}.")


def print_team_sheet(team: Team) -> None:
    print(f"\n=== {team.name} ===")
    print(f"Coach: {team.coach.name} ({team.coach.style}, IQ {team.coach.iq})")
    print(f"Encrypted coach avatar: {team.coach.encrypted_avatar_id()}")
    print(f"Team OVR: {team.team_rating()} | Chemistry: {team.chemistry} | Payroll: ${team.payroll()}M")
    for idx, p in enumerate(sorted(team.roster, key=lambda x: x.rating, reverse=True), start=1):
        origin = "Generated" if p.is_generated else "Real"
        print(
            f"{idx:>2}. {p.name:<22} {p.position} OVR {p.rating} Age {p.age} ${p.salary}M "
            f"[{origin}] [{p.badge}]"
        )
        print(f"    face-id: {p.encrypted_face_id()}")


def off_season(league: League) -> None:
    for team in league.teams:
        for p in team.roster:
            p.season_progress()
        team.coach.season_progress()
        team.chemistry = max(50, min(99, team.chemistry + random.randint(-3, 4)))

    generate_rookie_class(league, 12)
    draft_new_players(league)
    league.season += 1


def generate_rookie_class(league: League, count: int) -> None:
    rookies: List[Player] = []
    for _ in range(count):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        pos = random.choice(POSITIONS)
        rating = random.randint(72, 85)
        age = random.randint(19, 21)
        salary = random.randint(4, 10)
        badge = random.choice([
            "Rising Star",
            "Defensive Menace",
            "Elite Potential",
            "Athletic Freak",
            "Playmaking Gene",
        ])
        rookies.append(Player(name, pos, rating, age, salary, True, badge))

    rookies.sort(key=lambda p: p.rating, reverse=True)
    league.free_agents = rookies


def draft_new_players(league: League) -> None:
    order = sorted(league.teams, key=lambda t: t.wins)
    for team in order:
        if not league.free_agents:
            break
        pick = league.free_agents.pop(0)
        weakest = min(team.roster, key=lambda p: p.rating)
        team.roster.remove(weakest)
        team.roster.append(pick)



def simulate_regular_season(league: League) -> None:
    for team in league.teams:
        team.reset_record()

    for i, team_a in enumerate(league.teams):
        for j, team_b in enumerate(league.teams):
            if i >= j:
                continue
            for _ in range(4):
                score_a = team_a.team_rating() + random.randint(-12, 12) + team_a.chemistry // 12
                score_b = team_b.team_rating() + random.randint(-12, 12) + team_b.chemistry // 12
                if score_a >= score_b:
                    team_a.wins += 1
                    team_b.losses += 1
                else:
                    team_b.wins += 1
                    team_a.losses += 1


def play_in_game(user_team: Team, opponent: Team) -> bool:
    user_power = user_team.team_rating() + user_team.coach.iq // 10 + random.randint(-8, 8)
    opp_power = opponent.team_rating() + opponent.coach.iq // 10 + random.randint(-8, 8)

    print(f"\nPlayoff game: {user_team.name} vs {opponent.name}")
    print("Choose gameplan:")
    print("1) Attack the paint (+chemistry boost chance)")
    print("2) Pace-and-space (high variance)")
    print("3) Defensive grind (+coach IQ bonus)")
    plan = safe_int("Plan: ", 1, 3)

    if plan == 1:
        user_power += random.randint(0, 6)
        if random.random() < 0.35:
            user_team.chemistry = min(99, user_team.chemistry + 2)
    elif plan == 2:
        user_power += random.randint(-6, 10)
    else:
        user_power += user_team.coach.iq // 8

    won = user_power >= opp_power
    print("Result:", "WIN ✅" if won else "LOSS ❌")
    return won


def gm_mode(league: League) -> None:
    print("\n=== GM MODE ===")
    team = choose_team(league)

    while True:
        print(f"\n--- Season {league.season} | {team.name} GM Hub ---")
        print("1) View team sheet")
        print("2) Training focus")
        print("3) Simulate regular season")
        print("4) End season + offseason")
        print("5) Back to main menu")
        choice = safe_int("Choose: ", 1, 5)

        if choice == 1:
            print_team_sheet(team)
        elif choice == 2:
            apply_training(team)
        elif choice == 3:
            simulate_regular_season(league)
            show_standings(league)
            run_playoffs_for_team(league, team)
        elif choice == 4:
            off_season(league)
            print(f"Offseason complete. Welcome to {league.season}.")
        else:
            return


def apply_training(team: Team) -> None:
    print("\nChoose a player to train:")
    for i, p in enumerate(team.roster, start=1):
        print(f"{i}) {p.name} ({p.position}) OVR {p.rating}")
    idx = safe_int("Player #: ", 1, len(team.roster)) - 1

    print("Training package:")
    print("1) Shooting Lab")
    print("2) Strength & Defense")
    print("3) Playmaking Vision")
    pkg = safe_int("Package: ", 1, 3)

    boost = random.randint(1, 3)
    if pkg == 2 and team.roster[idx].position in {"C", "PF"}:
        boost += 1
    team.roster[idx].rating = min(99, team.roster[idx].rating + boost)
    team.chemistry = min(99, team.chemistry + 1)
    print(f"{team.roster[idx].name} improved to {team.roster[idx].rating} OVR.")


def player_career_mode(league: League) -> None:
    print("\n=== PLAYER CAREER MODE ===")
    team = choose_team(league)
    print(f"Pick your controlled player on {team.name}:")
    for i, p in enumerate(team.roster, start=1):
        print(f"{i}) {p.name} - {p.position} OVR {p.rating}")
    player = team.roster[safe_int("Player #: ", 1, len(team.roster)) - 1]

    while True:
        print(f"\n{player.name} Career Hub | Season {league.season}")
        print("1) Show profile")
        print("2) Skill workout")
        print("3) Sim season")
        print("4) Advance to next season")
        print("5) Back to main menu")
        c = safe_int("Choose: ", 1, 5)
        if c == 1:
            print(
                f"{player.name} | {player.position} | OVR {player.rating} | Age {player.age} | "
                f"Badge: {player.badge}\nEncrypted face: {player.encrypted_face_id()}"
            )
        elif c == 2:
            growth = random.randint(1, 4)
            player.rating = min(99, player.rating + growth)
            print(f"Grind session complete. +{growth} OVR => {player.rating}")
        elif c == 3:
            simulate_regular_season(league)
            show_standings(league)
            run_playoffs_for_team(league, team)
        elif c == 4:
            off_season(league)
            if player.age > 38 and random.random() < 0.5:
                print(f"{player.name} retired. Career complete. Legendary run!")
                return
            print(f"New season: {league.season}")
        else:
            return


def coach_career_mode(league: League) -> None:
    print("\n=== COACH CAREER MODE ===")
    team = choose_team(league)
    coach = team.coach

    while True:
        print(f"\nCoach {coach.name} Hub | Season {league.season}")
        print("1) View coach profile")
        print("2) Install team scheme")
        print("3) Sim season")
        print("4) Next season")
        print("5) Back to main menu")
        c = safe_int("Choose: ", 1, 5)
        if c == 1:
            print(
                f"{coach.name} | Style: {coach.style} | IQ {coach.iq} | "
                f"Encrypted avatar: {coach.encrypted_avatar_id()}"
            )
        elif c == 2:
            change_scheme(team)
        elif c == 3:
            simulate_regular_season(league)
            show_standings(league)
            run_playoffs_for_team(league, team)
        elif c == 4:
            off_season(league)
            print(f"Welcome to season {league.season}")
        else:
            return


def change_scheme(team: Team) -> None:
    print("Schemes:")
    schemes = ["Pace & Space", "Switch Everything", "Inside-Out", "Princeton Motion"]
    for i, s in enumerate(schemes, start=1):
        print(f"{i}) {s}")
    pick = safe_int("Scheme #: ", 1, len(schemes)) - 1
    team.coach.style = schemes[pick]
    iq_boost = random.randint(0, 2)
    chem_boost = random.randint(1, 3)
    team.coach.iq = min(99, team.coach.iq + iq_boost)
    team.chemistry = min(99, team.chemistry + chem_boost)
    print(f"New scheme set. IQ +{iq_boost}, chemistry +{chem_boost}.")


def choose_team(league: League) -> Team:
    print("\nSelect a team:")
    for i, t in enumerate(league.teams, start=1):
        print(f"{i}) {t.name} (OVR {t.team_rating()}) Coach: {t.coach.name}")
    idx = safe_int("Team #: ", 1, len(league.teams)) - 1
    return league.teams[idx]


def show_standings(league: League) -> None:
    print(f"\n=== {league.season} Standings ===")
    for rank, t in enumerate(league.standings(), start=1):
        print(f"{rank}. {t.name:25} {t.wins:>2}-{t.losses:<2} OVR {t.team_rating()}")


def run_playoffs_for_team(league: League, user_team: Team) -> None:
    top4 = league.standings()[:4]
    if user_team not in top4:
        print(f"{user_team.name} missed the playoffs.")
        return

    seed = top4.index(user_team) + 1
    print(f"{user_team.name} made playoffs as seed #{seed}.")

    opponents = [t for t in top4 if t is not user_team]
    random.shuffle(opponents)
    for rnd, opp in enumerate(opponents[:2], start=1):
        print(f"\nRound {rnd}")
        if not play_in_game(user_team, opp):
            print("Eliminated from playoffs.")
            return
    print("🏆 CHAMPIONS! Dynasty points +1")


def main() -> None:
    print("🏀 HARDWOOD DYNASTY: MYGM CAREER SIM")
    print("Build a dynasty in GM, Player Career, or Coach Career mode.")

    league = seed_league()

    while True:
        print("\nMain Menu")
        print("1) GM Mode")
        print("2) Player Career Mode")
        print("3) Coach Career Mode")
        print("4) Quit")
        choice = safe_int("Choose: ", 1, 4)

        if choice == 1:
            gm_mode(league)
        elif choice == 2:
            player_career_mode(league)
        elif choice == 3:
            coach_career_mode(league)
        else:
            print("Thanks for playing Hardwood Dynasty.")
            break


if __name__ == "__main__":
    random.seed()
    main()
