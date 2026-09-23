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
│       ├── elements.csv      # nós do grafo
│       └── connections.csv   # arestas e seus custos
├── main.py
├── LICENSE
└── README.md
```

### `elements.csv`: nós

| Coluna | Descrição |
| --- | --- |
| `Label` | Identificador do nó (ex.: `n01`) |
| `Address` | Endereço |
| `Type` | `residence`, `headquarters`, `collect_point` ou `reference_point` |
| `Resident` | Nome do idoso (apenas para residências) |
| `Latitude`, `Longitude` | Coordenadas geográficas |

### `connections.csv`: arestas

| Coluna | Descrição |
| --- | --- |
| `From`, `To` | Nós de origem e destino |
| `Type` | Tipo da conexão (ex.: `route`) |
| `robot_walkable` | Se o robô pode percorrer o trecho por conta própria |
| `distance` | Distância percorrida |
| `time` | Tempo de percurso |
| `battery_consumption` | Consumo de bateria |
| `security` | Nível de segurança da rota |
| `financial_cost` | Custo financeiro |
| `traffic_light` | Presença de semáforos |
| `road_holes` | Presença de buracos |
| `traffic_jam` | Engarrafamento |
| `speed_bumps` | Lombadas |

---

## Status

🚧 Em desenvolvimento. Os dados de **Vicente Pires** já estão disponíveis. As demais cidades e o algoritmo de roteamento (`main.py`) ainda serão implementados.

## Licença

Distribuído sob a licença contida em [LICENSE](LICENSE).
