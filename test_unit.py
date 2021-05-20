from subprocess import check_call

if __name__ == "__main__":
    check_call("python3 -m unittest discover -t . -s tests".split())
    # with Package() as pkg:
    #     pkg.run_python_code('import neatest; neatest.print_version()')
    #     pkg.run_shell_code('neatest --version')
    #
    # print("\nPackage is OK!")

