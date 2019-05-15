import pathlib, time
from subprocess import call

class timer():
    def __init__(self):
        self.beginTimeStr = ""
        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

        self.logFilenameStr = ""
        self.folderStr = "config/"
        self.testingBool = False
        
    def startLog(self):
        self.beginTimeStr = time.strftime("%Y%m%d%H%M%S")
        self.currentTimeStr = time.strftime("%Y%m%d%H%M%S")

        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        with open(pathStr,'w') as logFileHandle:
            logFileHandle.write("")

        self.delimiterStr = "- :" # for convertTime()
        self.phraseStr = "Begin at {}".format(self.convertTime())
        
        self.printPhrase()
        self.printDashLine()

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

    def printTimeStamp(self):
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        self.currentTimeStr = time.strftime("%Y%m%d%H%M%S")
        self.delimiterStr = "- :" # for convertTime()
        timeMsgStr = "[{}] {}".format(self.convertTime(),self.phraseStr)
        print( timeMsgStr )
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr+"\n" )
        
        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

    def runCommand(self):
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        errorStr = "{}{}-error.log".format(
            self.folderStr,self.logFilenameStr
        )
        self.currentTimeStr = time.strftime("%Y%m%d%H%M%S")
        self.delimiterStr = "- :" # for convertTime()
        timeMsgStr = "[{}] Run command: {}".format(self.convertTime(),self.phraseStr)
        print( timeMsgStr )
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr + "\n" )
        
        with open(errorStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr + "\n" )
        
        commandList = self.phraseStr.split(" ")
        if "" in commandList:
            errorMsgStr = "\n[libPrint ERROR MSG] \"\" in command line\n"
            print(errorMsgStr)
            with open(errorStr,'a') as logFileHandle:
                logFileHandle.write( errorMsgStr + "\n" )
            
        if not self.testingBool:
            call(commandList, stdout=open(pathStr,'a'),stderr=open(errorStr,'a'))

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""
        
    def printing(self,printMsgStr):
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        print(printMsgStr)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(printMsgStr+"\n")

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""
        
    def printPhrase(self):
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        print(self.phraseStr)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(self.phraseStr+"\n")

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

    def printBlankLine(self):
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        print("  ")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("  \n")

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

    def printDashLine(self):
        pathStr = "{}{}.log".format(
            self.folderStr,self.logFilenameStr
        )
        pathlib.Path(self.folderStr).mkdir(parents=True,exist_ok=True)

        print("----------")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("----------\n")

        self.currentTimeStr = ""
        self.phraseStr = ""
        self.delimiterStr = ""

    def convertTime(self):
        yearStr   = self.currentTimeStr[0:4]
        monthStr  = self.currentTimeStr[4:6]
        dayStr    = self.currentTimeStr[6:8]
        hourStr   = self.currentTimeStr[8:10]
        minuteStr = self.currentTimeStr[10:12]
        secondStr = self.currentTimeStr[12:14]

        if len(self.delimiterStr) != 3:
            self.delimiterStr =  "-_-"

        convertedMsgStr = (
            self.delimiterStr[0].join([ yearStr, monthStr, dayStr ])
            + self.delimiterStr[1]
            + self.delimiterStr[2].join([ hourStr, minuteStr, secondStr ]))

        return convertedMsgStr

    def stopLog(self):
        self.currentTimeStr = time.strftime("%Y%m%d%H%M%S")
        # yearDiffInt   = int(self.currentTimeStr[0:4])  -int(self.beginTimeStr[0:4])
        # monthDiffInt  = int(self.currentTimeStr[4:6])  -int(self.beginTimeStr[4:6])
        dayDiffInt    = int(self.currentTimeStr[6:8])  -int(self.beginTimeStr[6:8])
        hourDiffInt   = int(self.currentTimeStr[8:10]) -int(self.beginTimeStr[8:10])
        minuteDiffInt = int(self.currentTimeStr[10:12])-int(self.beginTimeStr[10:12])
        secondDiffInt = int(self.currentTimeStr[12:14])-int(self.beginTimeStr[12:14])

        if secondDiffInt < 0 :
            minuteDiffInt = minuteDiffInt -1
            secondDiffInt = secondDiffInt + 60

        if minuteDiffInt < 0 :
            hourDiffInt = hourDiffInt -1
            minuteDiffInt = minuteDiffInt + 60

        if hourDiffInt < 0 :
            dayDiffInt = dayDiffInt -1
            hourDiffInt = hourDiffInt + 24

        if dayDiffInt < 0 :
            totalTimeStr = "More than one month..."
        else:
            totalTimeStr = (
                str(hourDiffInt) + " hr "+
                str(minuteDiffInt) + " min "+
                str(secondDiffInt) + " s "
            )

        self.delimiterStr = "- :" #for convertTime()
        self.phraseStr = "Finished on [{}]\n     Total time: {}\n".format(
            self.convertTime(),
            totalTimeStr
        )
        self.printPhrase()

        self.phraseStr = ""
        self.currentTimeStr = ""
