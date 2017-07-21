from Fade import FadeExecutor


def h(x): x


with FadeExecutor() as f:
    future = f.submit(h, "tryme")

result = future.result()
