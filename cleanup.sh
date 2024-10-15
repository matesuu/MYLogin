if [ $# -eq 0 ]; then
    echo "missing argument: $0 <directory>"
    exit 1
fi

DIR=$1

find "$DIR" -type d -name "__pycache__" -exec rm -r {} + 

echo "deleted __pycache__. cleanup complete in $DIR"
exit 0