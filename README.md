# CareBot Route Planner

Sistema de planejamento de rotas para um **robô cuidador de idosos**, desenvolvido como projeto final da disciplina **Inteligência Artificial** do **IESB**.

## Contexto

O sistema calcula a melhor rota para o robô sair de um ponto **A**, onde ele está, e chegar a um ponto **B**, para onde precisa ir.

O ambiente se divide em dois contextos. A divisão é apenas conceitual: no grafo final, todos os nós são residências e pontos de endereço.

- **Micro:** grafo cujos nós são as residências dos idosos atendidos dentro de uma cidade.
- **Macro:** grafo cujos nós são as diferentes cidades.

### Regras do domínio

- Quando uma rota é gerada, o robô pode estar atendendo um idoso ou estar em uma das sedes.
- O robô só carrega a bateria em uma das sedes ou dentro de um veículo da empresa.
- **Entre cidades**, o robô precisa usar um veículo da empresa ou ser levado pela empresa.
- **Entre residências da mesma cidade**, o robô pode pedir um carro da empresa **ou** fazer o trajeto por conta própria.
- Cada atendimento dura um tempo médio (ainda a definir), e esse tempo afeta o consumo de bateria.

### Possível extensão

Calcular qual rota atribuir a um robô para que ele atenda **o maior número possível de idosos** em uma mesma rota, partindo com 100% de bateria e com no máximo 8 horas de trabalho.

---

## Modelagem

### Nós

| Tipo | Descrição |
| --- | --- |
| `residence` | Residência de um idoso a ser visitado |
| `headquarters` | Sede onde os robôs ficam em standby e recarregam |
| `collect_point` | Ponto de coleta dos carros da empresa |
| `reference_point` | Ponto de referência com endereço fixo (ex.: encontro de 4 ruas) |

A ideia é criar **40 nós do tipo residência** em cada uma de 4 cidades satélites de Brasília:

- Guará 1
- Guará 2
- Setor Habitacional Vicente Pires
- Setor Habitacional Arniqueiras

### Custos entre nós

Qualquer obstáculo ou gasto que aumente o custo de uma aresta entre dois nós:

- Distância percorrida
- Tempo
- Consumo de bateria
- Segurança da rota
- Custo financeiro
- Presença de semáforo
- Presença de buracos
- Engarrafamento
- Lombadas

---

## PEAS

### P: Medidas de desempenho

- Finalizar a rota
- Nunca ficar sem bateria
- Zero colisões graves com obstáculos
- **Maximizar:** porcentagem das atividades de cuidado concluídas com sucesso
- **Minimizar:**
  - consumo de bateria
  - choques com obstáculos
  - uso do transporte veicular da empresa

### E: Ambiente

**Macro (entre cidades, grafo de cidades)**
- Malha rodoviária e tráfego interurbano
- Sistema de frotas da empresa (disponibilidade, horários e pontos de embarque/desembarque)
- Condições meteorológicas adversas na estrada

**Micro (urbano e doméstico, grafo de residências)**
- *Vias e calçadas:* ruas residenciais e comerciais, semáforos, faixas de pedestres, desníveis, degraus e escadas
- *Agentes dinâmicos:* pedestres (idosos, crianças), animais domésticos, bicicletas, carros, motos e skates
- *Interiores (residência):* móveis e tapetes, portas, corredores estreitos e a presença do idoso

### A: Atuadores

- Movimentação (frente, trás, esquerda, direita)
- Controle de velocidade
- Interface de interação humano-robô
- Transposição de desníveis e escadas
- Requisições ao sistema de rotas
- Requisição de transporte veicular

### S: Sensores

- Câmeras
- Giroscópio
- Conexão com o sistema de rotas
- Sensor de proximidade de obstáculos
- Disponibilidade de transporte veicular
- Sensor de bateria
- GPS
- Dados do idoso atendido
- Detecção de presença humana

---

## Estrutura do repositório

```
.
├── csv/
│   └── vicente_pires/
│       ├── elements.csv               # nós da cidade
│       ├── connections.csv            # arestas entre nós da cidade
│       └── intercity_connections.csv  # arestas para nós de outras cidades
├── models/
│   └── graph.py                       # classes Element, Connection e Graph
├── generate_graph.py                  # gera graph.json a partir dos CSVs
├── graph.json                         # tabelas hash do grafo (gerado, não editar à mão)
├── main.py                            # loop de interação com o usuário
├── route_planner.py                   # cálculo de rotas (A*)
├── LICENSE
└── README.md
```

---

## Como executar

```bash
python3 generate_graph.py   # sempre que algum CSV mudar
python3 main.py
```

`generate_graph.py` lê os CSVs de todas as cidades e salva em `graph.json` duas tabelas hash:

- `nodes`: label do nó → dados do nó (cidade, endereço, tipo, residente, coordenadas)
- `connections`: label do nó → lista das conexões que saem dele, com todos os custos

