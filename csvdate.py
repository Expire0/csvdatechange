import re
from datetime import datetime
from settings import Settings
#import inspect
"""
The function will open a file specified in the settings
The file should be of csv format or on a similar format with defined 
columns that can be splited easily

The use case is to modify easily and change date format in big csv files
Set the current and wished date format on the settings file
Set the output file name and run the script to get the new file with new dates
"""

def main(s):
    # test the settings in the s variable
    try:
        isinstance(s, Settings)
    except:
        raise("The script needs an instance of Settings as argument")

    # read the file
    with open(s.in_file, 'r') as f:
        myfile = f.read()
        f.closed

    # will read each lines
    # tranform the date to new format and append to out_file
    for line in myfile.split('\n'):
        # if the first line match the header
        # write the header to the out_file
        # this will flush the out_file if it already exists
        if re.match(r'^{}$'.format(s.headers), line):
            with open(s.out_file, 'w') as f_out:
                f_out.write(s.headers)
                f_out.write('\n')
                f_out.closed
            continue
        # split the line by settings split character
        col = line.split(s.split_char)
        dates = []
        # get a list of dates column from the setting index variable
        try:
            for index in s.date_index:
                dates.append(col[index])
        except IndexError:
            if line != '':
                print('No change for line \n>{}'.format(line))
            continue
        newdates = []
        # convert the dates to the new format
        for d in dates:
            dt_format = datetime.strptime(d, s.in_format)
            dest_date = dt_format.strftime(s.out_format)
            newdates.append(dest_date)

        newlinelist = []
        # recreate the line using the original
        # and subtituting the old date format with the new one
        # using the index from the settings
        # a cursor keeps the list in order
        cursor = 0
        for x in range(s.csv_row_len):
            if x not in s.date_index:
                newlinelist.append(col[x])
            else:
                newlinelist.append(newdates[cursor])
                cursor += 1
        newline = ','.join(newlinelist)
        # write the new line to out_file
        with open(s.out_file, 'a') as f_out:
            f_out.write(newline)
            f_out.write('\n')
            f_out.closed
