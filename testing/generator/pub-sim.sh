waittime=60
initial_pub_count=$2  # set this to several query periods before updates and retractions can begin

#path_prefix=$1
flst=$1

i=0

for dn in `python rnd_list.py $flst` ; do

    
#    dn=`dirname $fn`
   
    starttime=`date +%s`

#    if [ $i -lt $initial_pub_count ]  ; then
    echo Processing $dn

    esgmapfile --project cmip6test --no-checksum $dn
    esgpublish --project cmip6test --map mapfiles
    esgpublish --project cmip6test --map mapfiles --noscan --thredds
    esgpublish --project cmip6test --map mapfiles --noscan --publish

    endtime=`date +%s`
    gentime=$(( $waittime - $(( $endtime - $starttime  )) ))


    rm -rf mapfiles

    echo sleeping $gentime
    sleep $gentime
    
    i=$(( $i + 1 ))

    if [ $i == $initial_pub_count ] ; then
	echo "count reached"
	exit
    fi
done
