if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <save_path>"
    exit 1
fi

SAVE_PATH=$1
url="https://indic-tts-public.objectstore.e2enetworks.net/data/indicvoices_r/Gujarati.tar"

filename=$(basename "$url")
filepath="$SAVE_PATH/$filename"

echo "Downloading Gujrati dataset"
curl -o "$filepath" "$url"

echo "Extracting $filename in $SAVE_PATH..."
tar -xf "$filepath" -C "$SAVE_PATH"

echo "Deleting $filename..."
rm "$filepath"

data_folder="$SAVE_PATH/Gujarati"
echo "Making XTTS compatible data..."
python3 make_xtts_compitably_data.py "$data_folder" 0.8
echo "Cleaning up..."
rm -rf "$data_folder"