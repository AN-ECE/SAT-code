import time
import chip_solver_k_sat

tot_time = 0
for i in range(1):
    start_time = time.time()

    cnffile = ''  # Input path to the cnf

    cnffile_new = ''
    scheme = 1

    X_final, sat_time, flip_time, total_time = chip_solver_k_sat.chip_solver_k_sat(cnffile,cnffile_new, scheme)

    print("The SAT solution is : ")
    print(X_final)