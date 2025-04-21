from dataclasses import dataclass


@dataclass
class Config:
    """
    Config class for managing application configuration settings.

    Attributes:
        csrf_secret (str): A secret key used for CSRF protection.
        csrf (bool): A flag indicating whether CSRF protection is enabled.
    """

    csrf_secret: str
    csrf_enabled: bool
