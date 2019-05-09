import vf_energy
import vf_input


input_data = vf_input.inputContainer()

costs = vf_energy.energy(input_data)

print("GOT costs ", costs)