import os
import pandas as pd

def combine_metadata_files(input_dir, output_file):
    # List to hold dataframes
    df_list = []

    # Loop through each file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.tsv') or file_name.endswith('.txt'):
            file_path = os.path.join(input_dir, file_name)
            protein_class = os.path.splitext(file_name)[0]

            # Read the TSV file into a dataframe
            try:
                df = pd.read_csv(file_path, sep='\t', dtype=str)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

            # Add 'ProteinClass' column
            df['ProteinClass'] = protein_class
            df_list.append(df)
        else:
            print(f"Skipping file {file_name}")

    # Combine all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)
    # Save the combined dataframe to a CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined metadata saved to {output_file}")

# Example usage
if __name__ == '__main__':
    input_directory = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Metadata'
    output_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Metadata/combined_metadata.csv'
    combine_metadata_files(input_directory, output_csv)
