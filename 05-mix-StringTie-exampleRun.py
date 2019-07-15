#!/usr/bin/env python3
import libConfig, libPrint, pathlib
import libStringtie

# standared workflow
SAssembling = libStringtie.assembler()
SAssembling.branchStr = "testing"
SAssembling.headerStr = "Stringtie"
SAssembling.assembling()

SMerging = libStringtie.merger()
SMerging.branchStr = "testing"
SMerging.headerStr = "Stringtie"
SMerging.merging()

SEstimating = libStringtie.estimator()
SEstimating.branchStr = "testing"
SEstimating.headerStr = "Stringtie"
SEstimating.estimating()

# directly workflow
SDEstimating = libStringtie.estimator()
SDEstimating.branchStr = "testing"
SDEstimating.directEstimating = True
SDEstimating.headerStr = "dsStringtie"
SDEstimating.estimating()

SDMerging = libStringtie.merger()
SDMerging.branchStr = "testing"
SDMerging.headerStr = "dsStringtie"
SDMerging.merging()

# without annotation worflow
Assembling = libStringtie.assembler()
Assembling.branchStr = "testing"
Assembling.withoutAnnotation = True
Assembling.headerStr = "waStringtie"
Assembling.assembling()

Merging = libStringtie.merger()
Merging.branchStr = "testing"
Merging.headerStr = "waStringtie"
Merging.merging()

Estimating = libStringtie.estimator()
Estimating.branchStr = "testing"
Estimating.headerStr = "waStringtie"
Estimating.estimating()
