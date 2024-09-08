echo "Preparing data ..."
./indicvoicesR_gujratidata.sh dataset

echo "Download checkpoint ..."
python download_checkpoint.py --output_path checkpoints/

echo "Extending vocab ..."
python extend_vocab_config.py --output_path=checkpoints/ --metadata_path dataset/metadata_train.csv --language gu --extended_vocab_size 150

echo "Finetuning DVAE ..."
python train_gpt_xtts.py \
--output_path=checkpoints/ \
--train_csv_path=dataset/metadata_train.csv \
--eval_csv_path=dataset/metadata_eval.csv \
--language="gu" \
--num_epochs=100 \
--batch_size=512 \
--lr=5e-5

echo "Finetuning GPT ..."
python train_gpt_xtts.py \
--output_path=checkpoints/ \
--train_csv_path=dataset/metadata_train.csv \
--eval_csv_path=dataset/metadata_eval.csv \
--language="gu" \
--num_epochs=500 \
--batch_size=8 \
--grad_acumm=2 \
--max_text_length=300 \
--max_audio_length=255995 \
--weight_decay=1e-2 \
--lr=5e-5 \
--save_step=100
