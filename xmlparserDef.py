import xml.etree.ElementTree as ET
import xml.dom.minidom as XD
import re
import sys

from shutil import copyfile

'''
#first param: dev path
#second param: prod path
#third param: destination path
#fourth path: jobs to be merged
#Sample Command: python xmlparser.py C:/Users/rgu107/Desktop/comp/sample1.xml C:/Users/rgu107/Desktop/comp/sample2.xml C:/Users/rgu107/Desktop/comp/output1.xml J10,J11
'''

# Ask for jobs to be merged
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

if len(sys.argv) == 1:
    input_devPath = input("Enter dev copy path: ")
    input_prodPath = input("Enter Prod copy path: ")
    input_destinationPath = input("Enter destination path:")
    input_mergeJob = input("Enter jobs to be merged (comma seprated): ")
    print("Jobs to be merged " + input_mergeJob)
    input_mergelist = input_mergeJob.split(',')
elif len(sys.argv) ==5:
    input_devPath = sys.argv[1]
    input_prodPath = sys.argv[2]
    input_destinationPath = sys.argv[3]
    input_mergeJob = sys.argv[4]
    print("Jobs to be merged " + input_mergeJob)
    input_mergelist = input_mergeJob.split(',')

# parse left file
leftJobName = []

leftTree = ET.parse(input_devPath)
leftRoot = leftTree.getroot()
for job in leftRoot.findall('SMART_TABLE/JOB'):
    leftJobName.append(job.attrib['JOBNAME'])

#print('-----leftjobanme-----', leftJobName)

# parse right file
rightTree = ET.parse(input_prodPath)
rightRoot = rightTree.getroot()
rightJobName = []
for job in rightRoot.findall('SMART_TABLE/JOB'):
    rightJobName.append(job.attrib['JOBNAME'])

#print('--------rightjobname----', rightJobName)

# print ("dup: ",set(input_mergelist) & set(rightJobName))
# print("new: ", set(input_mergelist) - set(rightJobName))
# print("all: ", list(set(input_mergelist+rightJobName)))

# get duplicate jobs
dupJob = set(input_mergelist) & set(rightJobName)
# get new jobs
newJob = set(input_mergelist) - set(rightJobName)
# get all jobs from both files
allProcessedJobs = list(set(input_mergelist + rightJobName))

# create mapping dict
old_new_dict = {}

# process new jobs
insertion_point = rightTree.findall("./SMART_TABLE")[-1]

for jobName in newJob:
    xpath = './/JOB[@JOBNAME="' + jobName + '"]'
    for job in leftRoot.findall(xpath):
        insertion_point.append(job)
        old_new_dict[jobName] = jobName

# find max of all jobs for creating new job numbers
allNumbersJob = []

for job in allProcessedJobs:
    allNumbersJob += re.findall('\d+', job)

allNumbersJob = list(map(int, allNumbersJob))
currentMaxNumber = max(allNumbersJob)

# process duplicate jobs
for jobName in dupJob:
    xpath = './/JOB[@JOBNAME="' + jobName + '"]'
    for job in leftRoot.findall(xpath):
        # increment number
        currentMaxNumber = int(currentMaxNumber) + 1
        oldJobName = job.attrib['JOBNAME']
        jobNameText = re.sub("[0-9]", "", oldJobName)
        newJobText = jobNameText + str(currentMaxNumber)
        old_new_dict[oldJobName] = newJobText
        job.attrib['JOBNAME'] = newJobText
        insertion_point.append(job)

print("##old_new dict map##", old_new_dict)
rightTree.write(input_destinationPath)

# replace autoGeneratedNames in INCOND tag
mergedTree = ET.parse(input_destinationPath)

