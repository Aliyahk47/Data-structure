VRP Coursework Implementation Portfolio

This repository contains a modular Python implementation for solving the Capacitated Vehicle Routing Problem (CVRP). The project evaluates a hierarchy of algorithms—ranging from a simple greedy baseline to an advanced AI-supported relocation heuristic—using a set of six unique test instances.

Project Structure

The implementation is broken down into separate modules for clarity and maintainability:  

vrp_core.py: Core data structures, the VRP class, and the distance matrix computation.  

vrp_naive.py: Implementation of the Greedy Nearest Neighbor initial solver.  

vrp_improved.py: Implementation of the Clarke-Wright Savings algorithm with 2-opt local search refinement.  

vrp_ai_advanced.py: Implementation of the advanced Or-opt inter-route relocation solver.  

benchmark.py: Visualization utilities used to generate comparison graphs.  

tests.py: The primary execution script that runs all six test modules and saves the benchmarking plots.

Test Data Modules

The project includes six pre-defined test instances of varying difficulty:  

test_data_1_tiny.py: 5 customers  

test_data_2_small.py: 10 customers  

test_data_3_medium.py: 20 customers  

test_data_4_large.py: 40 customers  

test_data_5_constrained.py: Tightened capacity limits (10 units)  

test_data_6_stress.py: 100-customer "stress test" for scalability

Installation

Ensure you have Python 3.x installed. Install the necessary dependencies for plotting

 `requirements.txt`  lists `matplotlib`

 pip install -r requirements.txt
 pip install matplotlib


To run the example tests:
run the test.py files or 

```powershell
py "./tests.py"
```
to get the comparison graph:
run the vrp_coursework.py 