# point-mutation-prediction

________________________________________
Project Title (generalized)
“Prediction model to analyze the impact of point mutations of DNA codons on protein structure and function.”
________________________________________
Primary Objective
•	To develop a computational model that predicts the effect of a point mutation on a protein, including whether it is deleterious, neutral, or causes truncation.
________________________________________
Secondary Objectives
1.	Classify mutation types
o	Distinguish between silent, missense, and nonsense mutations.
o	Flag truncated proteins automatically.
2.	Quantify biochemical changes
o	Calculate changes in hydrophobicity, molecular weight, charge, and polarity caused by mutations.
3.	Predict functional impact
o	Use machine learning to determine if a mutation will affect protein stability, folding, or activity.
4.	Provide structural insights (optional/advanced)
o	Visualize mutation effects on 3D protein structure using computational tools (PyMOL, AlphaFold).
5.	Create a generalizable workflow
o	Ensure the model can handle any gene/protein and any single-nucleotide mutation.
6.	Lay foundation for future research/publication
o	Demonstrate that the workflow can screen mutations for potential deleterious effects in disease-related genes.
________________________________________
Summary of Key Goals
1.	Input: DNA codon mutation
2.	Process: Translate → amino acid → calculate Δfeatures → ML model → classify effect
3.	Output:
o	Mutation type (silent/missense/nonsense)
o	Protein truncated? (Yes/No)
o	Predicted effect (deleterious/neutral)
o	 Structural visualization

USED LIBRARIES

pip install torch torchvision torchaudio
pip install biopython
pip install pandas numpy scikit-learn
pip install networkx
pip install matplotlib
pip install rdkit-pypi         
pip install torch-geometric     
pip install einops             
pip install requests

WHAT DOES THE ML MODEL ACTUALLY DO
 Take DNA sequence
 Detect the mutation inside it
Classify mutation
•	silent
•	missense
•	nonsense
•	frameshift
•	splice-site
•	promoter mutation
Predict its biochemical impact
Predict amino acid change
Analyze protein structure change using GNN
Show structure visualization (optional: PyMol, AlphaFold model download)
  Generate a report


There will be two models working simultaneously A sequential model and a GNN model

DNA sequence
     │
     ▼
Mutation Detection Model (Sequence Model)
     │  
     ├── Mutation type prediction
     └── Mutated codon → amino acid conversion
     ▼
Protein Sequence Generator
     │
     ▼
Protein Structure Fetcher (AlphaFold / PDB)
     │
     ▼
Graph Constructor (Residue-level graph)
     │
     ▼
GNN Model for Structure Impact
     │
     ▼
Final Report
    - Mutation class
    - Amino acid change
    - Structural disruption
    - Stability change (ΔΔG)
    - Functional interpretation
SEQUENTIAL MODE
Purpose
Detects and classifies mutations directly from a DNA sequence.
Input:
Encoded DNA nucleotides (A, C, G, T → 0,1,2,3)
Output:
Mutation class (6 classes):
•	silent
•	missense
•	nonsense
•	frameshift
•	splice-site
•	regulatory/promoter

Model Architecture (Sequence Model)
A simple but powerful LSTM-based classifier:

Embedding Layer (4 → 32 dim)
     ↓
Bidirectional LSTM (hidden 64)
     ↓
Fully Connected Layer
     ↓
Softmax (6 classes)

Advantages:
•	Learns codon patterns
•	Understands local sequence context
•	Good for short and medium-length sequences


4.2 Mutation Impact Engine
Once a mutation is identified:
1. Codon → Amino Acid Conversion
The mutated codon is translated and compared to reference.
2. Mutation Type Verification
•	If amino acid does not change → silent
•	If amino acid changes → missense
•	If codon becomes STOP → nonsense
________________________________________
4.3 Protein Sequence Generator
The DNA sequence is translated into a full protein sequence in FASTA format.
________________________________________
4.4 Protein Structure Acquisition
Source options:
•	AlphaFold2 Protein Structure Database
•	PDB (Protein Data Bank)
If no structure exists, AlphaFold model is used.
Output: 3D atomic coordinates (.pdb file)
________________________________________
5. Protein Graph Construction
To analyze structure with GNNs, the protein must be turned into a graph.
Nodes:
Each amino acid residue
Node Features:
•	Residue type (20 aa)
•	Hydrophobicity
•	Charge
•	Polarity
•	Secondary structure prediction
Edges:
Edges between residues within 8 Å distance (spatial graph)
________________________________________
6. Graph Neural Network for Structure Impact
Purpose
Predict how the mutation changes:
•	Protein stability
•	Foldability
•	Domain disruption
•	Long-range interactions
•	Active site geometry
________________________________________
Model Architecture (GNN)
A GCN (Graph Convolutional Network):
Node Features (20 dim)
       ↓
GraphConv Layer 1 (ReLU)
       ↓
GraphConv Layer 2 (ReLU)
       ↓
Global Mean Pooling
       ↓
Fully Connected Layer → Stability / Function Score


GNN Output Predictions
The model predicts:
✔ ΔΔG (Stability Change Score)
•	Negative → destabilizing mutation
•	Positive → stabilizing mutation
✔ Structural Clash / Disruption Score
✔ Functional Loss Probability

7. Integration of Both Models
The system fuses:
Sequence Intelligence
(LSTM/Transformer prediction)
+ Structural Intelligence
(GNN prediction)
to generate a comprehensive biological interpretation.




