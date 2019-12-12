echo "Para criar o super usuario, adicione o parametro **createsuperuser*"
echo
python manage.py makemigrations qnow_client
python manage.py makemigrations qnow_user
python manage.py makemigrations qnow_site
python manage.py makemigrations qnow_provider
python manage.py migrate

echo "Deseja criar superuser? Digite(s/N)" 
read CONFIRMAR
if [ -z $CONFIRMAR ]; then
    echo "Tudo bem, sem criar superusuario!"
else if [ $CONFIRMAR = 'S' ] || [ $CONFIRMAR = 's' ]; then
         python manage.py createsuperuser
         echo "Pronto!"
     fi;
fi;

echo "Deseja executar o sistema? Digite(s/N)" 
read CONFIRMAR
if [ -z $CONFIRMAR ]; then
    echo "Tudo bem, sem executar!"
else if [ $CONFIRMAR = 'S' ] || [ $CONFIRMAR = 's' ]; then
        python manage.py runserver
     fi;
fi;
