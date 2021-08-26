import argparse

from dicom_phi_check.find_phi import find_phi


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI tool for identifying and optionally overwriting DICOM fields with patient health information."
    )
    parser.add_argument("path", help="path to a DICOM file or folder with DICOM files")
    parser.add_argument(
        "--overwrite", help="overwrite original files with anonymized files", default=False, action="store_true"
    )
    parser.add_argument("--verbose", "-v", help="verbose printing", default=False, action="store_true")
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    print(f"Overwrite is set to {args.overwrite}")
    print(f"Verbose is set to {args.verbose}")
    find_phi(args.path, args.overwrite, args.verbose)


if __name__ == "__main__":
    main(parse_args())
