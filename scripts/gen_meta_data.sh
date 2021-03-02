#!/usr/bin/env bash
# 数据预处理的入口
echo usage: pass dataset list as param, split with space
echo eg: source gen_mate_data.sh

dataset_lst=(smp)

# ======= size setting ======
# 一个episode中，每个意图包含多少个support样本（比如domain下面有3个意图就是9个样本）
support_shots_lst=(3)
#support_shots_lst=(5)
query_shot=4

# 控制一个epoch里面有多少个episode
episode_num=50
way=-1

remove_rate=80


# ====== general setting =====
seed_lst=(0)

# TODO 任务切换
<<<<<<< HEAD
#task=sc
task=sl
=======
task=sc
#task=sl
>>>>>>> 333ef88eabf7831d715f91cb4c1cbed180b5c481

#dup_query=--dup_query  # dup_query set empty to not allow duplication between query and support
dup_query=

allow_override=--allow_override

check=--check

# ====== train & test setting ======
split_basis=domain
# split_basis=sent_label

#eval_confif_id_lst=(1)  # for snips
#eval_config_id_lst=(0 1 2 3 4 5)  # for toursg
label_type_lst=(attribute)

#use_fix_support=
# use_fix_support=--use_fix_support

# ======= default path (for quick distribution) ==========
input_dir=../FewJoint/SMP_Final_Origin2_3/
output_dir=../FewJoint/SMP_Final_Origin2_3/

echo \[START\] set jobs on dataset \[ ${dataset_lst[@]} \]
# === Loop for all case and run ===
for seed in ${seed_lst[@]}
do
  for dataset in ${dataset_lst[@]}
  do
    for support_shots in ${support_shots_lst[@]}
    do
      echo \[CLI\] generate with \[ ${use_fix_support} \]
      input_path=${input_dir}
      mark=try

      export OMP_NUM_THREADS=2  # threads num for each task
      python3 ./other_tool/meta_dataset_generator/generate_meta_dataset.py \
        --input_path ${input_path} \
        --output_dir ${output_dir} \
        --dataset ${dataset} \
        --episode_num ${episode_num} \
        --support_shots ${support_shots} \
        --query_shot ${query_shot} \
        --way ${way} \
        --task ${task} \
        --seed ${seed} \
        --split_basis ${split_basis} \
        --remove_rate ${remove_rate} \
        --mark ${mark} ${dup_query} ${allow_override} ${check} > ${output_dir}${task}.spt_s_${support_shots}.q_s_${query_shot}.ep_${episode_num}.log
    done
  done
done





