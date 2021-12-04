
# Parsl - Parallel Scripting Library for Python : Benchmarking, Analysis, Expedition & Improvement


This project was conducted by AI major students of Illinois Institute of Technology. We would like to thank Dr. Ioan Raicu, our supervisor for this research project and for the "Data Intensive Computing" course. We are extremely glad for this opportunity to learn about numerous fields outside of our expertise such as parallel computing in Python.

## Team members

- Ismail Elomari Alaoui
- Reda Chaguer

## Abstract
Parsl is a parallel scripting library for Python. It facilitates and improves using multi-threading and parallel scripting in Python. Despite having other competitor libraries Parsl has proven to be one of the fastest, but it is still slow in comparison with other low level libraries. We will benchmark Parsl in numerous use cases and examine the situations where Parsl excels, but also study other cases, such as fine-grained parallelism, where it fails to create a fast, highly-scalable parallel script.

## Github Depository Arborescence

This depository contains The report, the presentation slides and the source code.

To install prerequisites on debian distribution on Linux , run `make install` or directly install *Python3.8* and using *pip* install parsl and pandas libs.

To launch the Benchmarking scripts, run `make launch_bench` and the output files will be in the *bench_outputs* and *bench_configs* folders.

To visualize the result, use the Jupyter Notebook or the equivalent Python script in the visualisation section and import the outputted  CSVs by modifying the file names in the first cell of the code to generate the different graphs shown in the final report.