Overview


master_algo.m is the main script for solving k-SAT problems using a reduction to 3-SAT and applying a Solver Algorithm. It processes CNF/DIMACS files and provides the final SAT state.

Input Parameters
The function takes the following inputs:
•	cnffile (string): Path to the k-SAT CNF/DIMACS file (Line 9).
•	cnffile_new (string, optional): Path to save the 3-SAT reduced CNF file if needed. Default is an empty string ('') (Line 11).
•	digital_backup (integer, optional): (Line 13)
    ⁃	Set to 1 to run the Solver Algorithm on the k-SAT problem after a certain number of iterations .
    ⁃	Usually set to 1 when the 3-SAT reduced problem has more than 4000 variables.
    ⁃	Default value: 0.

Output
The function displays the following outputs:
▪	X: Final SAT state for all the variables.
