echo 
echo "=========== Acessando PostgreSQL no Heroku ============"
echo "PassWord: fad29688a28db66d902856fba2688758cec82f563e6c03292de22be94f270e43"
echo 
heroku run psql -p 5432 -h ec2-54-235-246-201.compute-1.amazonaws.com -U rcvyijjkpymkue d5hoklb761lftk --app quotation-now