from Fade import FadeExecutor


def x(a, b): return [a + b, a - b]

with FadeExecutor() as f:
    future = f.submit(x, 5, 3)

result = future.result()
