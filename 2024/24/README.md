# 2024 Day 24

Part 1 is the python code in `circuit.py`.

For part 2, I converted the input into CSV format - the connections become this (with the OP name converted to lower case):

`a OP b -> c` → `c,"a,b",op` 

and the input `x` and `y` lines become

`name,"",in`

I then added some preamble to set the formatting rules for https://app.digrams.net:

```
## Topology
# namespace: csvimport-
# label: %name%
# connect: {"from": "inputs", "to": "name", "tolabel": "name", "invert": true}
# stylename: op
# styles: {"xor": "shape=mxgraph.electrical.logic_gates.logic_gate;operation=xor", "and": "shape=mxgraph.electrical.logic_gates.logic_gate;operation=and", "or": "shape=mxgraph.electrical.logic_gates.logic_gate;operation=or"}
# layout: verticalflow
name,inputs,op
```

This then imported into diagrams.net using arrange -> insert -> advanced -> CSV, and drew a pretty picture of the whole 45-bit adder.  I knew three of the gates I was looking for straight off because in a correctly configured adder all of the z bits apart from the most significant (`z45`) should be the output of an XOR operation, and there were three in my file that were ANDs or ORs instead.  The final one I found by inspecting the diagram and looking for a full-adder that didn't look the same as the ones either side.

I then spent about an hour puzzling over why my answer was wrong, until I realised I had mis-typed one of the node names when transcribing from the diagram to the solution page...