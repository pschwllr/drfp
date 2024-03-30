import typer
from typing import Optional
import pickle
from drfp import DrfpEncoder

def run():
    typer.run(main)

def main(
    input_file: typer.FileText = typer.Argument(..., help="The file containing one reaction SMILES per line."),
    output_file: typer.FileBinaryWrite = typer.Argument(..., help="The output file, a pickle file containing the corresponding list of fingerprints."),
    n_folded_length: int = typer.Option(2048, "--n_folded_length", "-d", help="The length / dimensionality of the fingerprint. Good values are between 128 and 2048."),
    min_radius: int = typer.Option(0, "--min_radius", "-m", help="The minimum radius used to extract circular substructures from molecules. 0 includes single atoms."),
    radius: int = typer.Option(3, "--radius", "-r", help="The radius, or maximum radius used to extract circular substructures from molecules."),
    rings: bool = typer.Option(True, "--rings/--no-rings", help="Whether or not to extract whole rings as substructures."),
    mapping: bool = typer.Option(False, "--mapping/--no-mapping", help="Whether or not to also export a mapping to help interpret the fingerprint."),
    hydrogens: bool = typer.Option(False, "--hydrogens", help="Include hydrogens explicitly."),
    root: bool = typer.Option(False, "--root", help="Root central atoms during substructure generation."),
    silent: bool = typer.Option(False, "--silent", help="Hide all output such as the progress bar.")
):
    """Creates fingerprints from a file containing one reaction SMILES per line."""

    smiles = [line.strip() for line in input_file]

    show_progress_bar = not silent

    fps = None
    fragment_map = None

    # Assuming DrfpEncoder.encode() is a placeholder for the actual encoding function
    if mapping:
        fps, fragment_map = DrfpEncoder.encode(
            smiles,
            n_folded_length,
            min_radius,
            radius,
            rings,
            mapping,
            root_central_atom=root,
            show_progress_bar=show_progress_bar,
            include_hydrogens=hydrogens,
        )
    else:
        fps = DrfpEncoder.encode(
            smiles,
            n_folded_length,
            min_radius,
            radius,
            rings,
            mapping,
            root_central_atom=root,
            show_progress_bar=show_progress_bar,
            include_hydrogens=hydrogens,
        )

    pickle.dump(fps, output_file)

    if mapping:
        filename_parts = output_file.name.split(".")
        filename_parts.insert(len(filename_parts) - 1, "map")
        with open(".".join(filename_parts), "wb+") as f:
            pickle.dump(fragment_map, f)

if __name__ == "__main__":
    run()
