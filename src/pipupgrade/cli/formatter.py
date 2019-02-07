# imports - standard imports
import argparse

class ArgumentParserFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter
):
    pass