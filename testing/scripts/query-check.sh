


sleep 50

qstr='https://esgf-dev1.llnl.gov/esg-search/search/?project=cmip6test&limit=10000&format=applicatio%2fsolr%2bjson'

echo $qstr
wget -O res.json $qstr


tries=$1

sleeptime=60

for i in `seq 1 $tries` ; do

	echo Round $i

	sleep $sleeptime

	wget res-new.json $qstr 

	python ../../src/compare.py 0 res.json res-new.json

	rm res.json
	mv res-new.json res.json

done

