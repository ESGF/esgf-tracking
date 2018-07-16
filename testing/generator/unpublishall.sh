
while [ True ] ; do

     esglist_datasets --select version_name --no-header cmip6test > pub-list

     count=`cat pub-list | wc -l`

     if [ $count == 0 ] ; then

     	echo "No more datasets"
	exit
     fi	

     sed s/\.v2018/#2018/g pub-list > pub-list-2
     esgunpublish --use-list pub-list-2 --skip-thredds --delete --project cmip6test
     esgunpublish --use-list pub-list --skip-index --database-delete --project cmip6test

done

