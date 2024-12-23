# WebScraping

Solution 1: Find the automated work flow created using UI-Path RPA tool
<< see workflow.docx >>
==============================================================================================================

Solution 2: Using 1 Postman Post method.

Post method: https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetid}:batchUpdate
here, spreadsheetid: "1xyNLCHxpZ_6vULjMLJmSWJ9ILp3tTI6Ky5YwC31g-qs"

POST: https://sheets.googleapis.com/v4/spreadsheets/1xyNLCHxpZ_6vULjMLJmSWJ9ILp3tTI6Ky5YwC31g-qs:batchUpdate

Set pre-request script
    - Use pre-request script to get the html response from wikipedia url.
    - parse the response to desired output format i.e. finals_data
    - set environment variable finals_data so that it can be accessed in the body section

    
const url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals";

pm.sendRequest(url, function (err, res) {
    if (err || res.code !== 200) {
        console.log("Failed to fetch webpage");
        return;
    }

    const cheerio = require('cheerio');
    const $ = cheerio.load(res.text());
    

    const rows = $("#mw-content-text > div.mw-parser-output > table:nth-of-type(4) > tbody > tr").slice(1);

    let finals_data = [];

    //console.log(rows.text())

    rows.each((index, row) => {
        const cells = $(row).find("th, td");

        const year = $(cells[0]).find("a").text().trim();
        const winner = $(cells[1]).find("span a, a").first().text().trim();
        const score = $(cells[2]).find("a").first().text().trim();
        const runner_up = $(cells[3]).find("span span a, span a").first().text().trim();

        if (year && winner && score && runner_up) {
            finals_data.push({
                values: [
                    { userEnteredValue: { stringValue: year } },
                    { userEnteredValue: { stringValue: winner } },
                    { userEnteredValue: { stringValue: score } },
                    { userEnteredValue: { stringValue: runner_up } }
                ]
            });
        }
    });

    pm.environment.set("finals_data", JSON.stringify(finals_data.slice(0, 10)));

});


Set body:
  - provide parameterized request body with id of the sheet in spreadsheet to be updated:
    {"requests": [{"appendCells": {"sheetId": {{sheetid}}, "rows": {{finals_data}},"fields": "*"}}]}
    Here sheetid = 250923555

  sample body
    {"requests": [{"appendCells": {"sheetId": 250923555, "rows": {{finals_data}},"fields": "*"}}]}


SET AUTHORIZATION:
- configure new token using below details:
    Token Name: google-api-token
    Grant Type: Authorization code
    Callback URL: http://localhost:8800/api/auth
    Auth URL: https://accounts.google.com/o/oauth2/v2/auth
    Access Token URL: https://oauth2.googleapis.com/token
    Client ID: 423857421920-qolfo74r62vn8ddv9ej05svs64ec8ar7.apps.googleusercontent.com
    Client Secret: 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
    Scope: https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/drive.file
    Client Authentication: Send client credential in body

  Generated token will remain valid for 1hr

  Now you're set to send the post request which will extract 10 fifa worldcup finals & append it to spreadsheet:
  https://docs.google.com/spreadsheets/d/1xyNLCHxpZ_6vULjMLJmSWJ9ILp3tTI6Ky5YwC31g-qs/edit?usp=drive_link

==================================================================================================================

Solution 3: Using python program

<< see beautiful_scrap.py >>
