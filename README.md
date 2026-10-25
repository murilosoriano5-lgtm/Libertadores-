# Libertaforss

Simulador da fase de liga da Libertadores no **formato suíço**: 36 times, 4 potes, 8 jogos por time.

## Regras implementadas
- 36 times em 4 potes de 9 (ver `libertaforss/teams.py`).
- Cada time joga **2 vezes contra cada pote** (1 em casa + 1 fora, adversários diferentes) = **8 jogos** (4 casa, 4 fora).
- Total: 144 jogos.
- Nunca enfrenta time do mesmo país.
- Atual campeão (Flamengo) e campeão da Sul-Americana (Lanús) entram no Pote 1.
- Classificação: pontos > saldo de gols > gols marcados > nome.

## Uso
```bash
python3 -m libertaforss draw --seed 1       # jogos de cada time
python3 -m libertaforss simulate --seed 1   # resultados e tabela
python3 -m unittest discover -s tests       # testes
```
Sem dependências externas (Python 3.10+). O mesmo `--seed` gera o mesmo sorteio.

## Estrutura
| Arquivo | Função |
|---|---|
| `libertaforss/teams.py` | Times, países e potes |
| `libertaforss/draw.py` | Sorteio com restrições (backtracking) |
| `libertaforss/simulate.py` | Gols (Poisson) e tabela |
| `tests/test_draw.py` | Valida as regras do sorteio |
| `docs/` | Documentação detalhada e material de estudo |

## Pendente / a definir
- Quantos avançam e como é o mata-mata (ex.: top 8 direto às oitavas, 9º–24º em playoff, como na Champions?).
- Ratings reais dos times (hoje a força depende só do pote).
