import os

# Define the input and output directories
input_attack_dir = "cicflowmeter/attack_input"
output_attack_dir = "cicflowmeter/attack_output_ordered"

input_benign_dir = "cicflowmeter/benign_input"
output_benign_dir = "cicflowmeter/benign_output_ordered"

print("Começando reordenação dos ataques")

# Iterate over each file in the input directory
for filename in os.listdir(input_attack_dir):
    if filename.endswith(".pcap"):
        input_path = os.path.join(input_attack_dir, filename)
        output_path = os.path.join(output_attack_dir, filename.replace(".pcap", "-reordered.pcap"))
        
        # Execute the reordercap command for each file
        os.system(f"reordercap {input_path} {output_path}")
        print(f"Reordered {filename} and saved as {output_path}")

        # Delete the original pcap file
        os.remove(input_path)
        print(f"Deleted {input_path}")

print("Começando reordenação dos benignos")

for filename in os.listdir(input_benign_dir):
    if filename.endswith(".pcap"):
        input_path = os.path.join(input_benign_dir, filename)
        output_path = os.path.join(output_benign_dir, filename.replace(".pcap", "-reordered.pcap"))
        
        # Execute the reordercap command for each file
        os.system(f"reordercap {input_path} {output_path}")
        print(f"Reordered {filename} and saved as {output_path}")

        # Delete the original pcap file
        os.remove(input_path)
        print(f"Deleted {input_path}")

print("All pcap files reordered and original files deleted.")
