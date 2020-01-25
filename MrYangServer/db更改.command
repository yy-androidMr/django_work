local="$0"
#echo $local
name=${local##*/}
manage=${local/$name/manage.py}

python3 $manage makemigrations
python3 $manage migrate