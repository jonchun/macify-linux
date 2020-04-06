#!/bin/bash
eval "$(python3 globals.py)"

# -O/--remote-name
#   Write output to a local file named like the remote file we get. 
#   (Only the file part of the remote  file  is  used, the path is cut off.)

# -L/--location
#   (HTTP/HTTPS)  If  the  server  reports that the requested page has moved 
#   to a different location (indicated with a Location: header and a 3XX 
#   response code), this option will make curl redo the request on the new 
#   place.  If  used together  with  -i/--include  or -I/--head, headers from 
#   all requested pages will be shown. When authentication is used, curl only 
#   sends its credentials to the initial host. If a redirect takes curl to a 
#   different host, it  won't be  able  to  intercept  the  user+password. 
#   See also --location-trusted on how to change this. You can limit the
#   amount of redirects to follow by using the --max-redirs option.

# -J/--remote-header-name
#   (HTTP) This option tells the -O/--remote-name option to  use  the  
#   server-specified  Content-Disposition  filename instead of extracting a 
#   filename from the URL.
curl --silent --location -o ${WALLPAPERS_DIR}/${DEFAULT_WALLPAPER} "https://unsplash.com/photos/RPT3AjdXlZc/download?force=true"
