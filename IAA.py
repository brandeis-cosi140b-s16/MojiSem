"""
@author: Noa Naaman

Uses nltk.metrics.agreement to calculate cross tag agreement using the multi_kappa() method:
Davies and Fleiss 1982: Averages over observed and expected agreements for each coder pair.

Requires Python 3

"""


from xml.etree.ElementTree import ElementTree
import nltk
from nltk.metrics.agreement import AnnotationTask


def process_xml(path):
    f = nltk.data.find(path)
    xml = ElementTree().parse(f)
    tags = []

    for tag in xml[1]:
        if tag.tag == 'mm':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'mm',text)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'content':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'content',text)
            tags.append(a)

    for tag in xml[1]:
        if tag.tag == 'func':
            spans = tag.get('spans')
            s = spans.split('~')
            n1 = int(s[0])
            n2 = int(s[1])
            text = tag.get('text')
            a = (n1,n2,'func',text)
            tags.append(a)

    tags = sorted(tags)

    raw = xml[0].text
    return raw, tags

def tags_to_task(tags, annotator):
	a_tags = []
	for t in tags:
		a = (annotator, t[0],t[2])
		a_tags.append(a)
	return a_tags

def combine_data(tags_list):
    res = []
    anno_num = len(tags_list)
    for l in tags_list:
        res.extend(l)

    spans_to_remove = {}
    for tup in res:
        if tup[1] in spans_to_remove:
            a = spans_to_remove[tup[1]]
            a.append(tup[0])
            spans_to_remove[tup[1]] = a
        else:
            spans_to_remove[tup[1]] = [tup[0]]

    spans_list = []
    for span in spans_to_remove:
        if len(spans_to_remove[span]) < anno_num:
            spans_list.append(span)

    print('Number of spans removed from task: ' + str(len(spans_list)))
    tags_list = [tup for tup in res if tup[1] not in spans_list]
    return tags_list



#week1
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week1\\a.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week1\\b.xml')
c,c_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week1\\c.xml')
d,d_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week1\\d.xml')
tags_list = [tags_to_task(a_tags, 'a'), tags_to_task(b_tags, 'b'), tags_to_task(c_tags, 'c'), tags_to_task(d_tags, 'd')]
t_l = combine_data(tags_list)
week1 = AnnotationTask(data=t_l)
print('Week 1 cross tags agreement:')
print(week1.multi_kappa())

#week2
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week2\\a.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week2\\b.xml')
c,c_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week2\\c.xml')
d,d_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week2\\d.xml')
tags_list = [tags_to_task(a_tags, 'a'), tags_to_task(b_tags, 'b'), tags_to_task(c_tags, 'c'), tags_to_task(d_tags, 'd')]
t_l = combine_data(tags_list)
week2 = AnnotationTask(data=t_l)
print('Week 2 cross tags agreement:')
print(week2.multi_kappa())

#week3_A
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week3\\A\\A1.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week3\\A\\A2.xml')
tags_list = [tags_to_task(a_tags, 'A1'), tags_to_task(b_tags, 'A2')]
t_l = combine_data(tags_list)
week3A = AnnotationTask(data=t_l)
print('Week 3_A cross tags agreement:')
print(week3A.multi_kappa())

#week3_J
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week3\\J\\J1.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week3\\J\\J2.xml')
tags_list = [tags_to_task(a_tags, 'J1'), tags_to_task(b_tags, 'J2')]
t_l = combine_data(tags_list)
week3J = AnnotationTask(data=t_l)
print('Week 3_J cross tags agreement:')
print(week3J.multi_kappa())

#week4_A
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week4\\A\\A1.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week4\\A\\A2.xml')
tags_list = [tags_to_task(a_tags, 'A1'), tags_to_task(b_tags, 'A2')]
t_l = combine_data(tags_list)
week4A = AnnotationTask(data=t_l)
print('Week 4_A cross tags agreement:')
print(week4A.multi_kappa())

#week4_J
a,a_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week4\\J\\J1.xml')
b,b_tags = process_xml('C:\\Brandeis\\Annotations\\annotated_tweets\\week4\\J\\J2.xml')
tags_list = [tags_to_task(a_tags, 'J1'), tags_to_task(b_tags, 'J2')]
t_l = combine_data(tags_list)
week4J = AnnotationTask(data=t_l)
print('Week 4_J cross tags agreement:')
print(week4J.multi_kappa())




    
    
    

