from utils.display import build_mosaics


roundness = [0.5, 0.85, 0.9, 0.95, 0.97]
path = "/Users/esti/Documents/PHX/mitosis_mediated_data/results/2021-12-20/"
path2original = "/Users/esti/Documents/PHX/mitosis_mediated_data/2021-12-20/"

for r in roundness:
    output_path = "/Users/esti/Documents/PHX/mitosis_mediated_data/mosaics_roundness_{}".format(r)
    build_mosaics(path, path2original, output_path, min_roundness = r)