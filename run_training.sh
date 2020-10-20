$BASE=/storage/slurm/liuyang/git-repos/detectron2

python tools/train_net.py \
  --config-file configs/COCO-InstanceSegmentation/binary_mask_rcnn_X_101_32x8d_FPN_3x.yaml \
  --num-gpus 1