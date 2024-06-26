# Hopfield Model Synthetic Data Generation

## Model Parameters
- **L**: Sequence length
- **n**: Number of patterns
- **N**: Number of proteins/species

Each protein sequence is represented by a spin vector \( s \) of length \( L \), where each element takes values of \( +1 \) or \( -1 \).

## Hopfield Model

The Hamiltonian used for the Hopfield model is:
\[ H = -\frac{1}{2}\sum_{i=1}^L\sum_{j=1}^L J_{ij}s_i s_j \]

The weight matrix follows the Hebbian learning rule:
\[ J_{ij} = \frac{1}{L}\sum_{\mu=1}^n x^\mu_i x^\mu_j \]
where \( x \) is a pre-generated pattern.

## Synthetic Data Generation

In the synthetic data:
- **L = 5000**
- **N = 100**

For a network of this size, its storage capacity is:
\[ \alpha = 0.138 L = 690 \]

To generate 100 artificial sequences, I used Gibbs sampling. Starting with a random initialization of the spin vector, I randomly select a spin at each step and update it based on the following probability function:
\[ P(s_i = 1|s_{j \neq i}) = \frac{1}{1 + \exp(-2\sum_j J_{ij}s_j)} \]

After the burn-in time, I collected \( s \) every 500 steps and repeated this process 100 times. Combining all the \( s \) vectors, I obtained the desired \( 100 \times 5000 \, X \) matrix.

## Generating the Y Data

For the one-column \( Y \) data, I calculated the corresponding energy for each sequence. To obtain binary \( Y \) data, we can apply thresholding to the energy values.

## Verification

To verify that the algorithm works, I tested with \( n = 690 \) patterns at the network's maximum capacity. Initializing the spin as the 50th pattern, the spin stayed in this state throughout the sampling, indicating that the network is capable of memorizing the patterns.

![Pattern Memory](https://github.com/Oldcharm/hofield-synthetic-data/assets/60882513/5b8c5d8f-05e1-4736-a0eb-9d9c9c1e43d2)

## Equilibrium Check

To ensure the system reached equilibrium when collecting \( X \) data, I calculated the autocorrelation for spin 0, which decreased to 0 rapidly.

![Autocorrelation](https://github.com/Oldcharm/hofield-synthetic-data/assets/60882513/61339bf6-5f7e-4732-8bdb-c074f3294654)

The energy of the system also fluctuated around its minimum after the burn-in time.

![Energy Fluctuation](https://github.com/Oldcharm/hofield-synthetic-data/assets/60882513/68487710-685a-4d54-b058-869e5746c544)

## Dimensionality Analysis

Finally, I computed the covariance of all the protein sequences and ran PCA on it to determine the dimensionality.

![PCA](https://github.com/Oldcharm/hofield-synthetic-data/assets/60882513/b236b84b-42f4-4584-943b-daa6f45596b1)

The participation ratio (PR) decreased from 7 to 4 as the pattern number increased from 50 to 600. For real protein sequence data, the PR value typically ranges from 1 to 15, depending on how conserved the protein family is across evolution. Therefore, the dimensionality of the \( X \) data should be comparable to realistic biological data.
