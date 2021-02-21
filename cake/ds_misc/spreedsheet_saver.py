import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

#https://docs.google.com/spreadsheets/d/spreadsheetId/edit#gid=sheetId  -- that's how the link looks like;
#spreadsheetId -- id of the table;
#sheetId -- id of the sheet within the table;
#ServiceAccountCredentials includes 9 functions to manipulate tbales after having authenticated;
#There is no way to create document in SpreadsheetAPI with asigning rights to it automatically, but
#there is one in Google Drive API v3;


class Spreadsheet:

    def __init__(self, title, size, email):
        self.valueRanges = []
        self.requests = []
        self.title = title
        CREDENTIALS_FILE = '/app/server_django/bakery/spreadheet-e11e96e6d677.json'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        self.spreadsheet = self.service.spreadsheets().create(body={  # returns spreedsheet object
            'properties': {'title': title, 'locale': 'de_DE'},
            'sheets': [{'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Seite 1',
                'gridProperties': {'rowCount': size[1], 'columnCount': size[0]}
            }}]
        }
        ).execute()

        driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)

        shareRes_admin = driveService.permissions().create(
            fileId=self.spreadsheet['spreadsheetId'],
            body={'type': 'user', 'role': 'writer', 'emailAddress': 'ysharapov@hssoft.com'},
            # access for writing by a link
            fields='id'
        ).execute()

        shareRes_user = driveService.permissions().create(
            fileId=self.spreadsheet['spreadsheetId'],
            body={'type': 'user', 'role': 'writer', 'emailAddress': email},
            # access for writing by a link
            fields='id'
        ).execute()
    def generate_link(self):
        link = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet['spreadsheetId']}/edit#gid={0}"
        return link

    def prepare_setDimensionPixelSize(self, dimension, startIndex, endIndex, pixelSize):
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.spreadsheet['spreadsheetId'],
                      "dimension": dimension,
                      "startIndex": startIndex,
                      "endIndex": endIndex},
            "properties": {"pixelSize": pixelSize},
            "fields": "pixelSize"}})

    def prepare_setColumnsWidth(self, startCol, endCol, width):
        self.prepare_setDimensionPixelSize("COLUMNS", startCol, endCol + 1, width)

    def prepare_setColumnWidth(self, col, width):
        self.prepare_setColumnsWidth(col, col, width)

    def prepare_setValues(self, cellsRange, values, majorDimension="ROWS"):
        self.valueRanges.append(
            {"range": cellsRange, "majorDimension": majorDimension, "values": values})

    def runPrepared(self, valueInputOption="USER_ENTERED"):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'],
                                                                  body={"requests": self.requests}).execute()
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet['spreadsheetId'],
                                                                           body={"valueInputOption": valueInputOption,
                                                                                 "data": self.valueRanges}).execute()
        finally:
            self.requests = []
            self.valueRanges = []

        return (upd1Res['replies'], upd2Res['responses'])

def to_json_serializable(data):
    data_ser = []
    for i in range(data.shape[0]):
        data_ser.append([])
        for j in range(data.shape[1]):
            data_ser[-1].append(str(data.iloc[i, j]))
    
    return data_ser

def save_as_spreadsheet(data, email):
    spreadsheet = Spreadsheet('Prognose', data.shape, email)
    num = data.shape[0]
    print(data.shape)
    data_ser = to_json_serializable(data.T)
    with open('log.txt', mode='w') as f:
       f.write(str(len(data_ser)))
	#f.write(str(len(data_ser[0])))
    spreadsheet.prepare_setValues("A1:E2", list([[column] for column in data.columns]), 'COLUMNS')
    spreadsheet.prepare_setValues(f"A2:E{num + 1}", data_ser, 'COLUMNS')
    spreadsheet.runPrepared()
    link = spreadsheet.generate_link()
    return link
