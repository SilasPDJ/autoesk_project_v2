import types
# vscode
# import modulefinder
import os
import sys
from dateutil import relativedelta

from pathlib import Path

from default.sets.now import Now
from default.sets.pathmanager import Dirs
from default import HasJson

from default.data_treatment import ExcelToData
from default.data_treatment.transformers import pdf2jpg, jpg2txt, pdf2txt

from default.interact import *
from default.webdriver_utilities import *
from default.webdriver_utilities import WDShorcuts

from pgdas_fiscal_oesk.emails_date_scrap import EmailsDateScrap
from pgdas_fiscal_oesk.relacao_nfs import tres_valores_faturados, NfCanceled
try:

    from _init_email import EmailExecutor
    # import platform
except ImportError:
    pass

