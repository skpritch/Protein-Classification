import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Added for plotting

def balance_dataset(input_file, output_file, method='undersample', target_count=100):
    # Read the extracted features file
    df = pd.read_csv(input_file, dtype=str)

    # Get the counts of each class
    class_counts = df['ProteinClass'].value_counts()
    print("Original class distribution:")
    print(class_counts)

    # Plot histogram of the original class distribution
    plt.figure(figsize=(10, 6))
    class_counts.plot(kind='bar')
    plt.title('Class Distribution Before Balancing')
    plt.xlabel('Protein Class')
    plt.ylabel('Number of Instances')
    plt.tight_layout()
    plt.show()

    if method == 'undersample':
        # Determine the target count
        if target_count is None:
            target_count = class_counts.min()
            print(f"Target count per class (minimum class size): {target_count}")

        # Under-sample each class to the target count
        df_balanced = df.groupby('ProteinClass').apply(
            lambda x: x.sample(n=target_count, random_state=42)
        )
        df_balanced = df_balanced.reset_index(drop=True)
    elif method == 'oversample':
        # Determine the target count
        if target_count is None:
            target_count = class_counts.max()
            print(f"Target count per class (maximum class size): {target_count}")

        # Over-sample each class to the target count
        df_balanced = df.groupby('ProteinClass').apply(
            lambda x: x.sample(n=target_count, replace=True, random_state=42)
        )
        df_balanced = df_balanced.reset_index(drop=True)
    else:
        print("Invalid method. Choose 'undersample' or 'oversample'.")
        return

    # Shuffle the dataset
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    # Save the balanced dataset
    """df_balanced.to_csv(output_file, index=False)
    print("Balanced dataset saved to", output_file)"""

    # Print new class distribution
    new_class_counts = df_balanced['ProteinClass'].value_counts()
    print("New class distribution:")
    print(new_class_counts)

    # Optional: Plot histogram of the new class distribution after balancing
    # Uncomment the following lines if you want to see the distribution after balancing
    # plt.figure(figsize=(10, 6))
    # new_class_counts.plot(kind='bar')
    # plt.title('Class Distribution After Balancing')
    # plt.xlabel('Protein Class')
    # plt.ylabel('Number of Instances')
    # plt.tight_layout()
    # plt.show()

# Example usage
if __name__ == '__main__':
    input_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Sequences/extracted_features.csv'
    output_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Sequences/balanced_seq.csv'
    # Choose method: 'undersample' or 'oversample'
    balance_method = 'oversample'  # or 'undersample'
    balance_dataset(input_csv, output_csv, method=balance_method)