# Canny Edge Detection

## Cel
Prosty projekt do wykrywania krawędzi metodą Canny:
- jako kod eksperymentalny w `experiment.py`,
- jako aplikacja GUI w `gui/main.py` (podgląd obrazu i suwaków progów).

## Instalacja
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uruchomienie
GUI:
```bash
python3 gui/main.py
```

Kod eksperymentalny (we własnym skrypcie / notebooku):
```python
from experiment import Experiment, ExperimentPlotter

exp = Experiment("sciezka/do/obrazu.jpg", threshold1=100, threshold2=200)
exp.run()
ExperimentPlotter.plot_edges(exp)
```
