#!/bin/bash
python codememory.py -h
python codememory.py -l 3 -p "//" -o out.main.rs main.rs
diff out.main.rs main.rs