O script também valida os dados e para com erro se encontrar label repetido, conexão para nó inexistente ou coluna vazia. **Depois de alterar qualquer CSV, rode o script de novo e faça commit do `graph.json` junto.**

---

## Padrão dos dados

Siga este padrão ao cadastrar uma nova cidade.

### Regras gerais

- Cada cidade tem uma pasta própria em `csv/`, com nome em `snake_case` e sem acentos (ex.: `guara_1`, `arniqueiras`).
- Toda pasta de cidade contém **exatamente** os três arquivos: `elements.csv`, `connections.csv` e `intercity_connections.csv`. Se não houver conexões com outras cidades, `intercity_connections.csv` fica só com o cabeçalho.
- Arquivos em UTF-8, separados por vírgula. Textos que contêm vírgula ficam entre aspas (ex.: `"Rua 3, Chácara 12, Vicente Pires"`).
- Os **labels dos nós são únicos em todo o projeto**, não só na cidade. Vicente Pires usa `n01` a `n40`, então a próxima cidade começa em `n41`, e assim por diante.

### `elements.csv`: nós

```csv
Label,Address,Type,Resident,Latitude,Longitude
n01,"Rua 3, Chácara 12, Vicente Pires",headquarters,,-15.803512,-48.028945
n02,"Rua 3, Chácara 45, Vicente Pires",residence,Dona Maria Silva,-15.80482,-48.02611
```

| Coluna | Descrição |
| --- | --- |
| `Label` | Identificador único do nó (ex.: `n01`) |
| `Address` | Endereço |
| `Type` | `residence`, `headquarters`, `collect_point` ou `reference_point` |
| `Resident` | Nome do idoso. Preenchido apenas em `residence`; vazio nos demais tipos |
| `Latitude`, `Longitude` | Coordenadas reais do ponto, em graus decimais |

### `connections.csv` e `intercity_connections.csv`: arestas

Os dois arquivos têm as mesmas colunas. Em `connections.csv`, os dois nós são da mesma cidade. Em `intercity_connections.csv`, `From` é um nó desta cidade e `To` é um nó de outra cidade.

```csv
From,To,Type,robot_walkable,distance,time,battery_consumption,security,financial_cost,traffic_light,road_holes,traffic_jam,speed_bumps
n01,n02,route,true,440,0.9,2.2,8,0,0,1,2,2
n02,n01,route,true,440,0.9,2.2,8,0,0,1,2,2
n20,n23,route,false,2760,2.8,0,5,10.52,2,2,6,4
n23,n20,route,false,2760,2.8,0,5,10.52,2,2,6,4
```

Cada linha é uma conexão **de mão única**, de `From` para `To`. Se o trecho puder ser feito nos dois sentidos, cadastre também a linha inversa (`B,A`); os valores podem ser diferentes em cada sentido. Nenhuma coluna pode ficar vazia.

| Coluna | Unidade | Como preencher |
| --- | --- | --- |
| `From`, `To` | label | Nós de origem e destino |
| `Type` | — | `route` |
| `robot_walkable` | `true`/`false` | `true` se o robô pode fazer o trecho sozinho; `false` se precisa de um carro da empresa |
| `distance` | metros | Distância em linha reta entre as coordenadas |
| `time` | minutos | calculado com base na distância e velocidade (velocidade muda com base no modo de deslocamento) |
| `battery_consumption` | % da bateria | Quantidade de bateria consumida para cada km |
| `security` | 0 a 10 | Segurança do trecho; quanto maior, mais seguro |
| `financial_cost` | R$ | Custo financeiro agregado da rota |
| `traffic_light` | quantidade | Número de semáforos no trecho |
| `road_holes` | 0 a 10 | Intensidade de buracos; 0 = nenhum |
| `traffic_jam` | 0 a 10 | Intensidade de engarrafamento; 0 = nenhum |
| `speed_bumps` | quantidade | Número de lombadas no trecho |

#### Custos por modo de deslocamento

| | Robô a pé (`robot_walkable = true`) | Carro da empresa (`robot_walkable = false`) |
| --- | --- | --- |
| Velocidade | 30 km/h | 60 km/h |
| `time` | `distance (km) ÷ 30 × 60` (= `distance (km) × 2`) | `distance (km) ÷ 60 × 60` (= `distance (km) × 1`) |
| `battery_consumption` | `distance (km) × 5` (5% por km) | `0` (o robô não gasta bateria no carro) |
| `financial_cost` | `0` | `5 + distance (km) × 2` (R$ 5 de bandeirada + R$ 2 por km) |

Exemplo: um trecho de 1240 m a pé fica com `time = 2.5`, `battery_consumption = 6.2` e `financial_cost = 0`. O mesmo trecho de carro fica com `time = 1.2`, `battery_consumption = 0` e `financial_cost = 7.48`.

---

## Status

🚧 Em desenvolvimento. Os dados de **Vicente Pires** já estão disponíveis. As demais cidades e o algoritmo de roteamento (`route_planner.py`) ainda serão implementados.

## Licença

Distribuído sob a licença contida em [LICENSE](LICENSE).
