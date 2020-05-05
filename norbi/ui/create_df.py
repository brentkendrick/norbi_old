import pandas as pd


from norbi.file_parsers.AgilentUV import read_Chemstation_file, chemstation_metadata
from norbi.ui.tk_file_open import select_file, select_files2
import sys, os, math, warnings

def create_df():

    filetype = eval(
        input(
            """Enter 1 to import Agilent Chemstation file(s), 
                or 2 to import Excel data (will import first sheet in workbook): """
        )
    )

    if filetype == 1:
        return chemstation_df2()

    else:
        return excel_df()


def chemstation_df():
    """Creates a DataFrame with the given input data files"""
    data_filename, folder_path, data_file = select_files()
    wv, xdata, ydata = read_Chemstation_file(data_file)
    metadata = {data_filename: chemstation_metadata(data_file)}
    print("Chromatogram wavelength is: " + str(wv) + " nm")
    df = pd.DataFrame()
    df["x-data"] = xdata
    df[data_filename] = ydata

    filenames = [data_filename]
    while True:
        ask_more = eval(
            input("""Enter 1 to import another file, or 2 to stop importing files """)
        )
        if ask_more == 1:
            data_filename, folder_path, data_file = select_files()
            wv, xdata, ydata = read_Chemstation_file(data_file)
            more_meta = chemstation_metadata(data_file)
            print("Chromatogram wavelength is: " + str(wv) + " nm")
            d = pd.DataFrame(ydata)
            d.columns = [data_filename]
            df = pd.concat([df, d], axis=1)
            filenames.append(data_filename)
            metadata[data_filename] = more_meta
        else:
            break

    return df, metadata


def excel_df():
    fileURL = "https://github.com/brentkendrick/Public-HPLC-files/raw/master/Example_HPLC_Data.xlsx"
    df1colnames = ["x-data", "rep1", "rep2", "rep3", "rep4"]

    datafile = select_file()
    empty_meta = {1: {'Message': 'No metadata for xlsx files!'}}
    # df = pd.read_excel(fileURL, "testdata", header=None, names=df1colnames)
    df = pd.read_excel(datafile, header=0)
    return df, empty_meta

def chemstation_df2():
    """Creates a DataFrame with the given input data files"""
    data_files = select_files2()

    wv, xdata, ydata = read_Chemstation_file(data_files[0])
    folder_path = os.path.split(data_files[0])[0]
    filename = folder_path.split("/")[-1].split(".")[0]
    metadata = {filename: chemstation_metadata(data_files[0])}
    print("Chromatogram wavelength is: " + str(wv) + " nm")
    df = pd.DataFrame()
    df["x-data"] = xdata
    df[filename] = ydata

    filenames = [filename]
    for i in range(int(len(data_files))-1):

        wv, xdata, ydata = read_Chemstation_file(data_files[i+1])
        more_meta = chemstation_metadata(data_files[i+1])
        print("Chromatogram wavelength is: " + str(wv) + " nm")
        d = pd.DataFrame(ydata)
        folder_path = os.path.split(data_files[i+1])[0]
        filename = folder_path.split("/")[-1].split(".")[0]
        d.columns = [filename]
        df = pd.concat([df, d], axis=1)
        filenames.append(filename)
        metadata[filename] = more_meta


    return df, metadata