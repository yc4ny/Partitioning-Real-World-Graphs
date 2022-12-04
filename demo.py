import argparse 
import os
import subprocess

def getGraphName(input_directory):
    input_dir = args.input 
    file_path = input_dir.split('/')
    filename = file_path[len(file_path)-1]
    filename = filename.replace('.csv', '')
    return filename

if __name__ == "__main__":
    # Parse command line arguments  
    parser = argparse.ArgumentParser(description = "Age Classification")
    parser.add_argument('--input', type = str, default = 'datasets/facebook_clean_data/artist_edges.csv', help = 'output from community detection')
    args = parser.parse_args()

    # Get the graph name for future saving purposes
    filename = getGraphName(args.input) #artist_edges

    # Run the full pipeline
    # Step 1: Label Propagation
    subprocess.run(["python", "label_propagation/label_propagation.py", "--input", args.input, "--output", "outputs/output_LP/" + filename + ".json",]) 
    # Step 1-2: Preprocessing output of Label Propagation to be ready for KL
    subprocess.run(["python", "preprocess/preprocess_LP.py", "--input", "outputs/output_LP/" + filename + ".json", "--output", "outputs/output_preprocess/processed_" + filename + ".txt", "--original_edges", args.input])
    # Step 2: Run KL graph partitioning algorithm 
    subprocess.run(["python", "baseline/kl_partitioning/kl.py", "--input", "outputs/output_preprocess/processed_" + filename + ".txt", "--output", "outputs/output_KL/partitioned_" + filename + ".txt",])
