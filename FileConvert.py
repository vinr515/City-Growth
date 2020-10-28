import re
DATA_LINE = r'[A-Za-z0-9.]'
FILES = """
https://www.census.gov/content/census/en/topics/income-poverty/poverty/data/tables.1990.html/
https://www.census.gov/data/tables/time-series/dec/cph-series/cph-l/cph-l-108.html
https://www2.census.gov/library/publications/decennial/1990/cph-l/cph-l-108.pdf"""

def clean_file(text):
    """Returns a cleaned up version of the file, given a string of everything
in the file"""
    text = text.upper().strip().split("\n")
    text = [i.split(',') for i in text]
    ###Removes all empty strings
    text = [[j for j in i if j] for i in text]
    text = [[j for j in i if(re.findall(DATA_LINE, j))] for i in text]
    for i in range(len(text)):
        if(len(text[i]) == 1 and len(text[i][0].split()) > 1):
            text[i] = text[i][0].split()  
    
    return text

def to_table(text):
    """Turns a list of list of values (from clean_file) into a list
The new list has [start, end, rowLength] that says where each table is"""
    tableSeries, startNum, runNum = [], 0, 0
    for i in range(len(text)):
        rowLength = len(text[i])
        if(rowLength != runNum):
            if(runNum > 1 and (i-startNum) > 1):
                tableSeries.append([startNum, i, runNum])
            startNum = i
            runNum = rowLength

    return tableSeries

def create_table(tableSeries, text):
    """Uses tableSeries to create a list with the actual data values"""
    table = []
    for i in tableSeries:
        newLine = [text[j] for j in range(i[0], i[1])]
        table.append(newLine)

    table = [i for i in table if(len(i) >= 3)]
    return table

def auto_merge(table):
    """Automatically merges any adjacent tables with the same header (first element)"""
    newTable = []
    lastHead = []
    combTable = []
    for i in table:
        if(i[0] != lastHead):
            if(lastHead):
                newTable.append(combTable)
            lastHead = i[0].copy()
            combTable = [j.copy() for j in i.copy()]
            
        else:
            combTable = combTable + i[1:]

    if(combTable):
        newTable.append(combTable)
        
    return newTable

def output_headers(table):
    for i in table:
        print(i[0])
        print("\t", i[-1])
        print()

def check_headers(line):
    for i in line:
        try:
            float(i)
            return False
        except ValueError:
            pass

    return True

def manual_merge(table, merges):
    """Merges any table that the user wants"""
    newTable = []
    index = 0
    holdTable = []
    for i in range(len(table)):
        if(index >= len(merges)):
            break
        if(not(i in merges[index])):
            newTable.append(table[i])
        else:
            if(check_headers(table[i][0]) and holdTable):
                holdTable = holdTable + table[i][1:]
            else:
                holdTable = holdTable + table[i].copy()
                
            if(i == max(merges[index])):
                newTable.append(holdTable)
                index += 1
                holdTable = []

    return newTable

def manual_header(table, header, index):
    """Adds a header manually to a table"""
    newTable = []
    table[index] = [header] + table[index]
        
    return table

def get_abbrs(text):
    """Gets a list of abbreviations with cleaned text (not perfect)"""
    abbrs = [' '.join(i) for i in text if '=' in ' '.join(i)]
    abbrs = [tuple(i.split('=')) for i in abbrs]
    return list(set(abbrs))

def search_abbrs(abbrs, word):
    a = [i for i in abbrs if word.lower().strip() == i[0].lower().strip()]
    if(a):
        return a
    return None

def merge_tables(table, indexes):
    """Merges tables. First column has to have the same values. This would be used
if one table has A values for every X, and a second has B values. This returns
one table with A and B values for every X. """
    lines = {}
    header = []
    for i in indexes:
        if(header):
            header = header + table[i][0][1:]
        else:
            header = table[i][0]
        for j in range(1, len(table[i])):
            if(table[i][j][0] in lines):
                lines[table[i][j][0]] = lines[table[i][j][0]] + table[i][j][1:]
            else:
                lines[table[i][j][0]] = table[i][j].copy()

        for j in lines:
            if(len(lines[j]) != len(header)):
                if(j == "AK"):
                    print(header)
                    print(lines[j])
                numLeft = len(header)-len(lines[j])
                row = lines[j] + ['']*numLeft
                lines[j] = row.copy()

    newTable = [header]
    for i in sorted(lines):
        newTable.append(lines[i])

    return newTable

def get_merge_indexes():
    indexes, line = [], "A"
    while(line != ""):
        line = input("Enter indexes to merge (sep. by comma): (Press Enter to end)  ").strip()
        if(line):
            indexes.append(list(map(int, line.split(','))))

    return indexes

def get_header_indexes(table):
    line = "A"
    while(line != ""):
        line = input("Enter header sep. by comma (enter to exit): ").strip()
        if(not(line)): continue
        index = int(input("Enter the index of the table  ").strip())
        table = manual_header(table, line.split(','), index)

    return table

def convert_pdf(fileName):
    with open(fileName, 'r') as f:
        read = f.read()

    text = clean_file(read)
    table = to_table(text)
    table = create_table(table, text)
    #table = auto_merge(table)
    #output_headers(table)
    #indexes = get_merge_indexes()
    #table = manual_merge(table, indexes)
    
    output_headers(table)
    table = get_header_indexes(table)

    table = auto_merge(table)
    output_headers(table)
    indexes = get_merge_indexes()
    print(indexes)
    if(indexes):
        table = manual_merge(table, indexes)
    
    abbrs = get_abbrs(text)

    return table, abbrs

def find_empty_rows(mergedTable):
    """Finds any rows that might be mistakes when merging tables"""
    return [i for i in mergedTable if i.count('')]

def write_abbrs(abbrs, header, fileName):
    realAbbrs = "-"*5 + fileName + "-"*5 + "\n"
    for i in header:
        line = search_abbrs(abbrs, i)
        if(line):
            realAbbrs += "{}={}\n".format(i, line[0][1])

    with open("Abbreviations.txt", 'a') as f:
        f.write(realAbbrs)
