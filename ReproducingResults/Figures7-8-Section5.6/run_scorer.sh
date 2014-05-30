for carrier in "att" "verizon3g" "verizon4g" "tmobile"
do
    for f in "ctcp-"$carrier"-sep17" "cubic-codel-"$carrier"-sep17" "hangouts-"$carrier"-sep17" "skype-"$carrier"-sep17" "sproutbt2-ewma-"$carrier"-sep17" "cubic-"$carrier"-sep17" "facetime-"$carrier"-sep17" "libutp-"$carrier"-sep17" "sproutbt2-"$carrier"-sep17" "vegas-"$carrier"-sep17"
    do 
	echo $f >> $carrier"_output"
	echo "uplink:" >> $carrier"_output"
	cat $f | ./scorer uplink | ./quantiles >> $carrier"_output"
	echo "downlink:" >> $carrier"_output"
	cat $f | ./scorer downlink | ./quantiles >> $carrier"_output"
    done
done

