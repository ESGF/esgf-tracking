
  while [ True ] ;
do

     esglist_datasets --select version_name --no-header > pub-list

     count=`cat pub-list | wc -l`

     if [ $count == 0 ] ; then

     	echo "No more datasets
	exit
	fi	


done

  225  esglist_datasets --select version_name --no-header > pub-list
  226  less pub-list 
  227  esglist_datasets --select version_name --no-header cmip6test > pub-list
  228  less pub-list 
  229  sed s/\.v2018/#2018/g pub-list > pub-list-2
  230  less pub-list2
  231  less pub-list-2 
  232  esgunpublish --use-list pub-list-2 --skip-thredds --delete --project cmip6test
  233  esgunpublish --use-list pub-list --skip-index --database-delete --project cmip6test
  234  esglist_datasets --select version_name --no-header cmip6test > pub-list-3
  235  less pub-list-3 
  236  sed s/\.v2018/#2018/g pub-list-3 > pub-list-4
  237  esgunpublish --use-list pub-list-4 --skip-thredds --delete --project cmip6test
  238  emacs pub-list-4 
  239  esgunpublish --use-list pub-list-3 --skip-index --database-delete --project cmip6test
  240  emacs pub-list-3 
  241  esgunpublish --use-list pub-list-4 --skip-thredds --delete --project cmip6test
  242  esgunpublish --use-list pub-list-3 --skip-index --database-delete --project cmip6test
  243  history | tail -n 30 > commands
