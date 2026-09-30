from generate_graph import load_graph
from route_planner import find_best_route

EXIT_COMMAND = "sair"


def main() -> None:
    graph = load_graph()
    print("CareBot Route Planner (digite 'sair' para encerrar)")

    while True:
        start = input("\nOnde você está? ").strip()
        if start.lower() == EXIT_COMMAND:
            break
        if start not in graph.nodes:
            print(f"Ponto {start!r} não existe.")
            continue

        goal = input("Para onde quer ir? ").strip()
        if goal.lower() == EXIT_COMMAND:
            break
        if goal not in graph.nodes:
            print(f"Ponto {goal!r} não existe.")
            continue

        route = find_best_route(graph, start, goal)
        if route:
            print("Melhor rota: " + " -> ".join(route))
        else:
            print(f"Nenhuma rota encontrada de {start} até {goal}.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
