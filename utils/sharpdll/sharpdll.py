import sys
import clr
clr.AddReference("/utils/sharpdll/ByteTerraUtils")

from ByteTerraUtils import GoogleUtils, DocumentUtils, Session, Ion
import System
REGEX_EXPONENTIAL = "\\d(\\.|,)\\d\\de\\+\\d\\d"
