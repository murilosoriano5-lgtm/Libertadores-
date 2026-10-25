import argparse

from .draw import generate_fixtures
from .history import describe, head_to_head, load_history
from .schedule import split_rounds
from .simulate import simulate
from .teams import TEAMS


def main():
    ap = argparse.ArgumentParser(prog="libertaforss")
    ap.add_argument("command", choices=["draw", "rounds", "simulate", "h2h"])
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("teams", nargs="*", help="h2h: os dois times")
    args = ap.parse_args()
    if args.command == "h2h":
        a, b = args.teams
        played, wins, goals = head_to_head(a, b, load_history())
        for g in played:
            print(describe(g))
        print(f"{a}: {wins[a]}V | empates: {wins['empates']} | {b}: {wins[b]}V | gols {goals[a]}x{goals[b]}")
        return
    fixtures = generate_fixtures(TEAMS, args.seed)

    if args.command == "draw":
        for team in TEAMS:
            print(f"\n{team.name} (Pote {team.pot})")
            for m in fixtures:
                if m.home == team:
                    print(f"  Casa : vs {m.away.name} (Pote {m.away.pot})")
            for m in fixtures:
                if m.away == team:
                    print(f"  Fora : @ {m.home.name} (Pote {m.home.pot})")
    elif args.command == "rounds":
        for n, rd in enumerate(split_rounds(fixtures, args.seed), 1):
            print(f"\nRODADA {n}")
            for m in rd:
                print(f"  {m.home.name} x {m.away.name}")
    else:
        print(f"{'#':>2} {'Time':<26}{'J':>3}{'V':>3}{'E':>3}{'D':>3}{'GP':>4}{'GC':>4}{'SG':>4}{'Pts':>5}")
        for i, r in enumerate(simulate(fixtures, TEAMS, args.seed), 1):
            print(f"{i:>2} {r.team.name:<26}{r.played:>3}{r.wins:>3}{r.draws:>3}{r.losses:>3}"
                  f"{r.gf:>4}{r.ga:>4}{r.gd:>4}{r.points:>5}")


main()
