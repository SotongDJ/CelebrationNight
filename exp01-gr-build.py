#!/usr/bin/env python3
import librun, libconfig, libgext
global helber
helber="""
--- README of exp01-Genome-Reference-build.py ---
 Title:
  Construct reference from Genome information for further analysis

 Usage:
  python3 exp01-gr-build.py -t <tribe>\\
    --genome=<Path and Name of GENOME File>
    --prefix=<Prefix for HISAT2 index and GFF Info file>

 CAUTION:
  Genome tag and Annotate tag must set with file name only.

 Original Command of Stage 1 (Build HISAT2 Index):
  hisat2-build -p [THREAD] <Path and Name of GENOME File> \\
    <OUTPUT FOLDER for HISAT2>/<codename>
--- README ---
"""
"""
 Postfix of variables:
  -si: String
   -ni: alternative/second string for same Usage
   -fi: string for open()
  -ho: String(that store dir path)
  -ti: Intiger/Float
  -li: List
  -tu: Tuple
  -di: Dictionary
  -fa: File (with open())
  -so: JSON
"""
Confi = libconfig.confi()
class genomerefer(librun.workflow):
    def pesonai(self):
        # self.testing = True
        self.helb = helber

        self.dicodi = {
            "genome" : "",
            "prefix" : "",
            "tribe"  : "",
        }
        self.Synom.input(Confi.diget("synom"))
        self.sync()

        self.comali = []
        self.filasi = "exp01-Genome-Reference-build.py"
        self.libadi = {
            "bin/hisat2build" : Confi.siget("bin/hisat2build"),
            "index/hisat"     : Confi.siget("index/hisat"),
            "result/log"      : Confi.siget("result/log"),
            "run/thread"      : Confi.siget("run/thread"),
            "refer/annotate"  : Confi.diget("refer/annotate"),
        }
        self.prelogi = self.libadi.get("result/log")+"/exp01-gr-build-"

    def actor(self):
        self.genosi = self.dicodi.get("genome","")
        self.pifisi = self.dicodi.get("prefix" ,"")
        self.tibesi = self.dicodi.get("tribe" ,"")

        self.head()

        self.frasi = "==========\nStage 1 : Build HISAT2 Index\n=========="
        self.printe()

        self.binosi = self.libadi.get("bin/hisat2build")
        self.tereli = ["-p",self.libadi.get("run/thread")]
        self.oputsi = self.libadi.get("index/hisat") + "/" + self.pifisi

        self.comali = []
        self.comali.append(self.binosi)
        self.comali.extend(self.tereli)
        self.comali.append(self.genosi)
        self.comali.append(self.oputsi)

        self.runit()

        self.frasi = "==========\nStage 2 : Copy Genome FASTA to HISAT2 Index folder\n=========="
        self.printe()
        self.comali = ["cp",self.genosi,self.oputsi+".fa"]

        self.runit()

        self.frasi = "==========\nStage 3 : Extract GFF Information\n=========="
        self.printe()

        Gekta = libgext.gffextract()
        Gekta.testing = self.testing
        Gekta.prelogi = self.libadi.get("result/log")+"/exp01-grb-libgext-"
        Gekta.dicodi = {
            "input"  : [self.libadi.get("refer/annotate").get(self.tibesi)],
            "tribe"  : self.tibesi,
            "output" : self.pifisi+"-gff-info.json"
        }
        Gekta.actor()

        self.printbr()

        self.endin()

GeRef = genomerefer()
