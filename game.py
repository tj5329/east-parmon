#!/usr/bin/env python3
"""Courtside Dynasty - interactive basketball franchise simulation game.

Features
- GM mode: manage roster, sign free agents, train players, play season.
- Player career mode: control a created player and progress through seasons.
- Coach mode: make tactical choices that influence outcomes.
- Uses a built-in dataset of real NBA teams, players, and coaches.
- Generates new rookie classes after each season.
- Creates encrypted avatar/face tokens for players and coaches (for flavor).
"""

from __future__ import annotations

import base64
import hashlib
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

SEED = 42
random.seed(SEED)

TEAMS = [
    "Boston Celtics",
    "Milwaukee Bucks",
    "Los Angeles Lakers",
    "Golden State Warriors",
    "Denver Nuggets",
    "Miami Heat",
]

COACHES = {
    "Boston Celtics": "Joe Mazzulla",
    "Milwaukee Bucks": "Doc Rivers",
    "Los Angeles Lakers": "JJ Redick",
    "Golden State Warriors": "Steve Kerr",
    "Denver Nuggets": "Michael Malone",
    "Miami Heat": "Erik Spoelstra",
}

PLAYERS_BY_TEAM = {
    "Boston Celtics": [
        ("Jayson Tatum", 95, "SF", 28),
        ("Jaylen Brown", 90, "SG", 29),
        ("Kristaps Porzingis", 87, "C", 30),
        ("Jrue Holiday", 86, "PG", 35),
        ("Derrick White", 85, "SG", 31),
    ],
    "Milwaukee Bucks": [
        ("Giannis Antetokounmpo", 97, "PF", 31),
        ("Damian Lillard", 91, "PG", 36),
        ("Khris Middleton", 84, "SF", 35),
        ("Brook Lopez", 82, "C", 38),
        ("Bobby Portis", 80, "PF", 32),
    ],
    "Los Angeles Lakers": [
        ("LeBron James", 95, "SF", 41),
        ("Anthony Davis", 94, "PF", 33),
        ("Austin Reaves", 84, "SG", 28),
        ("Rui Hachimura", 79, "PF", 28),
        ("D'Angelo Russell", 82, "PG", 30),
    ],
    "Golden State Warriors": [
        ("Stephen Curry", 96, "PG", 38),
        ("Draymond Green", 82, "PF", 36),
        ("Jonathan Kuminga", 81, "SF", 24),
        ("Andrew Wiggins", 81, "SF", 31),
        ("Brandin Podziemski", 78, "SG", 23),
    ],
    "Denver Nuggets": [
        ("Nikola Jokic", 98, "C", 31),
        ("Jamal Murray", 89, "PG", 29),
        ("Aaron Gordon", 83, "PF", 31),
        ("Michael Porter Jr.", 84, "SF", 28),
        ("Kentavious Caldwell-Pope", 80, "SG", 33),
    ],
    "Miami Heat": [
        ("Jimmy Butler", 90, "SF", 37),
        ("Bam Adebayo", 89, "C", 29),
        ("Tyler Herro", 86, "SG", 27),
        ("Terry Rozier", 82, "PG", 33),
        ("Jaime Jaquez Jr.", 79, "SF", 24),
    ],
}

ROOKIE_FIRST_NAMES = [
    "Jalen",
    "Tyrese",
    "Malik",
    "Cameron",
    "Isaiah",
    "Darius",
    "Jabari",
    "Collin",
    "Keegan",
    "Amen",
]

ROOKIE_LAST_NAMES = [
    "Henderson",
    "Brooks",
    "Walker",
    "Daniels",
    "Whitmore",
    "Sarr",
    "Miller",
    "George",
    "Castle",
    "Johnson",
]

POSITIONS = ["PG", "SG", "SF", "PF", "C"]


@dataclass
class Person:
    name: str
    age: int

    def encrypted_face(self, salt: str = "courtside-face") -> str:
        raw = f"{self.name}|{self.age}|{salt}".encode()
        digest = hashlib.sha256(raw).digest()
        return base64.urlsafe_b64encode(digest[:12]).decode()

    def encrypted_avatar(self, salt: str = "courtside-avatar") -> str:
        raw = f"{salt}|{self.name}|{self.age}".encode()
        digest = hashlib.blake2s(raw, digest_size=12).digest()
        return base64.urlsafe_b64encode(digest).decode()


@dataclass
class Player(Person):
    rating: int
    position: str
    potential: int
    career_points: int = 0
    career_rebounds: int = 0
    career_assists: int = 0

    def overall(self) -> int:
        return max(55, min(99, self.rating))


@dataclass
class Coach(Person):
    strategy: str = "Balanced"


@dataclass
class Team:
    name: str
    coach: Coach
    roster: List[Player] = field(default_factory=list)
    wins: int = 0
    losses: int = 0

    def power(self) -> float:
        if not self.roster:
            return 60.0
        top = sorted((p.overall() for p in self.roster), reverse=True)[:5]
        return sum(top) / len(top)

    def reset_record(self) -> None:
        self.wins = 0
        self.losses = 0


