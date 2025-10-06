import time
import chip_solver_mix
import chip_solver_large

tot_time = 0
for i in range(1):
    start_time = time.time()

    cnffile = ''  # Input path to the cnf

    cnffile_new = ''
    scheme = 1
    digital_backup = 0

    # Set to 1 if we need to run Solver Algorithm after some iterations
    if digital_backup == 1:

        X_final, sat_time, flip_time, total_time, MCMC_time = chip_solver_mix.chip_solver_mix(cnffile,cnffile_new, scheme)

        print("The SAT solution is : ")
        print(X_final)

    else:

        X_final, sat_time, flip_time, total_time = chip_solver_large.chip_solver_large(cnffile,cnffile_new, scheme)

        print("The SAT solution is : ")
        print(X_final)