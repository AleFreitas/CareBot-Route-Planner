from route_planner import find_best_route

EXIT_COMMAND = "sair"


def main() -> None:
    print("CareBot Route Planner (digite 'sair' para encerrar)")

    while True:
        start = input("\nOnde você está? ").strip()
        if start.lower() == EXIT_COMMAND:
            break

        goal = input("Para onde quer ir? ").strip()
        if goal.lower() == EXIT_COMMAND:
            break

        route = find_best_route(start, goal)
        if route:
            print("Melhor rota: " + " -> ".join(route))
        else:
            print(f"Nenhuma rota encontrada de {start} até {goal}.")


if __name__ == "__main__":
    main()
