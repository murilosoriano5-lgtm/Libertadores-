# Libertaforss

Simulador da fase de liga da Libertadores no **formato suíço**: 36 times, 4 potes, 8 jogos por time.

## Regras implementadas
- 36 times em 4 potes de 9 (ver `libertaforss/teams.py`).
- Cada time joga **2 vezes contra cada pote** (1 em casa + 1 fora, adversários diferentes) = **8 jogos** (4 casa, 4 fora).
- Total: 144 jogos.
- Nunca enfrenta time do mesmo país.
- Atual campeão (Flamengo) e campeão da Sul-Americana (Lanús) entram no Pote 1.
- Classificação: pontos > saldo de gols > gols marcados > nome.
- **Mata-mata:** os 16 primeiros avançam. Oitavas, quartas e semifinais em ida e volta (o melhor colocado na tabela decide em casa); final em jogo único. Decisão por pênaltis após empate no agregado.
- Chave das oitavas (posição na tabela): 1x16, 8x9, 3x14, 5x12 (lado A) e 2x15, 7x10, 4x13, 6x11 (lado B). Os lados só se encontram na final.

## Uso
```bash
python3 -m libertaforss draw --seed 1       # jogos de cada time (use --edition 2026 para a anterior)
python3 -m libertaforss rounds --seed 1     # jogos divididos em 8 rodadas
python3 -m libertaforss simulate --seed 1   # resultados e tabela
python3 -m libertaforss h2h Palmeiras Toluca  # histórico de confrontos
python3 -m libertaforss ranking             # ranking histórico (todas as edições)
python3 -m unittest discover -s tests       # testes
```
Sem dependências externas (Python 3.10+). O mesmo `--seed` gera o mesmo sorteio.

## Edições
Os times de cada edição ficam em `libertaforss/teams.py` (`EDITIONS`). Os comandos usam a mais recente (2027) ou `--edition 2026`.
- **2027**: Palmeiras (campeão) e Chivas (campeão da Sul-Americana) no Pote 1. Sorteio e rodadas (seed 2027) em `docs/SORTEIO_2027_SEED_2027.txt` e `docs/RODADAS_2027_SEED_2027.txt`.
- **2026**: usada nos arquivos `docs/*_SEED_2026.txt` e em `data/`.

## Estrutura
| Arquivo | Função |
|---|---|
| `libertaforss/teams.py` | Times, países e potes |
| `libertaforss/draw.py` | Sorteio com restrições (backtracking) |
| `libertaforss/schedule.py` | Divisão em 8 rodadas de 18 jogos |
| `libertaforss/knockout.py` | Chaveamento do mata-mata |
| `libertaforss/history.py` | Histórico de confrontos (head-to-head) |
| `tools/gerar_historico.py` | Gera `data/historico.csv` a partir dos arquivos de cada edição |
| `libertaforss/simulate.py` | Gols (Poisson) e tabela |
| `tests/` | Testes do sorteio, das rodadas e do mata-mata |
| `data/` | Edição 2026 jogada: resultados da fase de liga e do mata-mata (Palmeiras campeão) |
| `docs/` | Documentação detalhada e material de estudo |

## Edição 2026 (exemplo jogado)
Campeão: **Palmeiras** 2x1 Toluca (final). A tabela da fase de liga foi conferida contra os 144 resultados em `data/edicao_2026_resultados.txt` (pontos, V/E/D, saldo e ordem batem; saldo do Caracas: -7).

## Histórico de confrontos
`data/historico.csv` guarda todos os jogos de todas as edições (colunas: edição, fase, rodada, mandante, gols, visitante, pênaltis, prorrogação, sede). Por enquanto só a edição 2026. `h2h A B` lista os jogos entre dois times e o resumo de vitórias, empates e gols.
- **PR = prorrogação** (coluna `prorrogacao`).
- **Finais têm sede única** (coluna `sede`); a primeira, 2026, foi em **Montevidéu**.
- Jogo decidido nos pênaltis conta como empate no resumo; os pênaltis ficam em colunas à parte.
- **Ranking histórico** (`ranking`): soma todas as edições do CSV. Critério: pontos (3/1/0) > saldo > gols pró > nome. Mostra também títulos e vices (calculados pelas finais; pênaltis desempatam).
- Nova edição: crie `data/edicao_AAAA_resultados.txt` e `data/edicao_AAAA_mata_mata.txt`, inclua a sede em `FINAL_VENUES` e rode `python3 tools/gerar_historico.py 2026 AAAA`.

## Pendente / a definir
- O mata-mata ainda não é simulado automaticamente (apenas o chaveamento está em código).
- Ratings reais dos times (hoje a força depende só do pote).
