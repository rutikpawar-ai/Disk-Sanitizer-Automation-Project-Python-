###############################################
#
#  
# 
# Importing the required libraries
# 
# 
#
##############################################

import os
import sys
import hashlib
import time
import schedule

###############################################
#
#  functional name : calculatechecksum
# input : from findduplicate
# description : Gives the Checksum of directory
# date : 26/07/2026
# Auther : Rutik Pawar
#
##############################################

def calculatechecksum(filename):
    fobj = open(filename , "rb")
    hobj = hashlib.md5()   #imp

    buffer = fobj.read(1024)

    while(len(buffer)>0):
        hobj.update(buffer)   #imp
        buffer = fobj.read(1024)
    fobj.close()
    return hobj.hexdigest() #imp 

###############################################
#
# functional name : findduplicate
# input : from deleteduplicate
# description : Gives the names and count of duplicate files in directory
# date : 26/07/2026
# Auther : Rutik Pawar
#
##############################################

def findduplicate(directoryname):
    ret = False
    ret = os.path.exists(directoryname)

    if ret == False:
        print("Path is invalid")
        return
    ret = os.path.isdir(directoryname)

    if ret == False:
        print("it is not a directory")
        return

    duplicate = {}
    
    for foldername, subfolder, filename, in os.walk(directoryname):
        for fname in filename:
            fname = os.path.join(foldername,fname)

            checksum = calculatechecksum(fname)


            if checksum in duplicate:
                
                duplicate[checksum].append(fname)

            else:
                
                duplicate[checksum] = [fname]


    return duplicate

###############################################
#
# functional name : deleteduplicate
# input : From Main function
# description : It delete the Duplicate files in directory
# date : 26/07/2026
# Auther : Rutik Pawar
#
##############################################

def delteduplicate(directoryname):
    start_time = time.perf_counter()
    border = "-"*40
    print(border)
    timestamp = time.ctime()
    logfilename = "Detelefile%s.Log"%(timestamp)
    logfilename = logfilename.replace(" " , "_")
    logfilename = logfilename.replace(":" , "_")
       
    
    mydict = findduplicate(directoryname)
    
    result = list(filter(lambda x : len(x)>1, mydict.values())) 
    count = 0
    totaldeleted = 0
    totalfiles = sum(len(value) for value in mydict.values())
    for value in result:
        
        for subvalue in value:

            count = count + 1
            if (count > 1):
                os.remove(subvalue)
                totaldeleted = totaldeleted + 1
        count = 0
    print("total deleted files:", totaldeleted)
    
    fobj = open(logfilename , "w")
    fobj.write(border+"\n")
    fobj.write("Disk Sanitizer \n")
    fobj.write(border+"\n\n")
    fobj.write(f"Total files are : {totalfiles}\n \n")
    fobj.write(border+"\n\n")
    fobj.write(f"Deleted Files From the directory are : {totaldeleted}\n \n")
    end_time = time.perf_counter()
    fobj.write(border+"\n\n")
    
    fobj.write(f"Time required is : {end_time - start_time:.4f}\n \n")
    fobj.write(border+"\n")
    print(border)
    print("Thank you for using Disk Sanitizer Automation Script")
    print(border)

###############################################
#
# functional name : This is main function
# input : commond line argument
# description : It controls the script
# date : 26/07/2026
# Auther : Rutik Pawar
#
##############################################

def main():
    Border = "-"*40
    print(Border)
    print("Disk Sanitizer Automation Script")
    print(Border)
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This automation script is use to travel the directory")
        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Please execute the script as")
            print("Python Filename.py DirectoryName")
            print("DirectoryName should be absulute path")
        else:
    
            schedule.every(1).minute.do(delteduplicate,sys.argv[1])
                
            while True:
                schedule.run_pending()
                time.sleep(1)
                
    else:
        print("invalid nuber of arguments")
        print("please use --h or use --u ")
    
###############################################
#
#  
# 
# This is starter of program
# 
# 
#
##############################################

if __name__ == "__main__":
    main()