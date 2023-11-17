pip install --no-cache-dir --user -r requirements.txt
export PATH=$PATH:$HOME/.local/bin
cd /app 

pip show django
pip list 

project_name="applicationrunserver"

if [ ! -d "$project_name" ]; then
    django-admin startproject "$project_name"
else
    echo "Project folder already exists. Skipping django-admin startproject."
fi

chmod -R 777 /app

cd applicationrunserver

python manage.py runserver 0.0.0.0:8000










