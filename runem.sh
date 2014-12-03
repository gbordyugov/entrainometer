#!/bin/bash

function runem {
  data_file=$1
  output_dir=$2

  ./em.py $data_file $output_dir
  cd $output_dir
  ./nup.sh
  cd -
}

runem data/t24/ute-T24.txt        data/t24/output/figures
runem data/t22-26/ute-T22-T26.txt data/t22-26/output/figures
