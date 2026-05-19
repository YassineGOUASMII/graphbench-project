import os
import pandas as pd


def main():
    results_file = "results/basic_search/scores.csv"

    df = pd.read_csv(results_file)

    os.makedirs("results/final", exist_ok=True)

    final_csv = "results/final/final_results.csv"
    final_summary = "results/final/final_summary.txt"

    df.to_csv(final_csv, index=False)

    found_count = df["found"].sum()
    total_count = len(df)

    total_cost = df["cost"].sum()
    average_time = df["time"].mean()

    with open(final_summary, "w", encoding="utf-8") as f:
        f.write("===== FINAL RESULTS =====\n")
        f.write(f"Conjectures tested : {total_count}\n")
        f.write(f"Counterexamples found : {found_count}\n")
        f.write(f"Success rate : {found_count / total_count * 100:.2f}%\n")
        f.write(f"Approximate total cost : {total_cost:.2f}\n")
        f.write(f"Average time : {average_time:.2f} seconds\n")

    print()
    print("===== FINAL RESULTS =====")
    print("Conjectures tested :", total_count)
    print("Counterexamples found :", found_count)
    print("Success rate :", round(found_count / total_count * 100, 2), "%")
    print("Approximate total cost :", round(total_cost, 2))
    print("Average time :", round(average_time, 2), "sec")

    print()
    print("Saved:")
    print(final_csv)
    print(final_summary)


if __name__ == "__main__":
    main()