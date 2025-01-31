# 🤐 Zipperlab Data

This is the [Django](https://www.djangoproject.com) "data" app ([Python](https://www.python.org/) package) that generates zip files for Zipperlab for [LabCAS](https://edrn-labcas.jpl.nasa.gov/) for the [Early Detection Research Network](https://edrn.nci.nih.gov/).


## 📝 Developer Notes

1.  LabCAS UI calls labcas-backend with the user session, email address, and Solr files query (since it knows only the UI + backend have the authentication of the user)
    -   ~~We could derive the email address through an LDAP query~~
        -   NO! Because this can be used for public data too
    -   UI could abort early at this point if it can determine the file size from the query
2.  LabCAS-backend calls Zipperlab with the shared secret, email address, and Solr files query
    -   Secret token is shared between the two entities
3.  Zipperlab asks Solr for the `FileSize` and makes an estimate about ZIP archive
    -   Compression ratio of 0.5 is what ChatGPT recommends
    -   However, knowing a lot of binary data (DICOM images?) maybe 0.4 is better
        -   Make this a tunable parameter (setting)
    -   If the estimated ZIP size is larger than 2GB, immediately abort
    -   Otherwise, return 200 OK and
        1.  Alert the user that the archive is being prepared
        2.  Launch a task to create the archive
4.  Archive file should be a UUID + `.zip`
5.  Once complete:
    1.  Send an email with the URL to the file ready for download
    2.  Start a task to delete the file after 7 days
        -   Will Celery be able to handle this? Might be better to use cron to just scan for old files
            -   Cron, definitely cron!


My original notes: https://github.com/EDRN/labcas-ui/issues/215#issuecomment-2231989176

Okay, I think for a first pass we can leave out the status features
