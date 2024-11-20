import coverage
from pathlib import Path

def print_coverage(test_file, actual_file):
    cov = coverage.Coverage(branch=True, source=[str(Path(actual_file).resolve().parent)])
    cov.start()

    try:
        import pytest
        pytest.main([test_file])
    finally:
        cov.stop()
        cov.save()

    print(f"\nCoverage for {actual_file} while running {test_file}:\n")
    cov.report([str(Path(actual_file).resolve())])

    _, statements, missing, branches, partial_branches = cov.analysis2(str(Path(actual_file).resolve()))