class League:
    def __init__(self) -> None:
        self.teams: Dict[str, Team] = {}
        self.free_agents: List[Player] = []
        self.year = 2026
        self._build_league()

    def _build_league(self) -> None:
        for team_name in TEAMS:
            coach = Coach(name=COACHES[team_name], age=random.randint(42, 62))
            roster = [
                Player(name=n, rating=r, position=pos, age=age, potential=min(99, r + random.randint(1, 7)))
                for (n, r, pos, age) in PLAYERS_BY_TEAM[team_name]
            ]
            self.teams[team_name] = Team(name=team_name, coach=coach, roster=roster)

        for _ in range(15):
            self.free_agents.append(self._generate_rookie(as_free_agent=True))

    def _generate_rookie(self, as_free_agent: bool = False) -> Player:
        name = f"{random.choice(ROOKIE_FIRST_NAMES)} {random.choice(ROOKIE_LAST_NAMES)}"
        base = random.randint(68, 81) if as_free_agent else random.randint(70, 84)
        potential = min(99, base + random.randint(6, 15))
        return Player(
            name=name,
            age=19,
            rating=base,
            position=random.choice(POSITIONS),
            potential=potential,
        )

    def add_rookie_class(self) -> None:
        for _ in range(12):
            rookie = self._generate_rookie(as_free_agent=True)
            self.free_agents.append(rookie)

    def age_and_progress(self) -> None:
        for team in self.teams.values():
            for p in team.roster:
                p.age += 1
                growth = random.randint(-2, 4)
                if p.age <= 25:
                    growth += 1
                if p.age >= 33:
                    growth -= 2
                p.rating = max(60, min(p.potential, p.rating + growth))

    def standings(self) -> List[Team]:
        return sorted(self.teams.values(), key=lambda t: (t.wins, t.power()), reverse=True)

    def simulate_game(self, a: Team, b: Team, coach_boost_a: float = 0.0, coach_boost_b: float = 0.0) -> Team:
        a_score = a.power() + random.gauss(0, 8) + coach_boost_a
        b_score = b.power() + random.gauss(0, 8) + coach_boost_b
        winner = a if a_score >= b_score else b
        loser = b if winner is a else a
        winner.wins += 1
        loser.losses += 1

        for player in winner.roster[:5]:
            pts = random.randint(10, 34)
            reb = random.randint(2, 14)
            ast = random.randint(1, 11)
            player.career_points += pts
            player.career_rebounds += reb
            player.career_assists += ast

        return winner

    def simulate_season(self, user_team: Team, coach_mode: bool = False) -> Team:
        for t in self.teams.values():
            t.reset_record()

        all_teams = list(self.teams.values())
        for _round in range(20):
            random.shuffle(all_teams)
            for i in range(0, len(all_teams), 2):
                if i + 1 >= len(all_teams):
                    continue
                t1, t2 = all_teams[i], all_teams[i + 1]
                boost1, boost2 = 0.0, 0.0
                if coach_mode and (t1 is user_team or t2 is user_team):
                    print("\nCoach decision: choose gameplan for this matchup")
                    print("1) Pace & Space (+offense, risky)")
                    print("2) Defensive Grind (+defense, stable)")
                    print("3) Balanced")
                    choice = input("Choice: ").strip()
                    if choice == "1":
                        if t1 is user_team:
                            boost1 += random.choice([5, -2])
                        else:
                            boost2 += random.choice([5, -2])
                    elif choice == "2":
                        if t1 is user_team:
                            boost1 += 2
                        else:
                            boost2 += 2
                self.simulate_game(t1, t2, coach_boost_a=boost1, coach_boost_b=boost2)

        top4 = self.standings()[:4]
        semifinal_winners = [self.simulate_game(top4[0], top4[3]), self.simulate_game(top4[1], top4[2])]
        champ = self.simulate_game(semifinal_winners[0], semifinal_winners[1])
        return champ


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def team_menu(team: Team) -> None:
    print_header(f"{team.name} | Coach: {team.coach.name}")
    print(f"Coach Face Token: {team.coach.encrypted_face()}")
    print(f"Coach Avatar Token: {team.coach.encrypted_avatar()}")
    for idx, p in enumerate(sorted(team.roster, key=lambda x: x.rating, reverse=True), start=1):
        print(
            f"{idx:>2}. {p.name:24} {p.position} OVR {p.overall()} AGE {p.age} "
            f"Face:{p.encrypted_face()} Avatar:{p.encrypted_avatar()}"
        )


