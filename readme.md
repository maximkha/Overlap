# Overlap

Overlap is a simple python program made to do pseudo sequence alignment. Pseudo sequence alignment means that it is a naïve verbatim search algorithm. This allows for quick rough alignment, the results are very close to real alignment and the process takes a fraction of a second. The only caveat is that the closer the two genomes are, the more accurate the alignment will be.

#### Experiment

I took the sequence of a very early version of COVID, [HCoV-HKU1](https://www.ncbi.nlm.nih.gov/nuccore/306569684), this specific version was sequenced in 2010, however the actual virus was first seen January 2004. I used the National Institutes of Health’s genome breakdown to find the spike glycoprotein, which was located from base pair 22906 to base pair 26076. I extracted the amino acid sequence of the protein and ran the program against the current strain of COVID’s genome, sequenced in July 2020:

*Note, the best match is zero based, while most genetics systems start at one.*

`Total Length 29903, Needle Length: 4069, TotalOut: 25834
Best Match: 21309 with value of 0.34209879577291713`

 ![matchAllign](img\matchAllign.png)

As we can see, at base pair 21310, of the current COVID strain, there is a naïve 34% similarity between the old protein and that subsection of the current COVID genome. Checking this with the [official NIH’s spike protein base](https://www.ncbi.nlm.nih.gov/nuccore/MN988713.1) pair range: 21563 to 25384. The estimate is off by 253 base pairs. The actual similarity is shown below:

![diff](img\diff.png)

So we can see, that from around base pairs 3000 to 3750 are pretty much in common with the current Covid spike protein (note this is the approximately aligned version).