"""Vast cloud adaptor."""

import functools

from sky import skypilot_config

_vast_sdk = None


def import_package(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global _vast_sdk

        if _vast_sdk is None:
            try:
                import vastai_sdk as _vast  # pylint: disable=import-outside-toplevel
                _vast_sdk = _vast.VastAI()
            except ImportError as e:
                raise ImportError(f'Fail to import dependencies for vast: {e}\n'
                                  'Try pip install "skypilot[vast]"') from None
        return func(*args, **kwargs)

    return wrapper


@import_package
def vast():
    """Return the vast package."""
    return _vast_sdk


def get_secure_cloud_only() -> bool:
    """Checks if secure cloud only mode is enabled for Vast.ai."""

    secure_cloud_only = skypilot_config.get_effective_region_config(
        cloud='vast',
        region=None,
        keys=('secure_cloud_only',),
        default_value=False)
    return secure_cloud_only
