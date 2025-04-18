import marimo

__generated_with = "0.12.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    return np, plt


@app.cell
def _(np):
    def f(x, r):
        return r * x * (1 - x)

    r_vals, x_vals = [], []
    R = np.linspace(1, 4, 500)

    n, m = 500, 1000

    for r in R:
        x = np.random.uniform(0, 1)
        for i in range(n + m):
            x = f(x, r)
            if i > n:
                r_vals.append(r)
                x_vals.append(x)
    return R, f, i, m, n, r, r_vals, x, x_vals


@app.cell
def _(plt, r_vals, x_vals):
    # Plotting the bifurcation diagram
    plt.figure(figsize=(15, 5))
    plt.plot(r_vals, x_vals, ",k", alpha=0.25)
    plt.xlabel("r")
    plt.ylabel("x")
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
