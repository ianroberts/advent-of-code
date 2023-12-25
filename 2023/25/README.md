# 2023 Day 25

I kind of cheated on this one - rather than programming anything significant I

- converted the puzzle input to graphviz format
- rendered the graphviz as a force-directed graph in SVG using `sfdp`
  - this clearly showed two dense clusters with just three edges connecting them
- manipulated the SVG (with XSLT) to remove all the edges but leave the nodes in place
- manually drag-selected the clusters in Inkscape to count the number of nodes in each one