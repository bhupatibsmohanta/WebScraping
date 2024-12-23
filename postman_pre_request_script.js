
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
