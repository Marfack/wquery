#! /bin/bash
find . "(" -name "*.py" -or -name "*.json" ")" -print | xargs wc -l