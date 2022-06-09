import os, json, csv
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

app = Flask(__name__, template_folder='templates')

indexHtml = """<html>
   <body>
   Please input flat file with a viable target column:
      <form action = "http://localhost:5000/uploader" method = "POST"
         enctype = "multipart/form-data">
         <input type = "file" name = "uploadfile" id = "uploadfile" />
         <input type = "submit" name = "submitbutton" id = "submitbutton"/>
      </form>
   </body>
</html>"""

@app.route('/')
def index():
    return indexHtml

@app.route('/uploader', methods = ['GET', 'POST'])
def benfords_assertion():
    uploadReport = ""
    if request.method == 'POST':
        # check if the post request has the file part

        f = request.files['uploadfile']
        if f.filename == "":
            uploadReport = "No file Name"
        else:
            f.save(secure_filename(f.filename))
            f.seek(0)

            uploadReport += """<html><head><meta charset="utf-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <meta name="description" content="">
                                <meta name="author" content=""><title>Benford's Law</title>
                                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                                <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.1.1/d3.js"></script>
                                </head>
                                <body>File uploaded successfully!"""

            # Retrieve first line to check for Header
            headerLine = str(f.readline(), 'utf-8')
            headerColumns = headerLine.rstrip().split('\t')
            uploadReport += "<br>Columns Count: <b>" + str(len(headerColumns)) + "</b>:<br>"

            # Parse data into Dict
            parsedData = dict()
            for eC in headerColumns:
                parsedData[eC] = []

            columnIsNumber = dict()
            for eC in headerColumns:
                columnIsNumber[eC] = True

            numLines = 0
            with open(secure_filename(f.filename)) as openfileobject:
                for line in openfileobject:
                    # Skip header line
                    if numLines != 0:
                        elems = line.rstrip().split('\t')
                        # rowVals = dict()
                        for colCounter, eachCol in enumerate(elems):
                            # uploadReport += "<br>eachCol: " + eachCol + ", bool:" + str(isfloat(eachCol)) + "."
                            if isfloat(eachCol) == False:
                                columnIsNumber.update({headerColumns[colCounter]: False})
                                # uploadReport += "Yes<br>"
                            parsedData[headerColumns[colCounter]].append(eachCol)
                        # parsedData[numLines] = rowVals
                    numLines += 1

            # Generate histograms for each possible column
            histRes = dict()
            for eC in headerColumns:
                currHisto = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
                if columnIsNumber[eC]:
                    freq = dict()
                    i = 0
                    while i < 10:
                        i += 1
                        freq[str(i)] = 0

                    leadingDigits = []
                    for eachNum in parsedData[eC]:
                        i = 0
                        # Find the leading digit's index, other than the zeros and dots
                        lmd = int(eachNum[0])

                        leadingDigits.append(int(lmd))

                    # Generate histogram for leadingDigits 
                    for eEl in leadingDigits:
                        # uploadReport += "<br>Check for " + str(eEl) + " in leadingDigits .<br>"
                        if str(eEl) in currHisto.keys():
                            currHisto[str(eEl)] += 1
                    histRes[eC] = currHisto
                else:
                    histRes[eC] = currHisto


            uploadReport += "<br>Data rows Count: <b>" + str(numLines) + "</b>."

            uploadReport += """<div class="selectBox" style="margin-top: 10px;">
                                Select column header: <select id="selectedColumn">"""
            selectedUsed = False
            selected = ""
            for eC in headerColumns:

                if eC == '7_2009':
                    selected = " selected"
                else:
                    selected = ""
                histReseCString = map(str,histRes[eC].values())
                uploadReport += "<option value='" + " ,".join(histReseCString) + "' " + selected + ">" + eC + "</option> "
                uploadReport += """
                """
                selectedUsed = True

            uploadReport += """
                                </select>
                            </div><center><div id='graphTitle'><strong>Benford distribution checker</strong></div></center>"""

            uploadReport += """<div class="canvasWrapper">
                                    <canvas id="plotChart"></canvas>
                            </div>""" 

            uploadReport += """<style>
                                .canvasWrapper {
                                    position: relative;
                                    margin: auto;
                                    height: 60vh;
                                    width: 70vw;
                                }
                                </style><script>"""

            defaultFirstColumnToGraph = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            if '7_2009' in headerColumns:
                defaultFirstColumnToGraph = histRes['7_2009'].values()
            else:
                # Return the first column with numbers to see the fit to Benford's distribution
                nonZeroInitial = headerColumns[0]
                i = 0
                while list(histRes[headerColumns[i]].values())[0] == 0:
                    i += 1
                    if i == len(headerColumns):
                        nonZeroInitial = 0
                        break
                nonZeroInitial = i
                defaultFirstColumnToGraph = histRes[headerColumns[nonZeroInitial]].values()

            uploadReport += """
                                var xC = [""" + ", ".join(map(str,defaultFirstColumnToGraph)) + """];"""
            uploadReport += """
                                var xC1 = [""" + str(list(defaultFirstColumnToGraph)[0]) + """];"""
            uploadReport += """
                                var dateC = [1, 2, 3, 4, 5, 6, 7, 8, 9];
                                //console.log(xC1);
                                """
            uploadReport += """var newChart = new Chart(document.getElementById("plotChart"), {
                                data: {
                                    datasets: [
                                    {
                                        type: 'line',
                                        label: 'Expected data distribution',
                                        data: [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6],
                                        borderWidth: 8,
                                        backgroundColor: '#36a2eb',
                                        borderColor: '#36a2eb',
                                        yAxisID: 'y1',
                                    },
                                    {
                                        type: 'bar',
                                        label: 'Observed data distribution',
                                        data: xC,
                                        backgroundColor: '#ff6384',
                                        yAxisID: 'y',
                                    }],
                                    labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                                },
                                options: {
                                            scales: {
                                            y: {
                                                type: 'linear',
                                                display: true,
                                                position: 'left',
                                                ticks: {
                                                    color: '#ff6384',
                                                },
                                            },
                                            y1: {
                                                type: 'linear',
                                                display: true,
                                                position: 'right',
                                                ticks: {
                                                    beginAtZero:true,
                                                    max: 35,
                                                    color: '#36a2eb',
                                                },
                                            }
                                        }
                                    }
                                }
                                );"""
            uploadReport += """
                                const selectedColumn = document.getElementById('selectedColumn');
                                var currentTitle = document.getElementById('graphTitle');
                                selectedColumn.addEventListener('change', plotTracker);
                                function plotTracker(){
                                        const newLabel = selectedColumn.options[selectedColumn.selectedIndex].text;
                                        const newIndex = selectedColumn.options[selectedColumn.selectedIndex]
                                        const newValue = selectedColumn.value
                                        const tempData = newValue.split(',');
                                        //console.log(newValue);
                                        nbins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                                        newChart.data.datasets[1].data = tempData;
                                        newChart.update();
                                        let sum = 0;
                                        const tempInts = tempData.map(x => parseInt(x));
                                        for (let i = 0; i < tempInts.length; i++) {
                                            sum += tempInts[i];
                                            }              

                                        if(sum === 0) {
                                            currentTitle.innerHTML = "Benford distribution checker: " + newLabel + " (This column does not contain numbers)";
                                        }
                                        else {
                                            currentTitle.innerHTML = "Benford distribution checker: " + newLabel + ".";
                                        }
                                    }"""
            uploadReport += """</script>
                                </body>
                                </html>"""

    return uploadReport

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')