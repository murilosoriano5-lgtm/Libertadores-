"""Dados dos 36 times, divididos em 4 potes de 9."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Team:
    name: str
    country: str
    pot: int


_POTS_2026 = {
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

_POTS_2027 = {
    1: [("Palmeiras", "BRA"), ("Chivas", "MEX"), ("Fluminense", "BRA"),
        ("Flamengo", "BRA"), ("Boca Juniors", "ARG"), ("River Plate", "ARG"),
        ("Estudiantes", "ARG"), ("Peñarol", "URU"), ("Atlético Mineiro", "BRA")],
    2: [("Cruzeiro", "BRA"), ("Athletico", "BRA"), ("Rosario Central", "ARG"),
        ("Colo-Colo", "CHI"), ("Cerro Porteño", "PAR"), ("Independiente del Valle", "ECU"),
        ("LDU", "ECU"), ("Atlético Nacional", "COL"), ("Toluca", "MEX")],
    3: [("Montevideo City Torque", "URU"), ("América de Cali", "COL"), ("Bolívar", "BOL"),
        ("Club América", "MEX"), ("Cruz Azul", "MEX"), ("Olimpia", "PAR"),
        ("Universidad Católica", "CHI"), ("Universitario", "PER"), ("Always Ready", "BOL")],
    4: [("Forge", "CAN"), ("Inter Miami", "USA"), ("Nashville", "USA"),
        ("Los Angeles FC", "USA"), ("Alajuelense", "CRC"), ("Belgrano", "ARG"),
        ("Caracas", "VEN"), ("Deportivo Táchira", "VEN"), ("Alianza Lima", "PER")],
}


def _build(pots):
    return [Team(n, c, p) for p, ts in pots.items() for n, c in ts]


EDITIONS = {"2026": _build(_POTS_2026), "2027": _build(_POTS_2027)}
LATEST = "2027"
TEAMS = EDITIONS[LATEST]
