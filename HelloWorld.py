import xml.etree.ElementTree as ET

leftJobName = []

leftTree = ET.parse('sample1.xml')
leftRoot = leftTree.getroot()
#for job in leftRoot.findall('SMART_TABLE/JOB'):
    #print(job.attrib['JOBNAME'])

dupJob = ['J10']
for jobName in dupJob:
    xpath = './/JOB[@JOBNAME="'+jobName+'"]'
    for job in leftRoot.findall(xpath):
        # increment number
        jobNameElement = job.attrib['JOBNAME']
        print(jobNameElement)

words = ['how', 'much', 'is[br]', 'the', 'fish[br]', 'no', 'really']

words = [w.replace('[br]', '<br />') for w in words]

print(words)


