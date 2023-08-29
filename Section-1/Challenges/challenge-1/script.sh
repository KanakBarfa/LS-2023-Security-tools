#!/bin/bash
l=0
# Specify the path to your file
file_path="./chall1.7z"

# Extract function for 7zip files
extract_7zip() {
  local file=$1
  local password=$2
  7z x "$file" -p"$password" -oextracted > /dev/null 2>&1
  return $?
}

# Extract function for zip files
extract_zip() {
  local file=$1
  local password=$2
  unzip -P "$password" "$file" -d extracted > /dev/null 2>&1
  return $?
}

# Recursive function to handle multiple levels of compressions
extract_recursive() {
  local file=$1
  local password=$2

  if [[ "$file" == *".7z" ]]; then
    extract_7zip "$file" "$password"
    return $?
  elif [[ "$file" == *".zip" ]]; then
    extract_zip "$file" "$password"
    return $?
  fi
}

# Clean up previously extracted files
rm -rf extracted

# Start the extraction process
extract_recursive "$file_path" ""
file_path="./extracted/files.zip"
# Find the latest enc_pass file in extracted folder
latest_enc_pass_file=$(find extracted -type f -name "enc_pass" | sort -r | head -n 1)

while [[ -f "$latest_enc_pass_file" ]]; do

  echo "Found latest enc_pass file: $latest_enc_pass_file"

  # Read the encoded password from the enc_pass file
  encoded_password=$(cat "$latest_enc_pass_file")

  # Array of decoding methods to try
  decoding_methods=("none" "base64" "base32" "hex")

  # Loop through each decoding method and try to decode the password
  for method in "${decoding_methods[@]}"; do
    case "$method" in
      "none")
        decoded_password=$encoded_password
        ;;
      "base64")
        decoded_password=$(echo "$encoded_password" | base64)
	decoded_password=${decoded_password%?}
	decoded_password="${decoded_password}="
        ;;
      "base32")
        decoded_password=$(echo "$encoded_password" | base32 | sed 's/BI======//g')
        ;;
      "hex")
        decoded_password=$(echo "$encoded_password" | xxd -p | sed 's/0a//g')
        ;;
    esac

    # Start the extraction process if password decoding is successful
    if [[ -n "$decoded_password" ]]; then
      echo "Trying decoding method: $method Password: $decoded_password File: $file_path"
      extract_recursive "$file_path" "$decoded_password"
      exit_code=$?

      if [[ $exit_code -eq 0 ]]; then
        # Extraction successful, update the latest enc_pass file
	echo -e "\e[32m Success for $decoded_password \e[0m"
	l=$l+1
	echo $l
	echo "Now removing $file_path and $latest_enc_pass_file"
	if [[ -f "$file_path" ]]; then
	rm -f "$file_path"
	rm -f "$latest_enc_pass_file"
	fi
	# Get the file names in the current folder
	files=$(ls ./extracted/)

	# Initialize the file_path variable
	file_path=""
	latest_enc_pass_file=""
	# Loop through each file and check its type
	for file in $files; do
  		file_type=$(file -b "./extracted/$file")

  	# Check if the file type is 7z or zip
  		if [[ "$file_type" == *"7-zip archive"* || "$file_type" == *"Zip archive data"* ]]; then
    			file_path="./extracted/$file"
  		fi
		if [[ "$file_type" == *"ASCII text"* || "$file_type" == *"X1"* ]]; then
    			latest_enc_pass_file="./extracted/$file"
  		fi
	done

	# Check if a file was found
	if [[ -n "$file_path" ]]; then
  		echo "File found: $file_path Password file: $latest_enc_pass_file"
	else
	  echo "No 7z or zip file found in the current folder."
	fi
        break
      else
        echo "Incorrect password for decoding method: $method"
      fi
    fi
  done

  # Clean up extracted files if extraction was unsuccessful
  if [[ ! -f "$latest_enc_pass_file" ]]; then
    echo "Extraction unsuccessful"
	echo $l
    break
  fi
done

if [[ -d "extracted" ]]; then
  echo "Final data extracted from: $file_path"
  # Further processing of the final extracted file can be added here
else
  echo "Latest enc_pass file not found."
fi
