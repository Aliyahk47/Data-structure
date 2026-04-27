import os
import matplotlib.pyplot as plt
from vrp_core import VRP
from vrp_naive import greedy_nearest_neighbor
from vrp_improved import clarke_wright_savings
from vrp_ai_advanced import solve as or_opt_solve
from benchmark import plot_comparison

# Import your test modules
import test_data_1_tiny
import test_data_2_small
import test_data_3_medium
import test_data_4_large
import test_data_5_constrained

def run_python_file_tests():
    os.makedirs('outputs', exist_ok=True)
    
    # List of the imported modules
    test_modules = [
        test_data_1_tiny,
        test_data_2_small,
        test_data_3_medium,
        test_data_4_large,
        test_data_5_constrained
    ]
    
    instances_info = []
    
    for module in test_modules:
        test_dict = module.data
        name = test_dict['name']
        print(f"Processing Python test file: {name}...")
        
        inst = VRP.from_dict(test_dict)
        
        # Run solvers
        g = greedy_nearest_neighbor(inst)
        cw = clarke_wright_savings(inst)
        ai_or = or_opt_solve(inst)
        
        # Calculate distances
        dg = inst.total_distance(g)
        dcw = inst.total_distance(cw)
        dai = inst.total_distance(ai_or)
        
        # Store for summary plot
        instances_info.append((name, inst, {
            'greedy': (dg, None, g),
            'clarke_wright': (dcw, None, cw),
            'or_opt': (dai, None, ai_or)
        }))
        
        # Save individual plot for this test file
        fig, ax = plt.subplots()
        ax.bar(['Greedy', 'CW', 'AI Or-Opt'], [dg, dcw, dai], color=['C0', 'C1', 'C2'])
        ax.set_title(f"Test Instance: {name}")
        fig.savefig(f"outputs/result_{name}.png")
        plt.close(fig)

    # Summary comparison plot
    plot_comparison(instances_info, outpath='outputs/final_comparison.png')
    print("Tests complete. Plots saved to 'outputs/' folder.")

if __name__ == '__main__':
    run_python_file_tests()