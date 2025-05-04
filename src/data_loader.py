import pandas as pd

def load_faf_data(filepath="cleaned_dataset.csv"): 
    """Loads the cleaned FAF data and calculates a congestion threshold."""
    print(f"Attempting to load cleaned FAF data from: {filepath}")
    try:
        df = pd.read_csv(filepath)
        print("FAF data loaded successfully.")

        if 'tot_trips' in df.columns:
            congestion_threshold = df['tot_trips'].quantile(0.80)
            print(f"Calculated congestion threshold (80th percentile of tot_trips): {congestion_threshold:.2f}")
            return df, congestion_threshold
        else:
            print("Warning: 'tot_trips' column not found in the loaded CSV.")
            print("Available columns:", df.columns.tolist())
            print("Cannot calculate threshold.")
            return df, None 

    except FileNotFoundError:
        print(f"Error: Cleaned data file not found at '{filepath}'")
        print("Ensure this path is correct relative to the 'smartsupplysim' directory where you run the command.")
        return None, None 
    except Exception as e:
         print(f"An error occurred loading the CSV: {e}")
         return None, None