import pandas as pd

def extract_features(input_file, output_file, columns_to_extract):
    # Read the combined metadata file
    df = pd.read_csv(input_file, dtype=str)

    # Check if all specified columns are present
    missing_columns = [col for col in columns_to_extract if col not in df.columns]
    if missing_columns:
        print(f"The following columns are missing in the input file: {missing_columns}")
        return

    # Extract the specified columns
    df_extracted = df[columns_to_extract].copy()

    # Save the extracted data to a new CSV file
    df_extracted.to_csv(output_file, index=False)
    print(f"Extracted features saved to {output_file}")

# Example usage
if __name__ == '__main__':
    input_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Metadata/combined_metadata.csv'
    output_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Sequences/extracted_features.csv'
    columns = ['Entry', 'Sequence', 'Selected_PDB', 'ProteinClass']
    extract_features(input_csv, output_csv, columns)
