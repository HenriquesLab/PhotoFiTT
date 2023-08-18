#!/bin/sh
nohup python3 pytorch-CycleGAN-and-pix2pix/train.py --dataroot "/home/ocb/Documents/EGM/PHX/PIX2PIX-MODELS/working_dir/ph_membrane_contrast-stretching_280723/AB" --name "ph_membrane_contrast-stretching_280723" --model pix2pix --batch_size 10 --preprocess scale_width_and_crop --load_size 1200 --crop_size 512 --checkpoints_dir "/home/ocb/Documents/EGM/PHX/PIX2PIX-MODELS" --no_html --n_epochs 1000 --n_epochs_decay 150 --lr 0.0005 --display_id 0 --save_epoch_freq 5 --input_nc "1" --output_nc "1" --dataset_mode "aligned" &> bash_training_logs &



