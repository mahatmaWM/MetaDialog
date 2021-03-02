#!/usr/bin/env bash
# 跑序列标注的入口，在MetaDialog目录下创建log目录 source scripts/run_exp.sh 0
echo usage: pass gpu id list as param, split with ,
echo eg: source scripts/run_exp.sh 0

# TODO 使用哪些GPU 任务切换
gpu_list=$1
#task=sc
task=sl
<<<<<<< HEAD
epoch=3
=======
epoch=1
>>>>>>> 333ef88eabf7831d715f91cb4c1cbed180b5c481

# ====== 尝试的各种参数组合 ======
dataset_lst=(smp)
seed_lst=(0)
#seed_lst=(6150 6151 6152)
support_shots_lst=(3)
train_batch_size_lst=(4)
#train_batch_size_lst=(4 8)
decay_lr_lst=(0.5)
#decay_lr_lst=(-1)
fix_embd_epoch_lst=(-1)
#fix_embd_epoch_lst=(1 2)
lr_lst=(0.00001)
#lr_lst=(0.000001 0.000005 0.00005)
upper_lr_lst=(0.001)
#upper_lr_lst=(0.001 0.1)
ems_scale_rate_lst=(0.01)
#ems_scale_rate_lst=(0.01 0.02 0.05 0.005)
emission_lst=(proto_with_label)
#emission_lst=(mnet proto tapnet)
ple_scale_r_lst=(0.5)

# ====== 其他参数 opt ======
clip_grad=5
similarity=dot
embedder=bert
emission_normalizer=norm
emission_scaler=learn
ple_normalizer=none
ple_scaler=fix
label_reps=sep
query_shot=4
episode=50
cross_data_id=0  # for smp
test_batch_size=2
grad_acc=4

# ======= default path (for quick distribution) ==========
# bert base path
pretrained_model_path=/data/chrism/pre_embeddings/pytorch_bert/bert-base-chinese
pretrained_vocab_path=/data/chrism/pre_embeddings/pytorch_bert/bert-base-chinese/vocab.txt
# electra small path
#pretrained_model_path=/users4/yklai/corpus/electra/chinese_electra_small_discriminator
#pretrained_vocab_path=/users4/yklai/corpus/electra/chinese_electra_small_discriminator

# --saved_model_path ${data_dir}${model_name}.DATA.${file_mark}/model.pl \
# data path
base_data_dir=../FewJoint/SMP_Final_Origin2_3/
#base_data_dir=/data/shiyuanyang/MetaDialog/lqd_data_100/


echo [START] set jobs on dataset [ ${dataset_lst[@]} ] on gpu [ ${gpu_list} ]
# === 类似网格搜索，尝试各种参数对应的模型效果 ===
for seed in ${seed_lst[@]}
do
    for dataset in ${dataset_lst[@]}
    do
        for support_shots in ${support_shots_lst[@]}
        do
            for train_batch_size in ${train_batch_size_lst[@]}
            do
                for decay_lr in ${decay_lr_lst[@]}
                do
                    for fix_embd_epoch in ${fix_embd_epoch_lst[@]}
                    do
                        for lr in ${lr_lst[@]}
                        do
                            for upper_lr in ${upper_lr_lst[@]}
                            do
                                for ems_scale_r in ${ems_scale_rate_lst[@]}
                                do
                                    for emission in ${emission_lst[@]}
                                    do
                                        for ple_scale_r in ${ple_scale_r_lst[@]}
                                        do
                                            # model names
                                            model_name=${task}.ga_${grad_acc}.ple_${ple_scale_r}.tbs_${train_batch_size}.sim_${similarity}.ems_${emission}_${emission_normalizer}
                                            # TODO cross_data_id
                                            # data_dir=${base_data_dir}${dataset}.${cross_data_id}.spt_s_${support_shots}.q_s_${query_shot}.ep_${episode}/
                                            data_dir=${base_data_dir}smp.try.spt_s_3.q_s_4.ep_50.lt_both.ci_0/
                                            file_mark=${dataset}.shots_${support_shots}.cross_id_${cross_data_id}.m_seed_${seed}
                                            train_file_name=train.json
                                            dev_file_name=dev.json
                                            test_file_name=test.json
                                            echo Model: ${model_name}
                                            echo Task:  ${file_mark}
                                            echo [CLI]
                                            export OMP_NUM_THREADS=2  # threads num for each task
                                            CUDA_VISIBLE_DEVICES=${gpu_list} python ../main.py --task ${task} \
                                                --seed ${seed} \
                                                --train_path ${data_dir}${train_file_name} \
                                                --dev_path ${data_dir}${dev_file_name} \
                                                --test_path ${data_dir}${test_file_name} \
                                                --output_dir ${data_dir}${model_name}.DATA.${file_mark} \
                                                --bert_path ${pretrained_model_path} \
                                                --bert_vocab ${pretrained_vocab_path} \
                                                --train_batch_size ${train_batch_size} \
                                                --cpt_per_epoch 4 \
                                                --gradient_accumulation_steps ${grad_acc} \
                                                --num_train_epochs ${epoch} \
                                                --learning_rate ${lr} \
                                                --decay_lr ${decay_lr} \
                                                --upper_lr ${upper_lr} \
                                                --clip_grad ${clip_grad} \
                                                --fix_embed_epoch ${fix_embd_epoch} \
                                                --test_batch_size ${test_batch_size} \
                                                --context_emb ${embedder} \
                                                --label_reps ${label_reps} \
                                                --emission ${emission} \
                                                --similarity ${similarity} \
                                                --emission_normalizer ${emission_normalizer} \
                                                --emission_scaler ${emission_scaler} \
                                                --ems_scale_r ${ems_scale_r} \
                                                --ple_normalizer ${ple_normalizer} \
                                                --ple_scaler ${ple_scaler} \
                                                --ple_scale_r ${ple_scale_r} \
                                                --transition learn > ../log/${model_name}.DATA.${file_mark}.log
                                        done
                                    done
                                done
                            done
                        done
                    done
                done
            done
        done
    done
done

echo [FINISH] set jobs on dataset [ ${dataset_lst[@]} ] on gpu [ ${gpu_list} ]
