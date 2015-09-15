#!/usr/bin/python

import os

# Turn on debug mode.
import cgi, cgitb
cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html\n")

html_start = ''
html_end = ''
html_container = ''

def do_csv_to_table(csvfilename):
    import csv
    ## print "csvfilename = " + csvfilename + "\n"

    if not os.path.exists(csvfilename):
        print "Can't access csvfile" + csvfilename + "\n"
        return

    fh = open(csvfilename)
    reader = csv.reader(fh, delimiter=',')
    rownum = 0
    table_data = "<table class=\"sdk\">\n  <thead>\n"

    for row in reader:  # Read a single row from the CSV file
        if rownum == 0:  ## header row
            table_data += "    <tr>\n"
            for column in row:
                table_data += "      <th>" + column + "</th>\n"
            table_data += "    </tr>\n  </thead>\n  </tbody>\n"    

        else:  ## all other rows
            table_data += "    <tr>\n"
            for column in row:
                table_data += "      <td>" + column + "</td>\n"
            table_data += "    </tr>\n"
        rownum += 1

    table_data += "  </tbody>\n</table>\n"

    # Close opend file
    fh.close()
    ## print "Created " + str(rownum) + " row table."

    return table_data;


def do_csv_to_chart(csvfilename):
    import numpy as np
    from matplotlib import pyplot as plt
    ## print "csvfilename = " + csvfilename + "\n"

    if not os.path.exists(csvfilename):
        print "Can't access csvfile" + csvfilename + "\n"
        return
	
    OX = []
    OY = []

    try :
    	with open(csvfilename, 'r') as openedFile :
            for line in openedFile :
                tab = line.split(',')
                print tab
                OY.append(int(tab[1]))
                OX.append(str(tab[0]))
    except IOError :
        print("IOError!")

    print OX
    print OY

    fig = plt.figure()

    width = .75
    ind = np.arange(len(OY))
    plt.bar(ind, OY)
    plt.xticks(ind + width / 2, OX)

    fig.autofmt_xdate()

    plt.savefig("chart.pdf")

## html

##<!DOCTYPE html>
def do_start_end_html():
    global html_start
    html_start = '''
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>SDKs Build Test</title>
<style>
html { font-family:Arial, Helvetica, sans-serif; color:#333; }
body { background:#333; margin:0; }  ## #ccc
#container { width:1000px;
margin-top:5px;
margin-right:auto;
margin-bottom:5px;
margin-left:auto;
#background:#fff;
}

#devel {
  width:32%;
  margin:5px;
  padding:0px;
  float:left;
  clear:both;
  font-size:1.0em;
}
h1, h2, h3, h4 {
  font-family:Helvettica,Arial,sans-serif;
  #font-size:1.2em;
  padding-left:2px;
}
h2   {color:#8B69F2}
h3   {color:#2CCF85}
h4   {color:#8B69F2}


table.sdk {
  font-family:Arial,Helvettica,sans-serif;
  font-size:1.0em;
  background-color: #333;
  color: #eee;
}
th {
  background-color: #333;
  color: #eee;
  height: 25px;
  text-align:center;
  padding-left:5px;
}
td {
  height: 25px;
  padding-left:5px;
}

</style>
</head>
<body>

'''

    global html_end
    html_end = '''
<P> </P>
</body>
</html>
'''

def do_container_html():
    global html_container
    
    if (os.path.isdir("./export")):
        data_dir = './export'
    
    sdk_commits_day_table = do_csv_to_table('sdk-commits-per-day-stat.csv')
    do_csv_to_chart('sdk-commits-per-day-stat.txt')
    
   # print sdk_commits_day_table 
    
    html_container = '''
<!-- CONTAINER -->
<div class="container">
    <!-- HEADER -->
    <div id="devel">
        <div>
            <h4>Commits per day - SDK</h4>
            <hr color="#999">    

            <!-- table -->
            '''+sdk_commits_day_table+'''

        </div>
    </div>  <!-- DEVEL -->
    <div id="chart">
        <div>
	    <embed src="chart.pdf" width="500" height="375" type='application/pdf'>
        </div>
    </div>  <!-- ~Chart -->
</div>  <!-- CONTAINER -->
'''

do_start_end_html()
do_container_html()
print html_start
print html_container
print html_end
