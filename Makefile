crf_%.txt:
	python2.7 generate_crf_input.py

chars_by_count.txt: crf_train.txt crf_test.txt
	perl -C -pe 's/[[:ascii:]]//g;s/([^\p{IsLatin}])/\1\n/g;' crf_train.txt crf_test.txt | sort | uniq -c | sort -rn >  $@

nonce.txt: chars_by_count.txt
	grep '^ *1 ' chars_by_count.txt | awk '{print $2}' > $0
