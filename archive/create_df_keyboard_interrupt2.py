import pandas as pd


from hplc.file_parsers.AgilentUV import read_Chemstation_file, chemstation_metadata
from hplc.ui.tk_file_open import select_files


def create_df():

    filetype = eval(
        input(
            """Enter 1 to import Agilent Chemstation file(s), 
                or 2 to import example data"""
        )
    )

    if filetype == 1:
        return chemstation_df()

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
    try:
        while True:
            # ask_more = eval(
            #     input("""Enter 1 to import another file, or 2 to stop importing files """)
            # )

            # if ask_more == 1:
            data_filename, folder_path, data_file = select_files()
            wv, xdata, ydata = read_Chemstation_file(data_file)
            more_meta = chemstation_metadata(data_file)
            print("Chromatogram wavelength is: " + str(wv) + " nm")
            d = pd.DataFrame(ydata)
            d.columns = [data_filename]
            df = pd.concat([df, d], axis=1)
            filenames.append(data_filename)
            metadata[data_filename] = more_meta
    except KeyboardInterrupt:
        pass

    return df, metadata


def excel_df():
    fileURL = "https://github.com/brentkendrick/Public-HPLC-files/raw/master/Example_HPLC_Data.xlsx"
    df1colnames = ["x-data", "rep1", "rep2", "rep3", "rep4"]
    return pd.read_excel(fileURL, "testdata", header=None, names=df1colnames)
