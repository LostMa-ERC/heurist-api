"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
package = root.joinpath("heurist")

# Recursively get python files in the package directory
for path in sorted(package.rglob("*.py")):
    # Parse the python module's path
    module_path = path.relative_to(package).with_suffix("")
    # Build the
    doc_path = path.relative_to(package).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[0] == "mock_data" or parts[0] == "cli":
        continue
    if parts[-1] == "constants.py":
        continue

    if parts[-1] == "__init__":
        parts = parts[:-1]
    elif parts[-1] == "__main__":
        continue
    elif parts[0] == "__init__":
        continue
    if str(full_doc_path).endswith("__init__.md"):
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())
