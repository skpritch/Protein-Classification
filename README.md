# Protein Family Classification: A Machine Learning Approach to Investigating Feature Engineering and Data Sufficiency

**Author:** Simon Pritchard  
**Affiliation:** Stanford University, Department of Biology  
**Contact:** [skpritch@stanford.edu](mailto:skpritch@stanford.edu)

---

## Abstract

Accurate protein classification remains one of the greatest challenges—and opportunities—in Biology. With the advent of cheaper, longer-read sequencing, the growth of sequence databases has vastly outpaced that of experimental validation of proteins. Classification of such sequences is instrumental in investigating novel proteins for therapeutic or academic purposes. While significant progress has been made by complex models such as AlphaFold, ESMFold, and Protein MPNN in predicting protein structure, sequence, and function, these approaches face challenges related to computational resource requirements and interpretability. This project examines the potential of classical, supervised machine-learning models trained on feature-engineered data for protein classification. To simulate resource constraints, forced data scarcity is employed as a proxy for limited computational resources. Results indicate that in data-poor scenarios, classical models achieve high predictive accuracy, whereas more complex architectures (e.g., neural networks, RNNs, LSTMs) often fail to perform better than random.

---

## Keywords
Amino Acid (AA), Peptide Sequence, Protein, ReLU, Cross Entropy Loss, Softmax, Logistic Regression, Random Forest, Gradient Boost, Neural Network, Recurrent Neural Network (RNN), Long-Short-Term Memory (LSTM)  

## File System
- Protein_Classification.ipynb: Code to run and evaluate models classifying proteins by class
- 
