#!/bin/sh
nohup python3 pytorch-CycleGAN-and-pix2pix/train.py --dataroot "/home/ocb/HardDrive_4TB/EGM/MULTICHANNEL/CYCLEGAN/MODELS/working_dir/choph_membrane_cycleGAN_28092023" --input_nc "1" --output_nc "1" --name "choph_membrane_cycleGAN_28092023" --model cycle_gan --batch_size 2 --preprocess scale_width_and_crop --load_size 1200 --crop_size 512 --checkpoints_dir "/home/ocb/HardDrive_4TB/EGM/MULTICHANNEL/CYCLEGAN/MODELS"  --no_html --n_epochs 500 --n_epochs_decay 500 --lr 0.0001 --display_id 0 --save_epoch_freq 10 &> bash_training_logs &







