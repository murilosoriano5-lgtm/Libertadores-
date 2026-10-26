# Documentação técnica

## 1. Modelo do problema
Cada pote tem 9 times. Para cada time, queremos 1 jogo em casa e 1 fora contra **cada** pote (inclusive o próprio).

- **Pote contra ele mesmo**: uma permutação `π` onde `x` recebe `π(x)`. Cada time recebe 1 e visita 1. Proibimos `π(x)=x`, mesmo país e pares de 2 ciclos (A×B em casa e B×A em casa seria repetir o confronto).
- **Pote i contra pote j**: duas permutações — `host` (time de i joga em casa) e `visit` (time de i joga fora) — com adversários diferentes entre si. Do ponto de vista do pote j, as mesmas permutações dão 1 jogo em casa e 1 fora.

## 2. Algoritmo
`_find_permutation` faz backtracking com ordem aleatória (`random.Random(seed)`), respeitando uma função `forbidden`. Se algum passo não tem solução, o sorteio recomeça (até 1000 tentativas).

## 3. Simulação
Gols ~ Poisson, com média 1,45·e^d (mandante) e 1,15·e^-d (visitante), onde `d = (força_casa − força_fora + 60)/800`. A força vem do pote (1900/1750/1650/1550) e 60 é a vantagem de casa.

## 4. Decisões e premissas
- Listas de vagas usadas como informadas; Flamengo e Lanús ficam nos potes como você definiu.
- Vancouver Whitecaps entra com país `CAN` (Canadá) e Inter Miami/Nashville como `USA`; restrição de país só impede mesmo código.
- Nomes ajustados: Peñarol, Platense, Independiente Rivadavia, Coquimbo Unido, Universitario.

## 5. Divisão em rodadas (`schedule.py`)
- Cada jogo é uma "aresta" entre dois times; uma rodada é um conjunto de jogos em que nenhum time repete (coloração de arestas com 8 cores). Usamos backtracking que escolhe sempre o jogo com menos rodadas possíveis, com limite de passos e reinício.
- Como as 8 rodadas podem ser embaralhadas, uma busca local escolhe a ordem com menos sequências de 3+ jogos seguidos em casa ou fora.
- Rodar 20 divisões diferentes e ficar com a melhor leva poucos segundos. Não é garantido zerar as sequências longas.

## 6. Mata-mata (`knockout.py`)
- Entram os 16 primeiros. As 8 séries das oitavas seguem `ROUND_OF_16` (1x16, 8x9, 3x14, 5x12 | 2x15, 7x10, 4x13, 6x11).
- Em cada série, o pior colocado na tabela joga a ida em casa e o melhor joga a volta em casa.
- `next_round` cruza os vencedores em pares na ordem da chave (vencedor de 1x16 contra vencedor de 8x9 etc.), então os lados A e B só se encontram na final.
- Pênaltis aparecem nos dados como `1(3)x0(5)` (placar da volta e, entre parênteses, os pênaltis de cada time).
- O teste `tests/test_knockout.py` reproduz o chaveamento da edição 2026 a partir dos resultados.

## 7. Histórico de confrontos (`history.py`)
- Formato: um CSV com uma linha por jogo, assim o mesmo arquivo serve para consultas, planilhas e futuras estatísticas.
- `head_to_head(a, b, games)` filtra os jogos entre os dois times (em qualquer mando) e soma vitórias, empates e gols. Pênaltis não alteram o placar.
- `tools/gerar_historico.py` converte os arquivos de texto de cada edição, normalizando nomes (ex.: "Penarol" vira "Peñarol").
- A sede da final é um dado por edição (`FINAL_VENUES`). 2026: Montevidéu.
- `all_time_ranking(games)` acumula J/V/E/D/gols/pontos por time em todos os jogos do CSV (liga e mata-mata). Títulos e vices vêm da fase "Final". O critério de ordenação é uma escolha de projeto e pode mudar (ex.: títulos primeiro).

## 8. Edições (`teams.py`)
- Cada edição é um dicionário de potes -> lista (nome, país). Os nomes devem ser idênticos entre edições para o histórico somar corretamente (ex.: "Peñarol", "Universitario", "Rosario Central").
- 2027: Chivas conta como México (MEX) e Forge como Canadá (CAN). O campeão da Libertadores (Palmeiras) e o da Sul-Americana (Chivas) vão ao Pote 1 e ocupam a vaga do país. Brasil tem 6 times (5 vagas + campeão) e o México 4.
- Ao incluir uma edição, o teste `test_draw` valida sozinho: 36 times distintos, potes de 9, 144 jogos e regras do sorteio.
