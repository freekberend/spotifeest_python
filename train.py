import pandas as pd


#import csv as dataframe
df = pd.read_csv("train.csv", delimiter = ",",encoding = "utf-8")
print(df)


#rslt_df = df[df["Artist Name"] == "Eyal Golan"]
#print(rslt_df)

#check_df = df[df["Track Name"].str.contains("◊")]
#print(check_df)
#check2_df = df[df["Track Name"].str.contains("√")]
#print(check2_df)

#delete track names containing strange character
df_new = df.drop(df[(df["Track Name"].str.contains("◊")) | (df["Track Name"].str.contains("√"))].index)
print(df_new)

#check if removed
#check_df_new = df_new[df_new["Track Name"].str.contains("◊")]
#check2_df_new = df_new[df_new["Track Name"].str.contains("√")]
#print(check2_df_new)
#print(check_df_new)

#select rows
#print(df_new.iloc[8000:8030,])

#result = df[["Artist Name", "Track Name","tempo"]]
#result

#tempo180 = df[df["tempo"]>= 180]
#tempo180

#check NaN values columns
df.isna().any()

#check NaN values rows
df_new[df_new.isna().any(axis=1)]
df_new["Artist Name"] = df_new["Artist Name"].str.lower()
df_new["Track Name"] = df_new["Track Name"].str.lower()

print(df_new)

def select_artist():
    x_artist = input("name artist: ")
    contain_values = df_new[df_new["Artist Name"].str.contains(x_artist.lower())]
    return contain_values

select_artist()

def select_song():
    x_song = input("please name a song title: ")
    contain_song = df_new[df_new["Track Name"].str.contains(x_song.lower())]
    return contain_song

select_song()