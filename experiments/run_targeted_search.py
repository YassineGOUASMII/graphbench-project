import sys
import os

sys.path.append(os.path.abspath("src"))

import pandas as pd
import networkx as nx

from conjecture import Conjecture
from search_baseline import search_counterexample


def main():
    df = pd.read_excel("benchmark/benchmark.xlsx")

    target_ids = [1880, 2120]

    time_limit = 5
    restarts = 3

    os.makedirs("results/targeted_search", exist_ok=True)
    os.makedirs("results/targeted_search/best_graphs", exist_ok=True)

    global_results = []

    for target_id in target_ids:
        row = df[df["Conjecture ID"] == target_id].iloc[0]
        conjecture = Conjecture(row)

        print()
        print("=" * 60)
        print("Conjecture ciblée", conjecture.id)
        print(conjecture.text)
        print("=" * 60)

        best_result = None

        for restart in range(restarts):
            print()
            print(f"--- Restart {restart + 1}/{restarts} ---")

            result = search_counterexample(
                conjecture,
                time_limit=time_limit
            )

            if best_result is None or result["score"] > best_result["score"]:
                best_result = result

            if result["found"]:
                break

        result = best_result

        graph6 = nx.to_graph6_bytes(
            result["graph"],
            header=False
        ).decode().strip()

        result_file = f"results/targeted_search/best_graphs/conjecture_{conjecture.id}.txt"

        with open(result_file, "w", encoding="utf-8") as f:
            f.write(f"Conjecture ID : {conjecture.id}\n")
            f.write(f"Conjecture : {conjecture.text}\n")
            f.write(f"Trouvé : {result['found']}\n")
            f.write(f"Score : {result['score']}\n")
            f.write(f"Temps : {result['time']}\n")
            f.write(f"Graph6 : {graph6}\n")
            f.write("\nInvariants :\n")

            for k, v in result["invariants"].items():
                f.write(f"{k} = {v}\n")

        cost = result["time"] if result["found"] else 120

        global_results.append({
            "id": conjecture.id,
            "found": result["found"],
            "violation_score": result["score"],
            "time": result["time"],
            "cost": cost,
            "graph6": graph6
        })

        print()
        print("===== MEILLEUR RÉSULTAT CIBLÉ =====")
        print("Trouvé :", result["found"])
        print("Score :", result["score"])
        print("Temps :", round(result["time"], 2), "sec")
        print("Coût :", round(cost, 2))
        print("Graph6 :", graph6)

    results_df = pd.DataFrame(global_results)
    results_df.to_csv("results/targeted_search/scores.csv", index=False)

    print()
    print("===== FIN RECHERCHE CIBLÉE =====")
    print(results_df)


if __name__ == "__main__":
    main()