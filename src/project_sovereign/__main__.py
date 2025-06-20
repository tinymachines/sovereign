#!/usr/bin/env python3
"""
PROJECT SOVEREIGN package entry point.

This module allows the package to be run directly with python -m project_sovereign.
"""

import sys

from .cli.main import cli


def main():
    """Main entry point for PROJECT SOVEREIGN."""
    # Click handles sys.argv automatically
    cli()


if __name__ == "__main__":
    main()