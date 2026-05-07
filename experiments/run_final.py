import os
import pandas as pd


def main():
    baseline_file = "results/baseline_search/scores.csv"
    targeted_file = "results/targeted_search/scores.csv"

    baseline_df = pd.read_csv(baseline_file)
    targeted_df = pd.read_csv(targeted_file)

    final_results = []

    targeted_ids = set(targeted_df["id"])

    for _, row in baseline_df.iterrows():
        conjecture_id = row["id"]

        if conjecture_id in targeted_ids:
            targeted_row = targeted_df[
                targeted_df["id"] == conjecture_id
            ].iloc[0]

            if targeted_row["found"]:
                final_results.append(targeted_row.to_dict())
            else:
                final_results.append(row.to_dict())

        else:
            final_results.append(row.to_dict())

    final_df = pd.DataFrame(final_results)

    os.makedirs("results/final", exist_ok=True)

    final_csv = "results/final/final_results.csv"
    final_summary = "results/final/final_summary.txt"

    final_df.to_csv(final_csv, index=False)

    found_count = final_df["found"].sum()
    total_count = len(final_df)

    total_cost = final_df["cost"].sum()
    average_time = final_df["time"].mean()

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