import logging
from charm4py import charm
import sys
import mpi4py
mpi4py.rc.initialize = False
import argparse
import commi

def dummy_main(args):

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="MIRGE-Com Isentropic Nozzle Driver")
    parser.add_argument("-r", "--restart_file", type=ascii, dest="restart_file",
                        nargs="?", action="store", help="simulation restart file")
    parser.add_argument("-t", "--target_file", type=ascii, dest="target_file",
                        nargs="?", action="store", help="simulation target file")
    parser.add_argument("-i", "--input_file", type=ascii, dest="input_file",
                        nargs="?", action="store", help="simulation config file")
    parser.add_argument("-c", "--casename", type=ascii, dest="casename", nargs="?",
                        action="store", help="simulation case name")
    parser.add_argument("-g", "--logpath", type=ascii, dest="log_path", nargs="?",
                        action="store", help="simulation case name")
    parser.add_argument("--profile", action="store_true", default=False,
                        help="enable kernel profiling [OFF]")
    parser.add_argument("--log", action="store_true", default=False,
                        help="enable logging profiling [ON]")
    parser.add_argument("--lazy", action="store_true", default=False,
                        help="enable lazy evaluation [OFF]")
    parser.add_argument("--overintegration", action="store_true",
        help="use overintegration in the RHS computations")

    args = parser.parse_args()

    # for writing output
    casename = "prediction"
    if args.casename:
        print(f"Custom casename {args.casename}")
        casename = args.casename.replace("'", "")
    else:
        print(f"Default casename {casename}")
    lazy = args.lazy
    if args.profile:
        if lazy:
            raise ValueError("Can't use lazy and profiling together.")

    from grudge.array_context import get_reasonable_array_context_class
    actx_class = get_reasonable_array_context_class(lazy=lazy, distributed=True)

    restart_filename = None
    if args.restart_file:
        restart_filename = (args.restart_file).replace("'", "")
        print(f"Restarting from file: {restart_filename}")

    target_filename = None
    if args.target_file:
        target_filename = (args.target_file).replace("'", "")
        print(f"Target file specified: {target_filename}")

    input_file = None
    if args.input_file:
        input_file = args.input_file.replace("'", "")
        print(f"Using user input from file: {input_file}")
    else:
        print("No user input file, using default values")

    log_path = "log_data"
    if args.log_path:
        log_path = args.log_path.replace("'", "")

    print(f"Running {sys.argv[0]}\n")

    from y3prediction.prediction import main
    comm = commi.CreateCharmCommunicator([8], 8)
    comm.begin_exec(main, None, 
    restart_filename, target_filename,
    args.profile, args.log, 
    input_file, args.overintegration, actx_class,
    casename,
    lazy, log_path)

charm.start(dummy_main)
