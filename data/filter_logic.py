import pandas as pd


def apply_filters(df, filters):
    df = df.copy()
    print("\nFilters passed in:", filters)

    for metric, threshold in filters.items():
        if metric in df.columns:
            print(f"\nFiltering on: {metric}")
            print(df[[metric]].head())
            print("Types in column:", df[metric].map(type).value_counts())

            # Convert to numeric
            df[metric] = pd.to_numeric(df[metric], errors='coerce')
            df = df[df[metric].notna()]

            # Apply threshold
            if "PE Ratio" in metric or "Debt/Equity" in metric:
                df = df[df[metric] < threshold]
            else:
                df = df[df[metric] > threshold]

    return df.reset_index(drop=True)


