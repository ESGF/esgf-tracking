waittime=20
initial_pub_count=8  # set this to several query periods before updates and retractions can begin

path_prefix=$1
flst=$2

i=0

for fn in `cat $flst | python rnd_list.py` ; do

    
    dn=`dirname $fn`
   
    starttime=`date +%s`

#    if [ $i -lt $initial_pub_count ]  ; then
    echo Processing $dn

    esgmapfile --project cmip6test --no-checksum $dn
    esgpublish --project cmip6test --map mapfiles
    esgpublish --project cmip6test --map mapfiles --noscan --thredds
    esgpublish --project cmip6test --map mapfiles --noscan --publish

    endtime=`date +%s`
    gentime=$(( $waittime - $(( $endtime - $starttime  )) ))

    sleep $gentime

    rm -rf mapfiles
    
    i=$(( $i + 1 ))
done
