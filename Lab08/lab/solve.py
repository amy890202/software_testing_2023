import angr
import claripy

main_addr = 0x4011a9
find_addr = 0x401363
avoid_addr = 0x40134d

# Define the constants from the program
EQUATION_CNT = 14
VARIABLE_CNT = 15
equations = []

with open('src/equations', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            numbers = line[1:-2].split(',')
            numbers = [int(num.strip()) for num in numbers]
            equations.append(numbers)

class ReplacementScanf(angr.SimProcedure):
    def run(self, format_string, ptr):
        # Read in data from standard input
        data = claripy.BVS('input', 8 * (ptr.size() // 8))#ptr.size() returns the size of the pointer in bits, which is divided by 8 to get the size in bytes, and then multiplied by 8 to get the size in bits.ensure that the size of the BVS object is a multiple of 8, which is required by angr.
        # Pass the data back to the program via the pointer
        self.state.memory.store(ptr, data)
        # Return the length of the input
        return len(data) // 8
# class ReplacementScanf(angr.SimProcedure):
#     def run(self, format_string, arg0):
#         # Evaluate the format string to a string value
#         scanf_format = self.state.solver.eval(format_string)

#         # If the format string is "%d"
#         if scanf_format == "%d":
#             # Create a BitVector for the input integer
#             value = claripy.BVS('value', 32)

#             # Store the BitVector at the address of the argument
#             self.state.memory.store(arg0, value)

#             # Return 1 to indicate success
#             return self.state.solver.BVV(1, self.state.arch.bits)
#         else:
#             # Return 0 to indicate failure
#             return self.state.solver.BVV(0, self.state.arch.bits)
# class ReplacementScanf(angr.SimProcedure):
#     def run(self, format_string, ptr):
#         # Handle symbolic input by marking the buffer as symbolic
#         self.state.memory.store(ptr, self.state.solver.BVS('input', 100*8))
#         # Return the number of characters read
#         return len(format_string.args) - 1
# Create the angr project
proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol("__isoc99_scanf", ReplacementScanf(), replace=True)
#proj.hook(0x500028, my_fgets(), replace=True)
# Define the address of the main function
entry_state = proj.factory.entry_state()
#entry_state = proj.factory.blank_state(addr=main_addr)

# Create a simulation manager starting from the entry state
simgr = proj.factory.simulation_manager(entry_state)

# Explore the program to reach the state immediately after the second input loop
simgr.explore(find=find_addr, avoid=avoid_addr)

# Assert that there is a solution
assert simgr.found[0].solver.satisfiable()

# Get the variable symbols
sym_vars = [entry_state.solver.BVS(f'x{i}', 32) for i in range(VARIABLE_CNT)]

# Add constraints for each equation
for i in range(EQUATION_CNT):
    eq = 0
    for j in range(VARIABLE_CNT):
        eq += sym_vars[j] * equations[i][j]
    simgr.found[0].add_constraints(eq == equations[i][VARIABLE_CNT])#找出的sym_vars套進方程式計算出的答案(eq)，如果不等於第i個方程式的答案(equations[i][VARIABLE_CNT])，就不是正確答案

# Solve the constraints and print the result
for i in range(VARIABLE_CNT):
    print(f'x{i} = {simgr.found[0].solver.eval(sym_vars[i])}')#有一個名為x的符號變數，您可以使用以下命令獲取x的具體值：simgr.found[0].solver.eval(x)。

with open('solve_input', 'w') as f:
    for i in range(VARIABLE_CNT):
        f.write(f'{simgr.found[0].solver.eval(sym_vars[i])}\n')


# Create an instance of the Project class: proj = angr.Project('/path/to/program')
# Define the address of the main function: entry_state = proj.factory.entry_state()
# Create a SimulationManager object and configure it to start from entry_state: simgr = proj.factory.simulation_manager(entry_state)
# Explore the program to reach the state immediately after the second input loop (where all the values of the variables are known): simgr.explore(find=0x401363)
# Assert that there is a solution by checking that the state where the solver function (0x40134d) is reached is satisfiable: assert simgr.found[0].solver.satisfiable()
# Get the solution by printing the values of the variables: for i in range(VARIABLE_CNT): print(simgr.found[0].solver.eval(sym_vars[i]))
