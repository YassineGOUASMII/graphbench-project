import sys
import os

sys.path.append(os.path.abspath("src"))

import pandas as pd
import networkx as nx

from conjecture import Conjecture
from search import search_counterexample


def main():
    df = pd.read_excel("benchmark/benchmark.xlsx")

    number_of_conjectures = 100
    time_limit = 40

    # Nombre de redémarrages
    restarts = 4

    os.makedirs("results/basic_search", exist_ok=True)
    os.makedirs("results/basic_search/best_graphs", exist_ok=True)

    global_results = []

    for i in range(number_of_conjectures):
        row = df.iloc[i]
        conjecture = Conjecture(row)

        print()
        print("=" * 60)
        print("Conjecture", conjecture.id)
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

            if (
                best_result is None
                or result["score"] > best_result["score"]
            ):
                best_result = result

            if result["found"]:
                break

        result = best_result

        graph6 = nx.to_graph6_bytes(
            result["graph"],
            header=False
        ).decode().strip()

        result_file = f"results/basic_search/best_graphs/conjecture_{conjecture.id}.txt"

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
        print("===== MEILLEUR RÉSULTAT =====")
        print("Trouvé :", result["found"])
        print("Score :", result["score"])
        print("Temps :", round(result["time"], 2), "sec")
        print("Coût :", round(cost, 2))

    results_df = pd.DataFrame(global_results)

    results_df.to_csv(
        "results/basic_search/scores.csv",
        index=False
    )

    found_count = results_df["found"].sum()
    total_count = len(results_df)
    total_cost = results_df["cost"].sum()
    average_time = results_df["time"].mean()

    summary_file = "results/basic_search/summary.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("===== RÉSUMÉ EXPÉRIMENTAL =====\n")
        f.write(f"Nombre de conjectures testées : {total_count}\n")
        f.write(f"Nombre de contre-exemples trouvés : {found_count}\n")
        f.write(f"Taux de réussite : {found_count / total_count * 100:.2f}%\n")
        f.write(f"Score total officiel approximatif : {total_cost:.2f}\n")
        f.write(f"Temps moyen : {average_time:.2f} secondes\n")

    print()
    print("===== RÉSUMÉ FINAL =====")
    print("Conjectures testées :", total_count)
    print("Contre-exemples trouvés :", found_count, "/", total_count)
    print("Taux de réussite :", round(found_count / total_count * 100, 2), "%")
    print("Score total approximatif :", round(total_cost, 2))
    print("Temps moyen :", round(average_time, 2), "sec")

    print()
    print("Résultats sauvegardés dans results/basic_search/")
    print("Résumé sauvegardé dans results/basic_search/summary.txt")


if __name__ == "__main__":
    main()