dt=`date +%s`
mkdir old-res/res-$dt
mv *.log *.json *.old old-res/res-$dt


#sleep 50

qstr='https://esgf-dev1.llnl.gov/esg-search/search/?project=cmip6test&limit=10000&format=application%2fsolr%2bjson'

echo $qstr
time wget -O res.json $qstr

tries=$1

sleeptime=$2  # TODO - refactor the time and tries as parameters

for i in `seq 1 $tries` ; do

	echo Round $i

	# may need to adjust if query latency impacts time
	sleep $sleeptime

	wget -O res-new.json $qstr 

	python ../../src/compare.py $sleeptime res.json res-new.json

	mv res.json res.json.$i.old
	mv res-new.json res.json

done
