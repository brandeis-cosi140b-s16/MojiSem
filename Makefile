crf_%.txt:
	python2.7 generate_crf_input.py

chars_by_count.txt: crf_train.txt crf_test.txt
	perl -C -pe 's/[[:ascii:]]//g;s/([^\p{IsLatin}])/\1\n/g;' crf_train.txt crf_test.txt | sort | uniq -c | sort -rn >  $@

nonce.txt: chars_by_count.txt
	grep '^ *1 ' chars_by_count.txt | awk '{print $2}' > $@

MojiSem.model: crf_train.txt crf_test.txt
	crfsuite learn -aap -m $@ crf_train.txt

eval: crf_train.txt crf_test.txt
	crfsuite learn -e2 -aap crf_train.txt crf_test.txt

compare: MojiSem.model
	crfsuite tag -r -m MojiSem.model crf_test.txt > crf_tagged.txt
	paste crf_tagged.txt crf_test.txt

mistagged_words:
	paste crf_tagged.txt crf_test.txt | grep word | egrep 'mm|content'

clean:
	rm crf_train.txt crf_test.txt MojiSem.model


