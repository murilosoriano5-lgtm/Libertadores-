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
