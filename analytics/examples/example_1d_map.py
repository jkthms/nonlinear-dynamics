import marimo

__generated_with = "0.12.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    from typing import List

    return List, math, mo, np, plt


@app.cell
def _(mo):
    x0 = mo.ui.slider(start=-1.0, stop=1.0, step=0.01, label="x0")
    x0
    return (x0,)


@app.cell
def _(List, math):
    def run(x0: float = 0.0, steps: int = 25) -> List[float]:
        step = lambda x: math.cos(x)
        result = []
        for _ in range(steps + 1):
            result.append(x0)
            x0 = step(x0)
        return result

    return (run,)


@app.cell
def _(plt, run, x0):
    plt.figure(figsize=(15, 5))
    iteration = run(x0.value)
    plt.plot(list(range(len(iteration))), iteration, "k")
    plt.xlabel("n")
    plt.ylabel("x_n")
    plt.show()
    return (iteration,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
