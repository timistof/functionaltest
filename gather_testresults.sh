#!/bin/bash

timestamp() { 
  date -Iseconds 
}

check() {
	if (( $? != "0" )); then
		echo "Zipping testresults failed!";
		exit 1;
	fi
}

input="testresults"
output="../testresults-$(timestamp).zip"
echo "creating $output..."
zip -m $output $input > /dev/null
check
zip -T $output
check
rm -rf "$input"
mkdir $input
