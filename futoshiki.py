"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#
import numpy as np
import time
import copy
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains
        
    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of all variables based on the values
        of reassigned variables
        '''
        #======================================================================#
		#*#*#*# TODO: Write your implementation of forward checking here #*#*#*#
		#======================================================================#

        for var in reassigned_variables:
            row = ROW.index(var[0])
            col = COL.index(var[1])
            assigned_value = self.config[var]

            for a in range(self.n):                                     # Row/Column Removal
                if self.config[ROW[row] + COL[a]] == 0:                 # Row
                    if assigned_value in self.domains[ROW[row] + COL[a]]:
                        self.domains[ROW[row] + COL[a]].remove(assigned_value)
                
                if self.config[ROW[a] + COL[col]] == 0:                 #Column
                    if assigned_value in self.domains[ROW[a] + COL[col]]:
                        self.domains[ROW[a] + COL[col]].remove(assigned_value)

            if not self.apply_inequality_constraints(var):              # A domain became empty
                return False

        return True                                                     # Forward checked w/o issue    
        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
        
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
    def enforce_inequality(self, var1, var2, less):                     # Updates both variables domain to satisfy an inequality constraint

        if less:
            max_value_var2 = max(self.domains[var2], default=self.n + 1)
            new_domain_var1 = []
            for val in self.domains[var1]:
                if val < max_value_var2:
                    new_domain_var1.append(val)
            self.domains[var1] = new_domain_var1
            
            min_value_var1 = min(self.domains[var1], default=0)
            new_domain_var2 = []
            for val in self.domains[var2]:
                if val > min_value_var1:
                    new_domain_var2.append(val)
            self.domains[var2] = new_domain_var2

        else:
            min_value_var2 = min(self.domains[var2], default=0)
            new_domain_var1 = []
            for val in self.domains[var1]:
                if val > min_value_var2:
                    new_domain_var1.append(val)
            self.domains[var1] = new_domain_var1
            
            max_value_var1 = max(self.domains[var1], default=self.n + 1)
            new_domain_var2 = []
            for val in self.domains[var2]:
                if val < max_value_var1:
                    new_domain_var2.append(val)
            self.domains[var2] = new_domain_var2

        if len(self.domains[var1]) == 0 or len(self.domains[var2]) == 0:
            return False

        return True

    def apply_inequality_constraints(self, var):                        # Enforces inequality constraints between a variable and its neighbors

        row = ROW.index(var[0])
        col = COL.index(var[1])

        if row < self.n - 1:
            inequality = self.config.get(ROW[row] + '*' + COL[col], '-')
            if inequality == '<':
                if not self.enforce_inequality(var, ROW[row+1] + COL[col], less=True):
                    return False
            elif inequality == '>':
                if not self.enforce_inequality(var, ROW[row+1] + COL[col], less=False):
                    return False

        if row > 0:
            inequality = self.config.get(ROW[row-1] + '*' + COL[col], '-')
            if inequality == '<':
                if not self.enforce_inequality(ROW[row-1] + COL[col], var, less=True):
                    return False
            elif inequality == '>':
                if not self.enforce_inequality(ROW[row-1] + COL[col], var, less=False):
                    return False

        if col < self.n - 1:
            inequality = self.config.get(ROW[row] + COL[col] + '*', '-')
            if inequality == '<':
                if not self.enforce_inequality(var, ROW[row] + COL[col+1], less=True):
                    return False
            elif inequality == '>':
                if not self.enforce_inequality(var, ROW[row] + COL[col+1], less=False):
                    return False

        if col > 0:
            inequality = self.config.get(ROW[row] + COL[col-1] + '*', '-')
            if inequality == '<':
                if not self.enforce_inequality(ROW[row] + COL[col-1], var, less=True):
                    return False
            elif inequality == '>':
                if not self.enforce_inequality(ROW[row] + COL[col-1], var, less=False):
                    return False

        return True
   
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    #==========================================================#
	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
	#==========================================================#

    unassigned_vars = []
    for var in board.get_variables():
        if board.config[var] == 0:
            unassigned_vars.append(var)

    if not unassigned_vars:                                             # Board is solved
        return True

    var = min(unassigned_vars, key=lambda x: len(board.domains[x]))     # Minimum remaining value heuristic 
    original_domains = copy.deepcopy(board.domains)                     # Store a deep copy of the current board before trying a new assignment

    for value in board.domains[var]:
        board.config[var] = value                                       # Assign value

        if board.forward_checking([var]):
            if backtracking(board):
                return True
        
        board.config[var] = 0
        board.domains = copy.deepcopy(original_domains)                 # Restore state of board prior to attempted assignment

        if value in board.domains[var]:
            board.domains[var].remove(value)                            # Remove the previously tried value from the domain
    return False                                                        # No solution found, trigger backtracking
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#

    start_time = time.time()
    solved = backtracking(board)
    runtime = time.time() - start_time
    
    if not solved:
        print("No solution found for this board.")
        return None
    
    result = ''
    for row in range(board.n):
        for col in range(board.n):
            result += str(board.config[ROW[row] + COL[col]])
            if col != board.n - 1:
                result += board.config[ROW[row] + COL[col] + '*']
        if row != board.n - 1:
            for col in range(board.n):
                result += board.config[ROW[row] + '*' + COL[col]]
    
    board.config_str = result
    return board, runtime
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
