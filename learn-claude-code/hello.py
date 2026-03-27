"""Module for printing a greeting message."""


def hello(name: str = "World") -> None:
    """Print a greeting message to the console.

    Args:
        name: The name to greet. Defaults to "World".
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    hello()
