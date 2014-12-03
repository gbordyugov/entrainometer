#!/bin/bash

function runbb {
  data_file=$1
  output_dir=$2

  ./bluebars.py $data_file $output_dir
  cd $output_dir
  ./nup.sh
  cd -
}

runbb data/t24/ute-T24.txt        data/t24/output/bluebars
runbb data/t22-26/ute-T22-T26.txt data/t22-26/output/bluebars
