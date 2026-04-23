# VRP Coursework helpers

This folder contains the coursework code and small wrapper modules so the
provided `tests.py` can import solvers as separate modules.

Files added:

- `vrp_core.py` — exposes `VRP` and `generate_random_instance` from `vrp_coursework.py`
- `vrp_naive.py` — `greedy_nearest_neighbor(instance)` wrapper
- `vrp_improved.py` — `clarke_wright_savings(instance)` wrapper
- `benchmark.py` — `plot_comparison(instances_info, outpath)` helper
- `requirements.txt` — lists `matplotlib`

To run the example tests (from Windows PowerShell):

```powershell
py "./tests.py"
```
