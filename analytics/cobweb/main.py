import numpy as np
import matplotlib.pyplot as plt


def plot_cobweb(x, y, iters, vals):
    plt.figure(figsize=(12, 5))

    x_min, x_max = min(iters), max(iters)
    y_min, y_max = min(vals), max(vals)
    x_margin = (x_max - x_min) * 0.2
    y_margin = (y_max - y_min) * 0.2

    plt.xlim(x_min - x_margin, x_max + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)

    plt.plot(x, x, linestyle="-", color="darkgray", linewidth=2)
    plt.plot(x, y, color="navy", linewidth=2)

    for i in range(len(iters) - 1):
        plt.plot(
            [iters[i], iters[i]],
            [vals[i], vals[i + 1]],
            color="red",
            linewidth=1.3,
        )

        plt.plot(
            [iters[i], iters[i + 1]],
            [vals[i + 1], vals[i + 1]],
            color="red",
            linewidth=1.3,
        )

        start_x_v = iters[i]
        start_y_v = vals[i]
        start_x_h = iters[i]
        start_y_h = vals[i + 1]

        mid_y_v = (vals[i] + vals[i + 1]) / 2
        mid_x_h = (iters[i] + iters[i + 1]) / 2

        plt.arrow(
            start_x_v,
            start_y_v,
            0,
            (mid_y_v - start_y_v),
            head_width=0.01,
            head_length=0.02,
            fc="red",
            ec="red",
            width=0.005,
            length_includes_head=True,
        )
        plt.arrow(
            start_x_h,
            start_y_h,
            (mid_x_h - start_x_h),
            0,
            head_width=0.01,
            head_length=0.02,
            fc="red",
            ec="red",
            width=0.005,
            length_includes_head=True,
        )

    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)

    plt.xlabel("$x_{n}$", fontsize=12)
    plt.ylabel("$x_{n+1}$", fontsize=12)

    plt.xticks([])
    plt.yticks([])

    return plt.gcf()


def cobweb(f, x0, xmin, xmax, max_iters=50, num_points=1000, tol=1e-6):
    x = np.linspace(xmin, xmax, num_points)
    y = f(x)

    xn = x0
    iters = []
    vals = []

    for n in range(max_iters):
        iters.append(xn)
        vals.append(xn)

        xn_next = f(xn)

        iters.append(xn)
        vals.append(xn_next)

        iters.append(xn_next)
        vals.append(xn_next)

        if abs(xn_next - xn) < tol:
            break

        xn = xn_next

    return plot_cobweb(x, y, iters, vals)


def f(x):
    return np.cos(x)


def g(x):
    return 3.7 * x * (1 - x)


x0 = 0.01
max_iters = 20
tolerance = 1e-3

lr, rr = -5, 5
x = np.linspace(lr, rr, 1000)

cobweb(g, x0, lr, rr, max_iters=max_iters, tol=tolerance)
plt.show()
