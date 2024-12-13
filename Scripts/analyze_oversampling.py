import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_oversampling(balanced_file):
    # Read the balanced dataset
    df_balanced = pd.read_csv(balanced_file, dtype=str)

    # Assuming 'Sequence' uniquely identifies an entry
    # If not, adjust the columns used in the grouping
    entry_counts = df_balanced.groupby('Sequence').size()
    
    # Get the distribution of repetition counts
    repetition_counts = entry_counts.value_counts().sort_index()
    print("Distribution of entry repetition counts:")
    print(repetition_counts)

    # Original histogram of repetition counts
    plt.figure(figsize=(10, 6))
    repetition_counts.plot(kind='bar')
    plt.title('Histogram of Entry Repetition Counts')
    plt.xlabel('Number of Times an Entry is Repeated')
    plt.ylabel('Number of Entries')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # 1. Rank-Ordered Bar Plot of All Sequences
    sorted_counts = entry_counts.sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sorted_counts.reset_index(drop=True).plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Rank-Ordered Frequency of Individual Sequences')
    plt.xlabel('Sequence Rank (by Frequency)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    # 2. Cumulative Distribution Plot
    sorted_values = sorted_counts.values
    cum_dist = np.cumsum(sorted_values) / np.sum(sorted_values)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(sorted_values) + 1), cum_dist, marker='o', linestyle='-', color='red')
    plt.title('Cumulative Distribution of Sequence Frequencies')
    plt.xlabel('Sequence Rank (by Frequency)')
    plt.ylabel('Cumulative Proportion of All Entries')
    plt.tight_layout()
    plt.show()

    # 3. If Class Information is Available:
    # Assuming you have a 'Class' column
    if 'ProteinClass' in df_balanced.columns:
        # Merge repetition counts back into the dataframe
        df_with_counts = df_balanced[['Sequence', 'ProteinClass']].drop_duplicates()
        df_with_counts['Count'] = df_with_counts['Sequence'].map(entry_counts)

        # Box plot or violin plot to show distribution of counts by class
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_with_counts, x='ProteinClass', y='Count')
        plt.title('Distribution of Repetition Counts by ProteinClass')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Alternatively, a violin plot
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df_with_counts, x='ProteinClass', y='Count', inner='quartile')
        plt.title('Distribution of Repetition Counts by ProteinClass')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # 4. Correlation Plot (If There Are Other Numeric Features)
    # Suppose we have another numeric feature (like 'SequenceLength')
    if 'Sequence' in df_balanced.columns:
        # Example: Compute sequence length and see if there's correlation with repetition count
        df_with_features = df_balanced[['Sequence', 'ProteinClass']].drop_duplicates()
        df_with_features['Count'] = df_with_features['Sequence'].map(entry_counts)
        df_with_features['SequenceLength'] = df_with_features['Sequence'].apply(len)

        # Compute correlation matrix
        corr = df_with_features[['Count', 'SequenceLength']].corr()
        plt.figure(figsize=(6, 5))
        sns.heatmap(corr, annot=True, cmap='coolwarm', square=True)
        plt.title('Correlation Heatmap of Count vs. Sequence Length')
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == '__main__':
    balanced_csv = '/Users/simonpritchard/Documents/Academics/Junior_Year/ML_Tutorial/Protein_Project/Data/Sequences/balanced_seq.csv'
    analyze_oversampling(balanced_csv)