import mbutil


tileFile = r"E:\GHANA_Data\basemap\selected\031113120110_16.mbtiles"
silent = False
con = mbutil.mbtiles_connect(tileFile, silent)
cur = con.cursor()

mbutil.optimize_connection(cur)
mbutil.mbtiles_setup(cur)

mbutil.compression_prepare(cur, silent)
mbutil.compression_do(cur, con, 256, silent)
mbutil.compression_finalize(cur, con, silent)
mbutil.optimize_database(con, silent)



