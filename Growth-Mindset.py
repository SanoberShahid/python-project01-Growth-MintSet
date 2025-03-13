import openpyxl
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📀 DataSweeper - Sterling Integrator by Sanober-Shahid")
st.write("Transform your files between CSV and Excel format with built-in data cleaning and project creation for Q3!")

# File uploader (Fixed issues)
uploaded_files = st.file_uploader("Upload your files (Only CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file with encoding handling
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file, encoding='utf-8')
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading {file.name}: {str(e)}")
            continue

        # Display file details
        st.write(f"🔍 Preview of {file.name}:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("⚙️ Data Cleaning Options")

        clean_data = st.checkbox(f"Clean data for {file.name}")

        if clean_data:
            col1, col2 = st.columns(2)

            # Remove duplicates with session state
            if col1.button(f"Remove duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates Removed!")

            # Fill missing values
            fill_missing = col2.checkbox(f"Fill missing values for {file.name}")
            if fill_missing:
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ Missing values filled!")

        # Select columns to keep
        st.subheader("📊 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False, encoding='utf-8')
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            
            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")





# import openpyxl
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO
# st.set_page_config(page_title="Data Sweeper", layout="wide")

# # Custom CSS
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: black;
#         color: white;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Title and description
# st.title("📀 DataSweeper - Sterling Integrator by Sanober-Shahid")
# st.write("Transform your files between CSV and Excel format with built-in data cleaning and project creation for Q3!")

# # File uploader (Fixed issues)
# uploaded_files = st.file_uploader("Upload your files (Only CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext = os.path.splitext(file.name)[-1].lower()

#         if file_ext == ".csv":
#             df = pd.read_csv(file, encoding='utf-8')  # Encoding fix
#         elif file_ext == ".xlsx":
#             df = pd.read_excel(file, engine="openpyxl")  # Fixed issue
#         else:
#             st.error(f"Unsupported file type: {file_ext}")
#             continue

#         # Display file details
#         st.write("🔍 Preview of DataFrame:")
#         st.dataframe(df.head())

#         # Data cleaning options
#         st.subheader("⚙️ Data Cleaning Options")
#         if st.checkbox(f"Clean data for {file.name}"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Remove duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("✅ Duplicates Removed!")
#             with col2:
#                 if st.checkbox(f"Fill missing values for {file.name}"):
#                     numeric_cols = df.select_dtypes(include=["number"]).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("✅ Missing values filled!")

#         # Select columns to keep
#         st.subheader("📊 Select Columns to Keep")
#         columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
#         df = df[columns]

#         # Data visualization
#         st.subheader("📈 Data Visualization")
#         if st.checkbox(f"Show visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

#         # Conversion options
#         st.subheader("🔄 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

#         if st.button(f"Convert {file.name}"):
#             buffer = BytesIO()
#             if conversion_type == "CSV":
#                 df.to_csv(buffer, index=False, encoding='utf-8')  # Fixed issue
#                 file_name = file.name.replace(file_ext, ".csv")
#                 mime_type = "text/csv"
#             elif conversion_type == "Excel":
#                 df.to_excel(buffer, index=False, engine="openpyxl")  # Fixed issue
#                 file_name = file.name.replace(file_ext, ".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

#             buffer.seek(0)

#             st.download_button(
#                 label=f"⬇️ Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

# st.success("✅ All files processed successfully!")



#python -m streamlit run c:/python/Growth-Mindset.py




# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# st.set_page_config(page_title= "Data Sweeper", layout="wide")

# #custom css
# st.markdown(
#     """
#   <style>
#   .stApp{
#   background-color: black;
#   color: white;
#   }
#   </style>
#   """,
#   unsafe_allow_html=True
# )

# #title and description
# st.title("📀 DataSweeper sterling integrator by Sanober-Shahid")
# st.write("Transform your files between CSV and Excel formate with build in data-cleanning and Creating the Project for Quator 3!")

# #file uploader

# uploaded_files=st.file_uploader("Upload your files (Except CVS OR EXCEL):", type=["cvs", "xlsx"], except_multiple_files=(True))

# if uploaded_files:
#     for file in uploaded_files:
#         file_ext= os.path.splitext(file.name)[-1].lower()

#         if file_ext == ".csv":
#             df = pd.read_csv(file)
#         elif file_ext == "xlsx":
#             df = pd.read_excel(file)
#         else:
#             st.error(f"unsuppoerted file type: {file_ext}")
#             continue

#    #files details
#         st.write("🔍 preview the head of the Dataframe")
#         st.dataframe(df.head())

#         #data-cleanning 
#         st.subheader("⚙️ Data-Cleanning Options")
#         if st.checkbox(f"clean data for {file.name}"):
#             col1, col2, = st.columns(2)
#             with col1:
#                 if st.button(f"Remove duplicate from the file : {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write(" Duplicates Removed!")
#             with col2:
#                 if st.checkbox(f"fill missing values :  {file.name}"):
#                     numeric_cols = df.select_dtypes(include=["number"]).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("Missing values have been filled!")
               

#         st.subheader("Select columns too keep!")  
#         coloumns = st.multiselect(f"Choose column for {file.name}", df.columns, default=df.columns)   
#         df = df[coloumns]    


#         #data visualization
#         st.subheader("Data visualization")
#         if st.checkbox(f"Show visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])


#         #conversion options
#         st.subheader("Conversion options")   
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CVS", "Excel"], key=file.name) 
#         if st.button(f"Convert {file.name} "):
#             buffer = BytesIO()
#             if conversion_type == "CVS":
#                 df.to.csv(buffer, index= False)
#                 file_name = file.name.replace(file_ext, ".csv")
#                 mime_type = "text/csv"

#             elif conversion_type == "Excel":
#                 df.to.to_excel(buffer, index= False) 
#                 file_name = file.name.replace(file_ext, ".xlsx")
#                 mime_type = "application/vnd.openxmlformates-officedocument.spreadsheethml.sheet"
#             buffer.seek(0)

#             st.download_button(
#                 label=f"Doenload {file.name} as {conversion_type}",
#                 data = buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

# st.success ("ALL FILES PROCESSED SUCCESFULLY!")      