	#!/bin/bash

# Function to crawl a webpage and follow links recursively
crawl_webpage() {
  local url=$1
  local output_dir=$2

  # Download the webpage using wget
  wget -q -P "$output_dir" "$url"

  # Extract all the links from the downloaded webpage matching the desired pattern
  full_url=$(grep -o 'www.cse.iitb.ac.in/[^"]*.html' "$output_dir/$(basename "$url")")
``echo "$full_url"
    # Crawl the linked webpage recursively
  crawl_webpage "$full_url" "$output_dir"
}
# Main script starts here

# Specify the starting URL and output directory
start_url="https://www.cse.iitb.ac.in/~akshatka/Zxfz2lrFOWFygrTuloST.html"
output_directory="webpages"

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Crawl the starting URL and follow links recursively
crawl_webpage "$start_url" "$output_directory"

echo "Done"
