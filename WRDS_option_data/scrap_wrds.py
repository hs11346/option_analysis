import wrds
conn = wrds.Connection()

df = conn.raw_sql("""select * 
                        from optionm_all.opprcd2022
                        """,
                     date_cols=['date'])

