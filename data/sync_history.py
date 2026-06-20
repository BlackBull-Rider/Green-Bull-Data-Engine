from providers.nse_provider import (
    NSEProvider
)


def main():

    provider = NSEProvider()

    provider.get_history(
        "RELIANCE",
        "2020-01-01",
        "2025-12-31"
    )


if __name__ == "__main__":
    main()
