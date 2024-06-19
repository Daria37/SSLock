const express = require("express");
const { spawn } = require('child_process');
const bodyParser = require('body-parser');

const app = express();

app.use(express.static('public'));

// создаем парсер для данных application/x-www-form-urlencoded
const urlencodedParser = bodyParser.urlencoded({ extended: false });

app.get("/", function (_, res) {
    res.sendFile(__dirname + "/public/chain.html");
    console.log(__dirname + "/public/chain.html");
});

app.post("/public", urlencodedParser, function (req, res) {
    const dom = req.body.Domen;
    const org = req.body.Org;
    const code = req.body.Code;
    const town = req.body.Town;
    const city = req.body.City;
    const source = req.body.source; // Получаем значение источника данных

    if (source === 'com') {
        const pythonProcess = spawn('python', ['com.py', dom + "-" + org + "-" + code + "-" + town + "-" + city]);
        
        pythonProcess.stdout.on('data', (data) => {
            res.send(data.toString());
        });

    } else if (source === 'mingos') {
        const pythonProcess2 = spawn('python', ['mingos.py', dom + "-" + org + "-" + code + "-" + town + "-" + city]);
        
        pythonProcess2.stdout.on('data', (data) => {
            res.send(data.toString());
        });
    } else if (source === 'chain') {
        const pythonProcess2 = spawn('python', ['blockchain.py', dom + "-" + org + "-" + code + "-" + town + "-" + city]);
        
        pythonProcess2.stdout.on('data', (data) => {
            res.send(data.toString());
        });
    } else {
        res.send('Invalid source');
    }
});


//Creates the server on default port 8080 and can be accessed through localhost:8080
app.listen(8080, () => console.log("Сервер запущен..."));