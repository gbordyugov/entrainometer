#!/bin/sh

./em.py data/t24/ute-T24.txt tmp
cd tmp
./nup.sh
cd -
