import pandas as pd


def screen_companies(df):

    print("\n========== FINANCIAL SCREENER ==========\n")

    # Convert numeric columns
    df["roe_percentage"] = pd.to_numeric(
        df["roe_percentage"], errors="coerce"
    )

    df["roce_percentage"] = pd.to_numeric(
        df["roce_percentage"], errors="coerce"
    )

    df["composite_score"] = (
        df["roe_percentage"] + df["roce_percentage"]
    ) / 2

    while True:

        print("1. High ROE (>15%)")
        print("2. High ROCE (>20%)")
        print("3. Top Composite Score")
        print("4. Show All Companies")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            result = df[df["roe_percentage"] > 15]

            print(
                result[
                    [
                        "id",
                        "company_name",
                        "roe_percentage"
                    ]
                ]
            )

        elif choice == "2":

            result = df[df["roce_percentage"] > 20]

            print(
                result[
                    [
                        "id",
                        "company_name",
                        "roce_percentage"
                    ]
                ]
            )

        elif choice == "3":

            print(
                df[
                    [
                        "id",
                        "company_name",
                        "roe_percentage",
                        "roce_percentage"
                    ]
                ]
            )

        elif choice == "4":
            print(df[
        [
            "id",
            "company_name",
            "roe_percentage",
            "roce_percentage"
        ]
    ])

        elif choice == "5":
            print("Exiting Screener...")
            break

        else:
            print("Invalid Choice!")