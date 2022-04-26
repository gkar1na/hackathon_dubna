import sys
import clr
clr.AddReference("/utils/sharpdll/ByteTerraUtils")

from ByteTerraUtils import GoogleUtils, DocumentUtils, Session, Ion
import System

'''SPREADSHEET_ID = "1WEvoZXh8u4zmdTqoVwKjBVQ_k5ktEJgS2jTnfG_F2jk"
SERVICE_ACCOUNT_EMAIL = "documentsbot@documentsbot.iam.gserviceaccount.com"
GOOGLE_API_KEY = "AIzaSyBlzETUEJQJn4lSzTELzSLdKhtW0WCWvDk"
GOOGLE_APP_NAME = "DocumentsBot"
SERVICE_CREDS = "data/servicecreds.json"'''
REGEX_EXPONENTIAL = "\\d(\\.|,)\\d\\de\\+\\d\\d"