def select_team(league: League) -> Team:
    print_header("Choose Your Franchise")
    for i, name in enumerate(TEAMS, start=1):
        print(f"{i}) {name} (Coach: {COACHES[name]})")
    while True:
        pick = input("Team #: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(TEAMS):
            return league.teams[TEAMS[int(pick) - 1]]
        print("Invalid choice.")


def gm_actions(league: League, team: Team) -> None:
    while True:
        print_header("GM Hub")
        print("1) View roster")
        print("2) Sign free agent")
        print("3) Train a player")
        print("4) Start next season")
        print("5) Quit game")
        c = input("Choose: ").strip()

        if c == "1":
            team_menu(team)
            input("Press Enter...")
        elif c == "2":
            if not league.free_agents:
                print("No free agents available.")
                continue
            print_header("Free Agents")
            top_agents = sorted(league.free_agents, key=lambda p: p.rating, reverse=True)[:10]
            for i, p in enumerate(top_agents, start=1):
                print(f"{i}) {p.name} {p.position} OVR {p.rating} POT {p.potential} AGE {p.age}")
            pick = input("Sign player # (or enter to cancel): ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(top_agents):
                p = top_agents[int(pick) - 1]
                team.roster.append(p)
                league.free_agents.remove(p)
                print(f"Signed {p.name}!")
            input("Press Enter...")
        elif c == "3":
            team_menu(team)
            pick = input("Train which player #? ").strip()
            sorted_roster = sorted(team.roster, key=lambda x: x.rating, reverse=True)
            if pick.isdigit() and 1 <= int(pick) <= len(sorted_roster):
                p = sorted_roster[int(pick) - 1]
                gain = random.randint(1, 3)
                p.rating = min(p.potential, p.rating + gain)
                print(f"{p.name} improved +{gain} OVR.")
            input("Press Enter...")
        elif c == "4":
            return
        elif c == "5":
            raise SystemExit


def player_career_mode(league: League, team: Team) -> None:
    print_header("Create Your MyPlayer")
    name = input("Player name: ").strip() or "Rookie Star"
    pos = input("Position (PG/SG/SF/PF/C): ").strip().upper()
    if pos not in POSITIONS:
        pos = "SG"
    my_player = Player(name=name, age=19, rating=76, position=pos, potential=95)
    team.roster.append(my_player)
    print(f"You joined {team.name}!")

    for season in range(1, 6):
        print_header(f"Career Season {season}")
        print("Choose offseason focus:")
        print("1) Scoring")
        print("2) Playmaking")
        print("3) Strength")
        choice = input("Focus: ").strip()
        gain = random.randint(1, 4)
        my_player.rating = min(my_player.potential, my_player.rating + gain)
        champ = league.simulate_season(team)
        print(f"Season champion: {champ.name}")
        print(
            f"{my_player.name} CAREER: {my_player.career_points} PTS, "
            f"{my_player.career_rebounds} REB, {my_player.career_assists} AST | OVR {my_player.rating}"
        )
        league.age_and_progress()
        league.add_rookie_class()
        if choice == "1":
            my_player.career_points += random.randint(120, 260)
        elif choice == "2":
            my_player.career_assists += random.randint(80, 170)
        else:
            my_player.career_rebounds += random.randint(90, 180)


def coach_mode(league: League, team: Team) -> None:
    print_header("Coach Legacy Mode")
    print(f"You are now controlling: Coach {team.coach.name}")
    for season in range(1, 6):
        print_header(f"Coach Season {season}")
        champ = league.simulate_season(team, coach_mode=True)
        print(f"Season champion: {champ.name}")
        if champ is team:
            print("Your coaching decisions delivered a championship run!")
        league.age_and_progress()
        league.add_rookie_class()


def print_standings(league: League) -> None:
    print_header(f"Final Standings ({league.year})")
    for rank, t in enumerate(league.standings(), start=1):
        print(f"{rank:>2}. {t.name:26} {t.wins:>2}-{t.losses:<2} | Team OVR {t.power():.1f}")


def gm_mode(league: League, team: Team) -> None:
    for _ in range(1, 8):
        gm_actions(league, team)
        champion = league.simulate_season(team)
        print_header("Season Complete")
        print(f"Champion: {champion.name}")
        print_standings(league)
        league.age_and_progress()
        league.add_rookie_class()
        league.year += 1
        input("Press Enter for offseason...")


def main() -> None:
    print_header("COURTSIDE DYNASTY: MYGM / MYCAREER / MYCOACH")
    print("Welcome! Build a dynasty with real teams, stars, and coaches.")
    league = League()
    user_team = select_team(league)

    print_header("Choose Mode")
    print("1) GM Mode")
    print("2) Player Career Mode")
    print("3) Coach Mode")
    mode = input("Mode #: ").strip()

    if mode == "1":
        gm_mode(league, user_team)
    elif mode == "2":
        player_career_mode(league, user_team)
    elif mode == "3":
        coach_mode(league, user_team)
    else:
        print("Invalid mode selected, entering GM mode by default.")
        gm_mode(league, user_team)

    print_header("Thanks for playing Courtside Dynasty!")


if __name__ == "__main__":
    main()
