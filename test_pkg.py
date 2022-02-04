from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_python_code('import neatest; neatest.print_version()')
        pkg.run_shell_code('neatest --version')

    print("\nPackage is OK!")