for old, new in old_new_dict.items():
    xpath = './/JOB[@JOBNAME="' + new + '"]'
    for job in mergedTree.findall(xpath):
        jobOUTAll = job.findall('OUTCOND')
        for jobOUT in jobOUTAll:
            if jobOUT is not None and job.attrib['JOBNAME'] not in rightJobName:
                if jobOUT.attrib['NAME'] is not None:
                    jobOUTList = jobOUT.attrib['NAME'].split('-')  # split string into a list
                    for old, new in old_new_dict.items():
                        jobOUTList = [w.replace(old, new) for w in jobOUTList]
                        jobOUT.attrib['NAME'] = "-".join(jobOUTList)
        jobINAll = job.findall('INCOND')
        for jobIN in jobINAll:
            if jobIN != None and job.attrib['JOBNAME'] not in rightJobName:
                if jobIN is not None and jobIN.attrib['NAME'] is not None:
                    jobINList = jobIN.attrib['NAME'].split('-')  # split string into a list
                    for old, new in old_new_dict.items():
                        jobINList = [w.replace(old, new) for w in jobINList]
                        jobIN.attrib['NAME'] = "-".join(jobINList)

mergedTree.write(input_destinationPath)

# add missing conditions for non migrated group


#parse mergedroot
mergeJobName = []

mergedTree = ET.parse(input_destinationPath)
mergedRoot = mergedTree.getroot()
for job in mergedRoot.findall('SMART_TABLE/JOB'):
    mergeJobName.append(job.attrib['JOBNAME'])
allRemainingJob = set(mergeJobName) & set(allProcessedJobs)

#print("--------duplicate---", dupJob)
#print("------allRemainingJob---", allRemainingJob)
#print("------mergeJobName---", mergeJobName)
for remaining in allRemainingJob:
    xpath = './/JOB[@JOBNAME="' + remaining + '"]'
    for job in leftRoot.findall(xpath):
        jobINAll = job.findall('INCOND')
        for jobIN in jobINAll:
            if jobIN is not None and jobIN.attrib['NAME'] is not None:
                jobINList = jobIN.attrib['NAME'].split('-')  # split string into a list
                commonInList = set(jobINList) & set(allProcessedJobs)
                #print("commoninlist",commonInList)
                if commonInList:
                    xpath = './/JOB[@JOBNAME="' + job.attrib['JOBNAME'] + '"]'
                    for x in mergedRoot.findall(xpath):
                        intextList = []
                        for xin in x.findall('INCOND'):
                            intextList.append(xin.attrib['NAME'])
                            #print(intextList)
                        if jobIN.attrib['NAME'] not in intextList:
                            jobINList = jobIN.attrib['NAME'].split('-')  # split string into a list
                            jobINList = [w.replace(old, new) for w in jobINList]
                            jobIN.attrib['NAME'] = "-".join(jobINList)
                            x.append(jobIN)
        jobOUTAll = job.findall('OUTCOND')
        for jobOUT in jobOUTAll:
            if jobOUT is not None and jobOUT.attrib['NAME'] is not None:
                jobOUTList = jobOUT.attrib['NAME'].split('-')  # split string into a list
                commonOUTList = set(jobOUTList) & set(allProcessedJobs)
                #print("commonoutlist", commonOUTList)
                if commonOUTList:
                    xpath = './/JOB[@JOBNAME="' + job.attrib['JOBNAME'] + '"]'
                    for x in mergedRoot.findall(xpath):
                        intextList = []
                        for xin in x.findall('OUTCOND'):
                            intextList.append(xin.attrib['NAME'])
                            #print(intextList)
                        if jobOUT.attrib['NAME'] not in intextList:
                            x.append(jobOUT)

mergedTree.write(input_destinationPath)


def prettify(input_destinationPath):
    """
        Return a pretty-printed XML string for the Element.
    """
    xml = XD.parse(input_destinationPath)  # or xml.dom.minidom.parseString(xml_string)
    return xml.toprettyxml(indent=" ", newl='')


def strip(elem):
    for elem in elem.iter():
        if (elem.text):
            elem.text = elem.text.strip()
        if (elem.tail):
            elem.tail = elem.tail.strip()

#pretty print
pretty_xml_as_string = prettify(input_destinationPath)

text_file = open(input_destinationPath, "w")
text_file.write(pretty_xml_as_string)
text_file.close()


