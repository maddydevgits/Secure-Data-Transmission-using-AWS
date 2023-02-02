import streamlit as st
import boto3
import hashlib

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

def app():
    st.title('Secure Data Transmission')

    file_st=st.file_uploader('Upload the Data File',type=['txt','pdf','doc','docx'])

    if file_st is not None:
        file_details={}
        file_details['type']=file_st.type
        file_details['size']=file_st.size
        file_details['name']=file_st.name
        st.write(file_details)
        if file_details['type']=='application/pdf':
            st.error('pdf found')
            with open('uploads/file.pdf','wb') as f:
                f.write(file_st.getvalue())
            st.warning('Hash: '+hash_file('uploads/file.pdf'))
        elif file_details['type']=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            st.error('doc found')
            with open('uploads/file.doc','wb') as f:
                f.write(file_st.getvalue())
            st.warning('Hash: '+ hash_file('uploads/file.doc'))
        elif file_details['type']=='text/plain':
            st.error('txt found')
            with open('uploads/file.txt','wb') as f:
                f.write(file_st.getvalue())
            st.warning('Hash: ' + hash_file('uploads/file.txt'))
        st.success('File Saved')
    