"""Dados dos 36 times, divididos em 4 potes de 9."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Team:
    name: str
    country: str
    pot: int


_POTS = {
    1: [("Flamengo", "BRA"), ("Lanús", "ARG"), ("Palmeiras", "BRA"),
        ("Boca Juniors", "ARG"), ("Estudiantes", "ARG"), ("Peñarol", "URU"),
        ("LDU", "ECU"), ("Independiente del Valle", "ECU"), ("Fluminense", "BRA")],
    2: [("Rosario Central", "ARG"), ("Universidad Católica", "CHI"),
        ("Cerro Porteño", "PAR"), ("Libertad", "PAR"), ("Bolívar", "BOL"),
        ("Corinthians", "BRA"), ("Cruzeiro", "BRA"), ("Universitario", "PER"),
        ("Nacional", "URU")],
    3: [("Mirassol", "BRA"), ("Platense", "ARG"), ("Independiente Rivadavia", "ARG"),
        ("Always Ready", "BOL"), ("Independiente Medellín", "COL"),
        ("Caracas", "VEN"), ("Sporting Cristal", "PER"), ("Coquimbo Unido", "CHI"),
        ("Santa Fe", "COL")],
    4: [("Alajuelense", "CRC"), ("Real España", "HON"), ("Inter Miami", "USA"),
        ("Vancouver Whitecaps", "CAN"), ("Nashville", "USA"), ("Toluca", "MEX"),
        ("Club América", "MEX"), ("Cruz Azul", "MEX"), ("Universidad Central", "VEN")],
}

TEAMS = [Team(n, c, p) for p, ts in _POTS.items() for n, c in ts]
