#!/usr/bin/env python3
import libPrint
import pathlib
baCombineList = [["testing","speciesTestingA"]]

testingBool = False
gffreadStr = "bin/cufflinks/gffread {inputFile} -T -o {outputFile}"
inputStr = "data/dbga-GenomeAnnotation/{annotation}/{annotation}.gff3"
outputStr = "data/dbga-GenomeAnnotation/{annotation}/{annotation}.gtf"
copyStr = "cp -vf {output} {target}"
targetStr = "data/05-ds-Stringtie/{branch}/{annotation}-trimQ30-merged.gtf"

for baList in baCombineList:
    branchStr = baList[0]
    annotationStr = baList[1]

    Print = libPrint.timer()
    Print.logFilenameStr = "06-CuffDiff-gffConversion-{branch}-{annotate}".format(
        branch=branchStr,
        annotate=annotationStr,
    )
    Print.folderStr = "data/dbga-GenomeAnnotation/{annotate}/".format(annotate=annotationStr)
    Print.testingBool = testingBool
    Print.startLog()
    
    inputPath = inputStr.format(annotation=annotationStr)
    outputPath = outputStr.format(annotation=annotationStr)
    targetPath = targetStr.format(branch=branchStr,annotation=annotationStr)

    if not pathlib.Path(outputPath).exists():
        CommandStr = gffreadStr.format(inputFile=inputPath,outputFile=outputPath)
        Print.phraseStr = CommandStr
        Print.runCommand()

    CommandStr = copyStr.format(output=outputPath,target=targetPath)
    Print.phraseStr = CommandStr
    Print.runCommand()

    Print.stopLog()